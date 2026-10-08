// 마네킹 몸 치수와 3D 메시.
// 단위는 미터, 발바닥이 y=0, 마네킹은 +z(카메라 쪽)를 바라본다.
// 옷 메시(garments.js)도 이 치수를 그대로 써서 몸에 맞게 만든다.
import * as THREE from "three";

export const BODY = {
  neckTopY: 1.47,
  shoulderY: 1.4,
  armpitY: 1.27,
  waistY: 1.08,
  hipY: 0.96,
  crotchY: 0.8,
  shoulderWidth: 0.38,
  armAngle: THREE.MathUtils.degToRad(16), // A자 포즈: 팔이 수직에서 벌어진 각도
};

// 몸통 단면(타원) 프로필: y, 가로 반지름 rx, 앞뒤 반지름 rz (위에서 아래로)
const TORSO_PROFILE = [
  [1.47, 0.052, 0.052],
  [1.44, 0.075, 0.068],
  [1.415, 0.155, 0.095],
  [1.39, 0.19, 0.105],
  [1.33, 0.18, 0.118],
  [1.24, 0.16, 0.108],
  [1.14, 0.138, 0.094],
  [1.08, 0.134, 0.092],
  [0.99, 0.158, 0.104],
  [0.92, 0.166, 0.108],
  [0.85, 0.15, 0.098],
  [0.8, 0.095, 0.07],
  [0.78, 0.02, 0.02],
];

const torsoCurve = new THREE.CatmullRomCurve3(
  TORSO_PROFILE.map(([y, rx, rz]) => new THREE.Vector3(rx, y, rz)),
  false,
  "centripetal",
);
// y로 반지름을 찾기 위한 조회 테이블 (y 내림차순)
const torsoTable = torsoCurve.getSpacedPoints(400);

export function torsoRadiusAt(y) {
  const t = torsoTable;
  if (y >= t[0].y) return { rx: t[0].x, rz: t[0].z };
  for (let i = 1; i < t.length; i++) {
    if (y >= t[i].y) {
      const k = (y - t[i].y) / (t[i - 1].y - t[i].y || 1);
      return { rx: THREE.MathUtils.lerp(t[i].x, t[i - 1].x, k), rz: THREE.MathUtils.lerp(t[i].z, t[i - 1].z, k) };
    }
  }
  const last = t[t.length - 1];
  return { rx: last.x, rz: last.z };
}

// 옷이 덮어야 하는 반지름: 엉덩이 아래로는 양쪽 다리까지 감싸도록 넓게 유지한다.
export function coverRadiusAt(y) {
  const r = torsoRadiusAt(Math.max(y, 0.8));
  if (y < BODY.hipY) {
    r.rx = Math.max(r.rx, 0.168);
    r.rz = Math.max(r.rz, 0.11);
  }
  return r;
}

// 팔·다리 뼈대: side = -1(화면 왼쪽, -x) 또는 +1(화면 오른쪽, +x)
export function armPath(side) {
  const root = new THREE.Vector3(side * 0.172, 1.372, -0.005);
  const dir = new THREE.Vector3(side * Math.sin(BODY.armAngle), -Math.cos(BODY.armAngle), 0);
  const elbow = root.clone().addScaledVector(dir, 0.29).add(new THREE.Vector3(0, 0, -0.01));
  const wrist = elbow.clone().addScaledVector(dir, 0.255).add(new THREE.Vector3(0, 0, 0.03));
  return makeLimb([root, elbow, wrist], [0.05, 0.041, 0.031], side);
}

export function legPath(side) {
  const root = new THREE.Vector3(side * 0.085, 0.9, 0);
  const knee = new THREE.Vector3(side * 0.092, 0.48, 0.01);
  const ankle = new THREE.Vector3(side * 0.098, 0.085, -0.005);
  return makeLimb([root, knee, ankle], [0.084, 0.055, 0.037], side);
}

function makeLimb(points, radii, side) {
  const curve = new THREE.CatmullRomCurve3(points, false, "centripetal");
  const length = curve.getLength();
  // 각 관절까지의 길이 비율 (반지름 보간용)
  const cum = [0];
  for (let i = 1; i < points.length; i++) cum.push(cum[i - 1] + points[i].distanceTo(points[i - 1]));
  const total = cum[cum.length - 1];
  const radiusAt = (u) => {
    const d = u * total;
    for (let i = 1; i < cum.length; i++) {
      if (d <= cum[i]) return THREE.MathUtils.lerp(radii[i - 1], radii[i], (d - cum[i - 1]) / (cum[i] - cum[i - 1]));
    }
    return radii[radii.length - 1];
  };
  return { curve, length, radiusAt, side };
}

/**
 * 고리(ring)들을 이어 붙여 관 모양 메시를 만든다.
 * rings: { center, axisX, axisZ, rx, rz, ...임의 데이터 }
 * 각 고리의 정점은 각도 θ에서 center + axisX·cosθ·rx + axisZ·sinθ·rz.
 * θ는 -π/2(등 쪽)에서 시작해 한 바퀴 돌아 이음매가 등 뒤에 오게 한다. θ=π/2가 정면.
 * uvOf(ring, θ, position) → [u, v] 를 주면 텍스처 좌표도 만든다.
 * splitFrontBack이면 앞면(그룹 0)과 등면(그룹 1) 삼각형을 나눠 다른 재질을 쓸 수 있게 한다.
 */
export function ringsGeometry(rings, radial, uvOf, { splitFrontBack = false } = {}) {
  const positions = [];
  const uvs = [];
  const indices = [];
  const p = new THREE.Vector3();
  for (const ring of rings) {
    for (let j = 0; j <= radial; j++) {
      const theta = -Math.PI / 2 + (j / radial) * Math.PI * 2;
      p.copy(ring.center)
        .addScaledVector(ring.axisX, Math.cos(theta) * ring.rx)
        .addScaledVector(ring.axisZ, Math.sin(theta) * ring.rz);
      positions.push(p.x, p.y, p.z);
      if (uvOf) uvs.push(...uvOf(ring, theta, p));
    }
  }
  const stride = radial + 1;
  const back = [];
  for (let i = 0; i < rings.length - 1; i++) {
    for (let j = 0; j < radial; j++) {
      const a = i * stride + j;
      const b = a + stride;
      const isFront = j >= radial / 4 && j < (radial * 3) / 4; // θ ∈ [0, π]
      (splitFrontBack && !isFront ? back : indices).push(a, a + 1, b, b, a + 1, b + 1);
    }
  }
  const geo = new THREE.BufferGeometry();
  if (splitFrontBack) {
    geo.addGroup(0, indices.length, 0);
    geo.addGroup(indices.length, back.length, 1);
    indices.push(...back);
  }
  geo.setAttribute("position", new THREE.Float32BufferAttribute(positions, 3));
  if (uvOf) geo.setAttribute("uv", new THREE.Float32BufferAttribute(uvs, 2));
  geo.setIndex(indices);
  geo.computeVertexNormals();
  return geo;
}

const X = new THREE.Vector3(1, 0, 0);
const Z = new THREE.Vector3(0, 0, 1);

// 몸통 고리: y 위치와 반지름 함수로 만든다.
export function torsoRing(y, rx, rz, extra = {}) {
  return { center: new THREE.Vector3(0, y, 0), axisX: X, axisZ: Z, rx, rz, y, ...extra };
}

// 팔·다리 고리: 진행 방향에 수직인 단면. axisX는 몸 바깥쪽을 향한다.
export function limbRing(limb, u, radius, extra = {}) {
  // u < 0 이면 시작점에서 진행 방향 반대로 연장 (소매를 어깨 안쪽까지 덮을 때)
  const tangent = limb.curve.getTangentAt(Math.max(u, 0));
  const center = u >= 0 ? limb.curve.getPointAt(u) : limb.curve.getPointAt(0).addScaledVector(tangent, u * limb.length);
  const outward = new THREE.Vector3(-tangent.y, tangent.x, 0).normalize();
  if (Math.sign(outward.x) !== limb.side) outward.negate();
  const axisZ = new THREE.Vector3().crossVectors(tangent, outward).normalize();
  if (axisZ.z < 0) axisZ.negate();
  return { center, axisX: outward, axisZ, rx: radius, rz: radius, u, ...extra };
}

export function createMannequin() {
  const group = new THREE.Group();
  group.name = "mannequin";
  const material = new THREE.MeshStandardMaterial({ color: 0xe9e3da, roughness: 0.42, metalness: 0.02 });
  const add = (geo, mat = material) => {
    const mesh = new THREE.Mesh(geo, mat);
    mesh.castShadow = true;
    mesh.receiveShadow = true;
    group.add(mesh);
    return mesh;
  };

  // 몸통
  const torsoRings = torsoTable.filter((_, i) => i % 4 === 0).map((pt) => torsoRing(pt.y, pt.x, pt.z));
  add(ringsGeometry(torsoRings, 48));

  // 목과 머리
  const neck = add(new THREE.CylinderGeometry(0.05, 0.054, 0.14, 32));
  neck.position.set(0, 1.52, 0);
  const head = add(new THREE.SphereGeometry(1, 48, 32));
  head.scale.set(0.092, 0.118, 0.104);
  head.position.set(0, 1.645, 0.008);

  // 팔다리
  for (const side of [-1, 1]) {
    for (const limb of [armPath(side), legPath(side)]) {
      const rings = [];
      const steps = 40;
      for (let i = 0; i <= steps; i++) rings.push(limbRing(limb, i / steps, limb.radiusAt(i / steps)));
      add(ringsGeometry(rings, 28));
    }
    const arm = armPath(side);
    const hand = add(new THREE.SphereGeometry(1, 24, 16));
    hand.scale.set(0.026, 0.07, 0.042);
    hand.position.copy(arm.curve.getPointAt(1)).addScaledVector(arm.curve.getTangentAt(1), 0.055);
    hand.rotation.z = side * BODY.armAngle;

    const leg = legPath(side);
    const ankle = leg.curve.getPointAt(1);
    const foot = add(new THREE.CapsuleGeometry(0.036, 0.16, 8, 16));
    foot.rotation.x = Math.PI / 2;
    foot.position.set(ankle.x, 0.036, ankle.z + 0.05);
    const shin = add(new THREE.SphereGeometry(0.038, 16, 12));
    shin.position.copy(ankle);
  }
  return group;
}
