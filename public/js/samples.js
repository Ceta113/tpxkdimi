// 체험용 샘플 옷: 캔버스에 직접 그린 "옷 사진"과, Claude 분석 결과와 같은 형식의 정답 데이터.
// 사진이 없거나 API 키가 없어도 프로그램 흐름을 그대로 체험할 수 있다.
import { makeCanvas } from "./imageproc.js";

function sheet(w, h) {
  const c = makeCanvas(w, h);
  const ctx = c.getContext("2d");
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, w, h);
  return { c, ctx };
}

function poly(ctx, pts) {
  ctx.beginPath();
  pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)));
  ctx.closePath();
}

// 천 느낌을 내는 잔 노이즈
function grain(ctx, w, h, amount = 14) {
  const img = ctx.getImageData(0, 0, w, h);
  const d = img.data;
  for (let i = 0; i < d.length; i += 4) {
    if (d[i] > 245 && d[i + 1] > 245 && d[i + 2] > 245) continue; // 배경은 그대로
    const n = (Math.random() - 0.5) * amount;
    d[i] += n;
    d[i + 1] += n;
    d[i + 2] += n;
  }
  ctx.putImageData(img, 0, 0);
}

const kp = (obj) => Object.entries(obj).map(([name, [x, y]]) => ({ name, x, y }));
const base = (w, h, extra) => ({
  fit: "regular",
  sleeve: "none",
  facing: "none",
  view: "front_flat",
  background: { isPlain: true, color: "#ffffff" },
  outline: [],
  tips: "",
  ...extra,
});

function tshirt() {
  const { c, ctx } = sheet(640, 640);
  const P = {
    neck_center: [320, 72],
    shoulder_left: [168, 102],
    shoulder_right: [472, 102],
    armpit_left: [192, 228],
    armpit_right: [448, 228],
    cuff_left_outer: [70, 236],
    cuff_left_inner: [128, 292],
    cuff_right_outer: [570, 236],
    cuff_right_inner: [512, 292],
    hem_left: [196, 596],
    hem_right: [444, 596],
  };
  const body = [
    [255, 72], [385, 72], P.shoulder_right, P.cuff_right_outer, P.cuff_right_inner, P.armpit_right,
    P.hem_right, P.hem_left, P.armpit_left, P.cuff_left_inner, P.cuff_left_outer, P.shoulder_left,
  ];
  ctx.fillStyle = "#e8695b";
  poly(ctx, body);
  ctx.fill();
  // 앞 목둘레 (파인 부분은 배경색)
  ctx.fillStyle = "#ffffff";
  ctx.beginPath();
  ctx.moveTo(255, 70);
  ctx.quadraticCurveTo(320, 140, 385, 70);
  ctx.closePath();
  ctx.fill();
  ctx.strokeStyle = "#c9493d";
  ctx.lineWidth = 9;
  ctx.beginPath();
  ctx.moveTo(258, 76);
  ctx.quadraticCurveTo(320, 138, 382, 76);
  ctx.stroke();
  // 가슴 줄무늬와 로고
  ctx.fillStyle = "#fff4e6";
  ctx.fillRect(196, 300, 248, 26);
  ctx.fillRect(196, 340, 248, 10);
  ctx.fillStyle = "#2b2d42";
  ctx.font = "bold 54px sans-serif";
  ctx.textAlign = "center";
  ctx.fillText("DIMI", 320, 430);
  // 소매단
  ctx.strokeStyle = "#c9493d";
  ctx.lineWidth = 8;
  ctx.beginPath();
  ctx.moveTo(78, 244);
  ctx.lineTo(128, 286);
  ctx.moveTo(562, 244);
  ctx.lineTo(512, 286);
  ctx.stroke();
  grain(ctx, 640, 640);
  return {
    canvas: c,
    analysis: base(640, 640, {
      category: "top",
      name: "코랄 반팔 티셔츠",
      description: "가슴에 줄무늬와 DIMI 로고가 있는 면 반팔 티셔츠",
      sleeve: "short",
      dominantColors: ["#e8695b", "#fff4e6"],
      bbox: { x: 70, y: 70, width: 500, height: 528 },
      keypoints: kp(P),
    }),
  };
}

function jeans() {
  const { c, ctx } = sheet(640, 800);
  const P = {
    waist_left: [202, 60],
    waist_right: [438, 60],
    crotch: [320, 318],
    hem_left_outer: [176, 762],
    hem_left_inner: [304, 762],
    hem_right_inner: [336, 762],
    hem_right_outer: [464, 762],
  };
  const shape = [P.waist_left, P.waist_right, [468, 240], P.hem_right_outer, P.hem_right_inner, P.crotch, P.hem_left_inner, P.hem_left_outer, [172, 240]];
  ctx.fillStyle = "#3d5f93";
  poly(ctx, shape);
  ctx.fill();
  ctx.fillStyle = "#34527f";
  ctx.fillRect(202, 60, 236, 34); // 허리 밴드
  ctx.strokeStyle = "#d9a441";
  ctx.lineWidth = 3;
  ctx.setLineDash([8, 6]);
  ctx.beginPath();
  ctx.moveTo(206, 98);
  ctx.lineTo(434, 98);
  ctx.moveTo(320, 98);
  ctx.lineTo(320, 250); // 앞 지퍼선
  ctx.moveTo(214, 104);
  ctx.quadraticCurveTo(250, 170, 210, 200); // 주머니
  ctx.moveTo(426, 104);
  ctx.quadraticCurveTo(390, 170, 430, 200);
  ctx.moveTo(182, 740);
  ctx.lineTo(298, 740);
  ctx.moveTo(342, 740);
  ctx.lineTo(458, 740);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = "#c08a2d";
  ctx.beginPath();
  ctx.arc(320, 77, 7, 0, Math.PI * 2);
  ctx.fill();
  // 무릎 쪽 워싱 (바지 안쪽에만)
  ctx.save();
  poly(ctx, shape);
  ctx.clip();
  const fade = ctx.createRadialGradient(240, 470, 10, 240, 470, 90);
  fade.addColorStop(0, "rgba(160,190,230,0.45)");
  fade.addColorStop(1, "rgba(160,190,230,0)");
  ctx.fillStyle = fade;
  ctx.fillRect(150, 380, 180, 180);
  const fade2 = ctx.createRadialGradient(400, 470, 10, 400, 470, 90);
  fade2.addColorStop(0, "rgba(160,190,230,0.45)");
  fade2.addColorStop(1, "rgba(160,190,230,0)");
  ctx.fillStyle = fade2;
  ctx.fillRect(310, 380, 180, 180);
  ctx.restore();
  grain(ctx, 640, 800, 22);
  return {
    canvas: c,
    analysis: base(640, 800, {
      category: "pants",
      name: "연청 일자 청바지",
      description: "무릎에 워싱이 들어간 일자핏 데님 팬츠",
      dominantColors: ["#3d5f93"],
      bbox: { x: 172, y: 60, width: 296, height: 702 },
      keypoints: kp(P),
    }),
  };
}

function skirt() {
  const { c, ctx } = sheet(640, 600);
  const P = { waist_left: [222, 70], waist_right: [418, 70], hem_left: [104, 520], hem_right: [536, 520] };
  poly(ctx, [P.waist_left, P.waist_right, P.hem_right, [320, 540], P.hem_left]);
  ctx.save();
  ctx.clip();
  ctx.fillStyle = "#2f6b4f";
  ctx.fillRect(0, 0, 640, 600);
  // 타탄 체크
  for (let i = 0; i < 640; i += 64) {
    ctx.fillStyle = "rgba(20,40,70,0.45)";
    ctx.fillRect(i, 0, 26, 600);
    ctx.fillRect(0, i, 640, 26);
    ctx.fillStyle = "rgba(230,190,60,0.7)";
    ctx.fillRect(i + 40, 0, 3, 600);
    ctx.fillRect(0, i + 40, 640, 3);
  }
  ctx.restore();
  ctx.fillStyle = "#1f3f30";
  ctx.fillRect(222, 70, 196, 26);
  grain(ctx, 640, 600);
  return {
    canvas: c,
    analysis: base(640, 600, {
      category: "skirt",
      name: "그린 체크 플레어 스커트",
      description: "노란 선이 들어간 타탄 체크 A라인 스커트",
      dominantColors: ["#2f6b4f", "#e6be3c"],
      bbox: { x: 104, y: 70, width: 432, height: 470 },
      keypoints: kp(P),
    }),
  };
}

function beanie() {
  const { c, ctx } = sheet(480, 480);
  ctx.fillStyle = "#f2c14e";
  ctx.beginPath();
  ctx.ellipse(240, 300, 150, 190, 0, Math.PI, 0);
  ctx.closePath();
  ctx.fill();
  ctx.fillStyle = "#e0a92e";
  ctx.fillRect(90, 290, 300, 90); // 접은 단
  ctx.strokeStyle = "rgba(150,100,20,0.35)";
  ctx.lineWidth = 3;
  for (let x = 100; x < 390; x += 14) {
    ctx.beginPath();
    ctx.moveTo(x, 294);
    ctx.lineTo(x, 376);
    ctx.stroke();
  }
  ctx.fillStyle = "#fff8e8";
  ctx.beginPath();
  ctx.arc(240, 108, 34, 0, Math.PI * 2);
  ctx.fill();
  grain(ctx, 480, 480);
  return {
    canvas: c,
    analysis: base(480, 480, {
      category: "hat",
      name: "머스터드 비니",
      description: "방울이 달린 골지 니트 비니",
      dominantColors: ["#f2c14e"],
      bbox: { x: 90, y: 74, width: 300, height: 306 },
      keypoints: [],
    }),
  };
}

function sneakers() {
  const { c, ctx } = sheet(640, 320);
  // 앞코가 왼쪽을 향한 옆모습
  poly(ctx, [[40, 250], [60, 200], [150, 160], [260, 120], [360, 60], [520, 50], [600, 110], [600, 250]]);
  ctx.fillStyle = "#4361ee";
  ctx.fill();
  ctx.fillStyle = "#f8f9fa";
  ctx.fillRect(36, 250, 568, 34); // 밑창
  ctx.fillStyle = "#ffffff";
  ctx.beginPath();
  ctx.moveTo(240, 230);
  ctx.quadraticCurveTo(380, 150, 520, 160);
  ctx.lineTo(520, 190);
  ctx.quadraticCurveTo(380, 185, 260, 235);
  ctx.closePath();
  ctx.fill();
  ctx.fillStyle = "#ef476f";
  ctx.fillRect(540, 70, 50, 120); // 뒤꿈치 탭
  grain(ctx, 640, 320, 10);
  return {
    canvas: c,
    analysis: base(640, 320, {
      category: "shoes",
      name: "블루 스니커즈",
      description: "흰 밑창에 흰색 스우시 포인트가 있는 로우탑 스니커즈",
      facing: "left",
      view: "side",
      dominantColors: ["#4361ee", "#ffffff"],
      bbox: { x: 36, y: 50, width: 568, height: 234 },
      keypoints: [],
    }),
  };
}

export const SAMPLES = [
  { id: "tshirt", label: "반팔 티셔츠", make: tshirt },
  { id: "jeans", label: "청바지", make: jeans },
  { id: "skirt", label: "체크 스커트", make: skirt },
  { id: "beanie", label: "비니", make: beanie },
  { id: "sneakers", label: "스니커즈", make: sneakers },
];
