// 옷 사진 + 기준점 → 마네킹에 맞춘 3D 옷 메시.
//
// 핵심 아이디어: 몸에 맞는 관(tube) 모양 메시를 만들고, 각 정점이 사진의 어느 픽셀을
// 가져올지(UV)를 기준점으로 정한다. 예를 들어 상의 몸판은 "어깨 두 점 ~ 밑단 두 점"이 이루는
// 사각형에, 소매는 "어깨·겨드랑이 ~ 소매끝 두 점" 사각형에 대응시킨다.
// 배경을 지운 투명 픽셀은 alphaTest로 잘려 나가므로, 메시를 넉넉하게 만들어도
// 실제 보이는 모양은 사진 속 옷의 실루엣을 따라간다.
import * as THREE from "three";
import { BODY, armPath, coverRadiusAt, legPath, limbRing, ringsGeometry, torsoRadiusAt, torsoRing } from "./mannequin.js";

// 옷 종류별 몸에서 띄우는 거리(겹쳐 입을 때 바깥 옷이 더 멀리)
const OFFSET = { top: 0.014, outer: 0.03, dress: 0.015, pants: 0.01, skirt: 0.012 };
const FIT_EXTRA = { tight: 0, regular: 0.005, loose: 0.013, oversized: 0.025 };

const clamp = THREE.MathUtils.clamp;
const lerp = THREE.MathUtils.lerp;
const lerp2 = (a, b, t) => ({ x: lerp(a.x, b.x, t), y: lerp(a.y, b.y, t) });
const mid = (a, b) => lerp2(a, b, 0.5);
// (h, t) ∈ [0,1]² 를 사각형 tl-tr-br-bl 위의 점으로 (t가 범위를 벗어나면 연장)
const bilinear = (tl, tr, br, bl, h, t) => lerp2(lerp2(tl, tr, h), lerp2(bl, br, h), t);
const toUV = (p) => [p.x, 1 - p.y];

// 옷 가장자리 픽셀은 반투명·경계라 살짝 안쪽을 쓴다 (옆선에 틈이 생기지 않게)
const inset = (h) => 0.02 + 0.96 * h;

// 몸통 고리의 정점 각도 → 사진에서의 가로 위치(0=왼쪽 끝, 1=오른쪽 끝). 등판은 앞판을 좌우 대칭으로 사용.
function wrapParam(theta) {
  let phi = theta - Math.PI / 2;
  if (Math.abs(phi) > Math.PI / 2) phi = Math.sign(phi) * Math.PI - phi;
  return inset(0.5 - phi / Math.PI);
}
// 팔·다리 고리의 정점 각도 → 0(바깥쪽 선) ~ 1(안쪽 선)
function limbParam(theta) {
  const psi = ((theta % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI);
  return inset(psi <= Math.PI ? psi / Math.PI : (2 * Math.PI - psi) / Math.PI);
}

// 모자·신발은 사진을 통째로 칠하고(불투명), 나머지는 배경을 지운 모양대로 잘라 낸다.
export const SOLID_CATEGORIES = ["hat", "shoes"];

function makeMaterial(texture, solid) {
  return new THREE.MeshStandardMaterial({
    map: texture,
    alphaTest: solid ? 0 : 0.5,
    side: THREE.DoubleSide,
    roughness: 0.82,
    metalness: 0,
  });
}

function makeMesh(geometry, materials, solid) {
  const mesh = new THREE.Mesh(geometry, geometry.groups.length ? materials : materials[0]);
  mesh.castShadow = true;
  mesh.receiveShadow = true;
  if (!solid) {
    // 투명하게 잘린 부분은 그림자도 지지 않도록
    mesh.customDepthMaterial = new THREE.MeshDepthMaterial({
      depthPacking: THREE.RGBADepthPacking,
      map: materials[0].map,
      alphaTest: 0.5,
    });
  }
  return mesh;
}

/**
 * garment: { category, fit, sleeve, width, height, keypoints: {이름: {x,y} (0~1)}, bbox: {x,y,width,height} (0~1) }
 * textures: { front, back? } 배경이 지워진 THREE.Texture (back은 등판용, 없으면 front를 씀)
 */
export function buildGarmentMesh(garment, textures) {
  const builders = { top: buildUpper, outer: buildUpper, dress: buildUpper, pants: buildPants, skirt: buildSkirt, hat: buildHat, shoes: buildShoes };
  const build = builders[garment.category];
  const group = new THREE.Group();
  if (!build) return group;
  const solid = SOLID_CATEGORIES.includes(garment.category);
  const front = makeMaterial(textures.front, solid);
  const back = textures.back ? makeMaterial(textures.back, solid) : front;
  for (const geometry of build(garment)) group.add(makeMesh(geometry, [front, back], solid));
  return group;
}

// 기준점을 픽셀 좌표로 (길이 비율 계산용)
function pixelPoints(g) {
  const out = {};
  for (const [name, p] of Object.entries(g.keypoints)) out[name] = { x: p.x * g.width, y: p.y * g.height };
  return out;
}
const dist = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);
const toNorm = (g, p) => ({ x: p.x / g.width, y: p.y / g.height });

// ── 상의 · 아우터 · 원피스 ─────────────────────────────────────────────
function buildUpper(g) {
  const P = pixelPoints(g);
  const N = g.keypoints;
  const scale = BODY.shoulderWidth / Math.max(dist(P.shoulder_left, P.shoulder_right), 1); // 픽셀 → 미터
  const shoulderMidY = (P.shoulder_left.y + P.shoulder_right.y) / 2;
  const hemMidY = (P.hem_left.y + P.hem_right.y) / 2;
  const isDress = g.category === "dress";
  const length = (hemMidY - shoulderMidY) * scale;
  const hemY = clamp(BODY.shoulderY - length, isDress ? 0.12 : 0.62, 1.2);
  const off = OFFSET[g.category] + (FIT_EXTRA[g.fit] ?? 0.005);

  // 사진 속 옷을 평평하게 놓았을 때 폭 = 입었을 때 둘레의 절반 → 헐렁함/퍼짐 계산
  const armpitFlat = dist(P.armpit_left, P.armpit_right) * scale;
  const hemFlat = dist(P.hem_left, P.hem_right) * scale;
  const maxSpread = isDress ? 2.6 : 1.45;

  // 목 위쪽(어깨선보다 위) 고리가 사진에서 얼마나 위를 가리킬지: 목둘레 중앙점 기준
  const neckLift = N.neck_center
    ? Math.max((shoulderMidY - P.neck_center.y) / (hemMidY - shoulderMidY), 0.03) * 1.15
    : 0.1;

  const rings = [];
  const steps = 64;
  for (let i = 0; i <= steps; i++) {
    const y = lerp(BODY.neckTopY, hemY, i / steps);
    const base = y > BODY.shoulderY ? torsoRadiusAt(y) : coverRadiusAt(y);
    let rx = base.rx + off;
    let rz = base.rz + off;
    if (y < BODY.armpitY) {
      const f = clamp((BODY.armpitY - y) / (BODY.armpitY - hemY), 0, 1);
      const flat = lerp(armpitFlat, hemFlat, f);
      let k = clamp((2 * flat) / (Math.PI * (rx + rz)), 1, maxSpread);
      k = lerp(1, k, THREE.MathUtils.smoothstep(f, 0, 0.3));
      rx *= k;
      rz *= 1 + (k - 1) * 0.85;
    }
    rings.push(torsoRing(y, rx, rz));
  }
  const shoulderRx = torsoRadiusAt(BODY.shoulderY).rx + off;
  // 몸판은 두 칸으로 나눠 매핑: 어깨선~겨드랑이선(진동 둘레), 겨드랑이선~밑단
  const armpitY = Math.max(BODY.armpitY, hemY + 0.05);
  const upperQuad = [N.shoulder_left, N.shoulder_right, N.armpit_right, N.armpit_left];
  const lowerQuad = [N.armpit_left, N.armpit_right, N.hem_right, N.hem_left];
  const torso = ringsGeometry(rings, 64, (ring, theta) => {
    let h = wrapParam(theta);
    if (ring.y > BODY.shoulderY) {
      h = 0.5 + (h - 0.5) * Math.min(ring.rx / shoulderRx, 1);
      const t = (-neckLift * (ring.y - BODY.shoulderY)) / (BODY.neckTopY - BODY.shoulderY);
      // 어깨선 위(목 부분)는 어깨~밑단 방향으로 연장해 목둘레를 가져온다
      return toUV(bilinear(N.shoulder_left, N.shoulder_right, N.hem_right, N.hem_left, h, t));
    }
    if (ring.y > armpitY) {
      return toUV(bilinear(...upperQuad, h, (BODY.shoulderY - ring.y) / (BODY.shoulderY - armpitY)));
    }
    return toUV(bilinear(...lowerQuad, h, (armpitY - ring.y) / (armpitY - hemY)));
  }, { splitFrontBack: true });
  const parts = [torso];

  if (g.sleeve !== "none") {
    for (const [side, key] of [[-1, "left"], [1, "right"]]) {
      const S = N[`shoulder_${key}`];
      const A = N[`armpit_${key}`];
      const CO = N[`cuff_${key}_outer`];
      const CI = N[`cuff_${key}_inner`];
      if (!S || !A || !CO || !CI) continue;
      parts.push(buildSleeve(g, side, scale, off, { S, A, CO, CI }));
    }
  }
  return parts;
}

function buildSleeve(g, side, scale, off, { S, A, CO, CI }) {
  const px = (p) => ({ x: p.x * g.width, y: p.y * g.height });
  const arm = armPath(side);
  const sleeveLen = clamp(dist(mid(px(S), px(A)), mid(px(CO), px(CI))) * scale, 0.04, arm.length);
  const topFlat = dist(px(S), px(A)) * scale;
  const cuffFlat = dist(px(CO), px(CI)) * scale;
  const u0 = -0.035 / arm.length;
  const u1 = sleeveLen / arm.length;
  const rings = [];
  const steps = 28;
  for (let i = 0; i <= steps; i++) {
    const u = lerp(u0, u1, i / steps);
    const f = (u * arm.length) / sleeveLen;
    const radius = clamp(Math.max(arm.radiusAt(Math.max(u, 0)) + off, lerp(topFlat, cuffFlat, f) / Math.PI), 0, 0.12);
    rings.push(limbRing(arm, u, radius, { f }));
  }
  return ringsGeometry(rings, 32, (ring, theta) => {
    const a = limbParam(theta); // 0 = 바깥(어깨) 선, 1 = 안쪽(겨드랑이) 선
    return toUV(bilinear(S, A, CI, CO, a, ring.f));
  });
}

// ── 바지 ────────────────────────────────────────────────────────────
function buildPants(g) {
  const P = pixelPoints(g);
  const N = g.keypoints;
  const waistFlat = dist(P.waist_left, P.waist_right);
  const bodyWaistHalfCirc = 0.39; // 바지 허리 높이에서 몸 둘레의 절반 (m)
  const scale = bodyWaistHalfCirc / Math.max(waistFlat, 1);
  const waistMidY = (P.waist_left.y + P.waist_right.y) / 2;
  const crotchWorldY = 0.81;
  const rise = (P.crotch.y - waistMidY) * scale;
  const waistY = clamp(crotchWorldY + rise, 0.95, 1.12);
  const hemMidY = (P.hem_left_outer.y + P.hem_left_inner.y + P.hem_right_outer.y + P.hem_right_inner.y) / 4;
  const legLen = (hemMidY - P.crotch.y) * scale;
  const hemY = clamp(crotchWorldY - legLen, 0.03, 0.74);
  const off = OFFSET.pants + (FIT_EXTRA[g.fit] ?? 0.005);

  // 사진에서 가랑이 높이의 바깥 옆선 위치
  const crotchFrac = (P.crotch.y - waistMidY) / Math.max(hemMidY - waistMidY, 1);
  const outerAtCrotch = {
    left: lerp2(N.waist_left, N.hem_left_outer, crotchFrac),
    right: lerp2(N.waist_right, N.hem_right_outer, crotchFrac),
  };

  // 엉덩이 부분 (허리 ~ 가랑이)
  const hipRings = [];
  const hipBottom = crotchWorldY - 0.02;
  for (let i = 0; i <= 20; i++) {
    const y = lerp(waistY, hipBottom, i / 20);
    const base = coverRadiusAt(y);
    hipRings.push(torsoRing(y, base.rx + off, base.rz + off));
  }
  const hip = ringsGeometry(hipRings, 64, (ring, theta) => {
    const t = (waistY - ring.y) / (waistY - crotchWorldY);
    return toUV(bilinear(N.waist_left, N.waist_right, outerAtCrotch.right, outerAtCrotch.left, wrapParam(theta), t));
  });
  const parts = [hip];

  // 다리 두 개
  for (const [side, key] of [[-1, "left"], [1, "right"]]) {
    const leg = legPath(side);
    const yToU = (y) => clamp((leg.curve.getPointAt(0).y - y) / (leg.curve.getPointAt(0).y - leg.curve.getPointAt(1).y), 0, 1);
    const uTop = yToU(crotchWorldY + 0.04);
    const uHem = yToU(hemY);
    const topFlat = dist(
      { x: outerAtCrotch[key].x * g.width, y: outerAtCrotch[key].y * g.height },
      P.crotch,
    ) * scale;
    const hemFlat = dist(P[`hem_${key}_outer`], P[`hem_${key}_inner`]) * scale;
    const rings = [];
    for (let i = 0; i <= 36; i++) {
      const u = lerp(uTop, uHem, i / 36);
      const y = leg.curve.getPointAt(u).y;
      const f = (crotchWorldY - y) / (crotchWorldY - hemY);
      const radius = clamp(Math.max(leg.radiusAt(u) + off, lerp(topFlat, hemFlat, clamp(f, 0, 1)) / Math.PI), 0, 0.13);
      rings.push(limbRing(leg, u, radius, { f }));
    }
    const quad = [outerAtCrotch[key], N.crotch, N[`hem_${key}_inner`], N[`hem_${key}_outer`]];
    parts.push(ringsGeometry(rings, 40, (ring, theta) => toUV(bilinear(...quad, limbParam(theta), ring.f))));
  }
  return parts;
}

// ── 치마 ────────────────────────────────────────────────────────────
function buildSkirt(g) {
  const P = pixelPoints(g);
  const N = g.keypoints;
  const scale = 0.37 / Math.max(dist(P.waist_left, P.waist_right), 1);
  const waistY = 1.04;
  const length = ((P.hem_left.y + P.hem_right.y) / 2 - (P.waist_left.y + P.waist_right.y) / 2) * scale;
  const hemY = clamp(waistY - length, 0.08, 0.9);
  const off = OFFSET.skirt + (FIT_EXTRA[g.fit] ?? 0.005);
  const waistFlat = dist(P.waist_left, P.waist_right) * scale;
  const hemFlat = dist(P.hem_left, P.hem_right) * scale;
  const rings = [];
  for (let i = 0; i <= 40; i++) {
    const y = lerp(waistY, hemY, i / 40);
    const base = coverRadiusAt(y);
    let rx = base.rx + off;
    let rz = base.rz + off;
    const flat = lerp(waistFlat, hemFlat, i / 40);
    const k = clamp((2 * flat) / (Math.PI * (rx + rz)), 1, 2.8);
    rx *= k;
    rz *= 1 + (k - 1) * 0.85;
    rings.push(torsoRing(y, rx, rz));
  }
  const geo = ringsGeometry(rings, 64, (ring, theta) =>
    toUV(bilinear(N.waist_left, N.waist_right, N.hem_right, N.hem_left, wrapParam(theta), (waistY - ring.y) / (waistY - hemY))),
  );
  return [geo];
}

// ── 모자 ────────────────────────────────────────────────────────────
// 머리를 덮는 반구에 사진을 정면에서 투영한다.
function buildHat(g) {
  const b = g.bbox;
  const center = new THREE.Vector3(0, 1.645, 0.008);
  const r = { x: 0.105, y: 0.13, z: 0.117 };
  const bottomY = 1.6;
  const topY = center.y + r.y;
  const geo = new THREE.SphereGeometry(1, 48, 24, 0, Math.PI * 2, 0, Math.PI * 0.62);
  geo.scale(r.x, r.y, r.z);
  geo.translate(center.x, center.y, center.z);
  const pos = geo.attributes.position;
  const uv = geo.attributes.uv;
  for (let i = 0; i < pos.count; i++) {
    const nx = b.x + (pos.getX(i) / (2 * r.x) + 0.5) * b.width;
    const ny = b.y + (1 - (pos.getY(i) - bottomY) / (topY - bottomY)) * b.height;
    uv.setXY(i, nx, 1 - ny);
  }
  const parts = [geo];
  if (b.width / Math.max(b.height, 1e-6) > (g.height / g.width) * 1.4) {
    // 사진이 아주 넓으면 챙 있는 모자로 보고 챙을 추가 (챙 색은 사진 아래쪽 줄에서 가져옴)
    const brim = new THREE.RingGeometry(0.1, 0.2, 48, 1);
    brim.rotateX(-Math.PI / 2);
    brim.translate(0, 1.615, 0.01);
    const bp = brim.attributes.position;
    const buv = brim.attributes.uv;
    for (let i = 0; i < bp.count; i++) {
      buv.setXY(i, b.x + (bp.getX(i) / 0.4 + 0.5) * b.width, 1 - (b.y + b.height * 0.93));
    }
    parts.push(brim);
  }
  return parts;
}

// ── 신발 ────────────────────────────────────────────────────────────
// 신발 사진은 보통 옆모습이라, 발의 옆면(z-y 평면)으로 투영한다.
// 양발 모두 같은 매핑을 쓰면 바깥쪽에서 볼 때 각각 자연스러운 방향이 된다.
function buildShoes(g) {
  const b = g.bbox;
  const parts = [];
  for (const side of [-1, 1]) {
    const ankle = legPath(side).curve.getPointAt(1);
    const r = { x: 0.05, y: 0.06, z: 0.14 };
    const c = new THREE.Vector3(ankle.x, 0.045, ankle.z + 0.05);
    const geo = new THREE.SphereGeometry(1, 40, 20);
    geo.scale(r.x, r.y, r.z);
    geo.translate(c.x, c.y, c.z);
    const pos = geo.attributes.position;
    const uv = geo.attributes.uv;
    for (let i = 0; i < pos.count; i++) {
      const along = (pos.getZ(i) - c.z) / (2 * r.z) + 0.5; // 0 = 뒤꿈치, 1 = 앞코
      if (pos.getY(i) < 0.004) pos.setY(i, 0.004); // 밑창은 평평하게
      const up = clamp(pos.getY(i) / (c.y + r.y), 0, 1);
      // 사진 속 앞코 방향에 맞춰 앞코 쪽 정점이 앞코 픽셀을 가져오게 한다
      const u = g.facing === "right" ? along : 1 - along;
      uv.setXY(i, b.x + u * b.width, 1 - (b.y + (1 - up) * b.height));
    }
    geo.computeVertexNormals();
    parts.push(geo);
  }
  return parts;
}

// 어떤 옷이 어느 자리를 차지하는지 (원피스는 상의·하의 자리를 함께 차지)
export const SLOTS = {
  top: ["top"],
  outer: ["outer"],
  dress: ["top", "bottom"],
  pants: ["bottom"],
  skirt: ["bottom"],
  hat: ["hat"],
  shoes: ["shoes"],
};

export { toNorm };
