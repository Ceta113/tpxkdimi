// 브라우저에서 하는 실제 이미지 가공: 불러오기·배경 지우기·색 보정·무늬, 그리고
// Claude 분석 결과를 정리하거나(정규화·빠진 기준점 채우기) AI 없이 기준점을 추정하는 일.

export const UPPER = ["top", "outer", "dress"];
export const REQUIRED_POINTS = {
  top: ["neck_center", "shoulder_left", "shoulder_right", "armpit_left", "armpit_right", "hem_left", "hem_right"],
  pants: ["waist_left", "waist_right", "crotch", "hem_left_outer", "hem_left_inner", "hem_right_outer", "hem_right_inner"],
  skirt: ["waist_left", "waist_right", "hem_left", "hem_right"],
  hat: [],
  shoes: [],
};
REQUIRED_POINTS.outer = REQUIRED_POINTS.top;
REQUIRED_POINTS.dress = REQUIRED_POINTS.top;
export const CUFF_POINTS = ["cuff_left_outer", "cuff_left_inner", "cuff_right_outer", "cuff_right_inner"];

export function makeCanvas(w, h) {
  const c = document.createElement("canvas");
  c.width = w;
  c.height = h;
  return c;
}

export async function loadImageToCanvas(file, maxSide = 1024) {
  const url = URL.createObjectURL(file);
  try {
    const img = new Image();
    img.src = url;
    await img.decode();
    const k = Math.min(1, maxSide / Math.max(img.naturalWidth, img.naturalHeight));
    const c = makeCanvas(Math.round(img.naturalWidth * k), Math.round(img.naturalHeight * k));
    c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
    return c;
  } finally {
    URL.revokeObjectURL(url);
  }
}

// Claude에게 보낼 JPEG (투명 픽셀은 흰 배경으로)
export function canvasToPayload(canvas, maxSide = 1024) {
  const k = Math.min(1, maxSide / Math.max(canvas.width, canvas.height));
  const c = makeCanvas(Math.round(canvas.width * k), Math.round(canvas.height * k));
  const ctx = c.getContext("2d");
  ctx.fillStyle = "#fff";
  ctx.fillRect(0, 0, c.width, c.height);
  ctx.drawImage(canvas, 0, 0, c.width, c.height);
  const data = c.toDataURL("image/jpeg", 0.9).split(",")[1];
  return { data, mediaType: "image/jpeg", width: c.width, height: c.height };
}

const colorDist = (d, i, r, g, b) => Math.hypot(d[i] - r, d[i + 1] - g, d[i + 2] - b);

// 이미지 테두리 픽셀의 중간값 = 배경색 추정
function borderColor(d, w, h) {
  const rs = [], gs = [], bs = [];
  const take = (x, y) => {
    const i = (y * w + x) * 4;
    rs.push(d[i]);
    gs.push(d[i + 1]);
    bs.push(d[i + 2]);
  };
  for (let x = 0; x < w; x += 2) {
    take(x, 0);
    take(x, h - 1);
  }
  for (let y = 0; y < h; y += 2) {
    take(0, y);
    take(w - 1, y);
  }
  const median = (a) => a.sort((p, q) => p - q)[a.length >> 1];
  return [median(rs), median(gs), median(bs)];
}

/**
 * 배경을 투명하게 만든다.
 * - plain(단색 배경): 테두리에서 시작해 배경색과 비슷한 픽셀을 번져 나가며 지운다(flood fill).
 * - 아니면: Claude가 준 옷 외곽선 다각형(없으면 bbox) 바깥을 지운다.
 * outline, bbox는 0~1 정규화 좌표.
 */
export function removeBackground(src, { plain = true, tolerance = 60, outline = [], bbox = null } = {}) {
  const w = src.width;
  const h = src.height;
  const out = makeCanvas(w, h);
  const ctx = out.getContext("2d", { willReadFrequently: true });

  if (!plain) {
    ctx.beginPath();
    if (outline.length >= 3) {
      outline.forEach((p, i) => (i ? ctx.lineTo(p.x * w, p.y * h) : ctx.moveTo(p.x * w, p.y * h)));
    } else if (bbox) {
      ctx.rect(bbox.x * w, bbox.y * h, bbox.width * w, bbox.height * h);
    } else {
      ctx.rect(0, 0, w, h);
    }
    ctx.closePath();
    ctx.fill();
    ctx.globalCompositeOperation = "source-in";
    ctx.drawImage(src, 0, 0);
    ctx.globalCompositeOperation = "source-over";
    return out;
  }

  ctx.drawImage(src, 0, 0);
  const img = ctx.getImageData(0, 0, w, h);
  const d = img.data;
  const [br, bg, bb] = borderColor(d, w, h);
  const isBg = new Uint8Array(w * h);
  const queue = new Int32Array(w * h);
  let head = 0;
  let tail = 0;
  const seed = (p) => {
    if (!isBg[p] && colorDist(d, p * 4, br, bg, bb) < tolerance) {
      isBg[p] = 1;
      queue[tail++] = p;
    }
  };
  for (let x = 0; x < w; x++) {
    seed(x);
    seed((h - 1) * w + x);
  }
  for (let y = 0; y < h; y++) {
    seed(y * w);
    seed(y * w + w - 1);
  }
  while (head < tail) {
    const p = queue[head++];
    const x = p % w;
    const y = (p - x) / w;
    const neighbors = [x > 0 ? p - 1 : -1, x < w - 1 ? p + 1 : -1, y > 0 ? p - w : -1, y < h - 1 ? p + w : -1];
    for (const n of neighbors) {
      if (n < 0 || isBg[n]) continue;
      const fromBg = colorDist(d, n * 4, br, bg, bb);
      // 배경색에 가깝거나, 그림자처럼 바로 옆 배경 픽셀과 거의 같은 색이면 배경
      const fromPrev = colorDist(d, n * 4, d[p * 4], d[p * 4 + 1], d[p * 4 + 2]);
      if (fromBg < tolerance || (fromPrev < 10 && fromBg < tolerance * 1.8)) {
        isBg[n] = 1;
        queue[tail++] = n;
      }
    }
  }
  // 경계 1픽셀을 깎아 배경색 테두리(halo)를 없앤다
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const p = y * w + x;
      const edge =
        isBg[p] ||
        (x > 0 && isBg[p - 1] === 1) ||
        (x < w - 1 && isBg[p + 1] === 1) ||
        (y > 0 && isBg[p - w] === 1) ||
        (y < h - 1 && isBg[p + w] === 1);
      if (edge) d[p * 4 + 3] = 0;
    }
  }
  ctx.putImageData(img, 0, 0);
  return out;
}

// ── 색 보정 · 무늬 ───────────────────────────────────────────────────
export const DEFAULT_ADJUST = {
  hue: 0,
  saturation: 1,
  brightness: 1,
  contrast: 1,
  tint: { color: "#ff4d6d", strength: 0 },
  pattern: { type: "none", color: "#ffffff", scale: "medium", opacity: 0.8 },
};

export function normalizeAdjust(a) {
  const num = (v, lo, hi, dflt) => (Number.isFinite(v) ? Math.min(hi, Math.max(lo, v)) : dflt);
  const hex = (v, dflt) => (/^#[0-9a-f]{6}$/i.test(v ?? "") ? v : dflt);
  return {
    hue: num(a.hue, -180, 180, 0),
    saturation: num(a.saturation, 0, 2.5, 1),
    brightness: num(a.brightness, 0.3, 1.8, 1),
    contrast: num(a.contrast, 0.5, 1.8, 1),
    tint: { color: hex(a.tint?.color, "#ff4d6d"), strength: num(a.tint?.strength, 0, 1, 0) },
    pattern: {
      type: ["none", "stripes", "dots", "check"].includes(a.pattern?.type) ? a.pattern.type : "none",
      color: hex(a.pattern?.color, "#ffffff"),
      scale: ["small", "medium", "large"].includes(a.pattern?.scale) ? a.pattern.scale : "medium",
      opacity: num(a.pattern?.opacity, 0, 1, 0.8),
    },
  };
}

const hexToRgb = (hex) => [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16));

function rgbToHsl(r, g, b) {
  r /= 255;
  g /= 255;
  b /= 255;
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  const l = (max + min) / 2;
  if (max === min) return [0, 0, l];
  const dlt = max - min;
  const s = l > 0.5 ? dlt / (2 - max - min) : dlt / (max + min);
  let hh;
  if (max === r) hh = (g - b) / dlt + (g < b ? 6 : 0);
  else if (max === g) hh = (b - r) / dlt + 2;
  else hh = (r - g) / dlt + 4;
  return [hh * 60, s, l];
}

function hslToRgb(hh, s, l) {
  const c = (1 - Math.abs(2 * l - 1)) * s;
  const hp = (((hh % 360) + 360) % 360) / 60;
  const x = c * (1 - Math.abs((hp % 2) - 1));
  const [r, g, b] = hp < 1 ? [c, x, 0] : hp < 2 ? [x, c, 0] : hp < 3 ? [0, c, x] : hp < 4 ? [0, x, c] : hp < 5 ? [x, 0, c] : [c, 0, x];
  const m = l - c / 2;
  return [(r + m) * 255, (g + m) * 255, (b + m) * 255];
}

function patternHit(type, x, y, size) {
  if (type === "stripes") return Math.floor(y / size) % 2 === 0;
  if (type === "check") return (Math.floor(x / size) + Math.floor(y / size)) % 2 === 0;
  if (type === "dots") {
    const cx = (Math.floor(x / size) + 0.5) * size;
    const cy = (Math.floor(y / size) + 0.5) * size;
    return Math.hypot(x - cx, y - cy) < size * 0.28;
  }
  return false;
}

export function applyAdjustments(src, adj) {
  const a = normalizeAdjust(adj);
  const out = makeCanvas(src.width, src.height);
  const ctx = out.getContext("2d", { willReadFrequently: true });
  ctx.drawImage(src, 0, 0);
  const isIdentity =
    a.hue === 0 && a.saturation === 1 && a.brightness === 1 && a.contrast === 1 && a.tint.strength === 0 && a.pattern.type === "none";
  if (isIdentity) return out;

  const img = ctx.getImageData(0, 0, out.width, out.height);
  const d = img.data;
  const tint = hexToRgb(a.tint.color);
  const pcol = hexToRgb(a.pattern.color);
  const psize = out.width / { small: 45, medium: 24, large: 12 }[a.pattern.scale];
  for (let i = 0; i < d.length; i += 4) {
    if (d[i + 3] === 0) continue;
    let [hh, s, l] = rgbToHsl(d[i], d[i + 1], d[i + 2]);
    let [r, g, b] = hslToRgb(hh + a.hue, Math.min(1, s * a.saturation), l);
    const px = [r, g, b].map((c) => ((c * a.brightness - 128) * a.contrast + 128));
    if (a.tint.strength > 0) {
      const lum = (0.299 * px[0] + 0.587 * px[1] + 0.114 * px[2]) / 255;
      for (let k = 0; k < 3; k++) px[k] += (tint[k] * (0.3 + 0.95 * lum) - px[k]) * a.tint.strength;
    }
    if (a.pattern.type !== "none") {
      const p = i / 4;
      const x = p % out.width;
      if (patternHit(a.pattern.type, x, (p - x) / out.width, psize)) {
        for (let k = 0; k < 3; k++) px[k] += (pcol[k] - px[k]) * a.pattern.opacity;
      }
    }
    d[i] = px[0];
    d[i + 1] = px[1];
    d[i + 2] = px[2];
  }
  ctx.putImageData(img, 0, 0);
  return out;
}

// 투명 픽셀의 RGB를 가장 가까운 옷 픽셀 색으로 채운다.
// 텍스처를 확대·축소할 때 배경색(흰색)이 옷 가장자리에 번지지 않게 하고,
// opaque=true면 투명 부분까지 불투명하게 만들어 모자·신발처럼 통째로 칠할 때 쓴다.
export function bleedColors(src, { opaque = false } = {}) {
  const w = src.width;
  const h = src.height;
  const out = makeCanvas(w, h);
  const ctx = out.getContext("2d", { willReadFrequently: true });
  ctx.drawImage(src, 0, 0);
  const img = ctx.getImageData(0, 0, w, h);
  const d = img.data;
  const done = new Uint8Array(w * h);
  const queue = new Int32Array(w * h);
  let head = 0;
  let tail = 0;
  for (let p = 0; p < w * h; p++) {
    if (d[p * 4 + 3] > 0) {
      done[p] = 1;
      queue[tail++] = p;
    }
  }
  if (tail === 0) return out;
  while (head < tail) {
    const p = queue[head++];
    const x = p % w;
    for (const n of [x > 0 ? p - 1 : -1, x < w - 1 ? p + 1 : -1, p - w, p + w]) {
      if (n < 0 || n >= w * h || done[n]) continue;
      done[n] = 1;
      d[n * 4] = d[p * 4];
      d[n * 4 + 1] = d[p * 4 + 1];
      d[n * 4 + 2] = d[p * 4 + 2];
      queue[tail++] = n;
    }
  }
  if (opaque) for (let i = 3; i < d.length; i += 4) d[i] = 255;
  ctx.putImageData(img, 0, 0);
  return out;
}

// 등판용 이미지: 각 가로줄을 그 줄의 중간값 색으로 칠한다.
// 가로 줄무늬·색은 남고, 앞판의 로고·글씨는 사라진다(등에 거울처럼 비치지 않게).
export function makeBackCanvas(src) {
  const w = src.width;
  const h = src.height;
  const out = makeCanvas(w, h);
  const ctx = out.getContext("2d", { willReadFrequently: true });
  ctx.drawImage(src, 0, 0);
  const img = ctx.getImageData(0, 0, w, h);
  const d = img.data;
  const median = (a) => a.sort((p, q) => p - q)[a.length >> 1];
  for (let y = 0; y < h; y++) {
    const rs = [], gs = [], bs = [];
    for (let x = 0; x < w; x++) {
      const i = (y * w + x) * 4;
      if (d[i + 3] > 128) {
        rs.push(d[i]);
        gs.push(d[i + 1]);
        bs.push(d[i + 2]);
      }
    }
    if (!rs.length) continue;
    const [r, g, b] = [median(rs), median(gs), median(bs)];
    for (let x = 0; x < w; x++) {
      const i = (y * w + x) * 4;
      // 원래 밝기 변화를 조금 남겨 천의 질감을 살린다
      const diff = (d[i] + d[i + 1] + d[i + 2]) / 3 - (r + g + b) / 3;
      const shade = Math.abs(diff) < 25 ? diff * 0.3 : 0; // 크게 다른 픽셀(프린트)은 무시
      d[i] = r + shade;
      d[i + 1] = g + shade;
      d[i + 2] = b + shade;
    }
  }
  ctx.putImageData(img, 0, 0);
  return out;
}

// ── 마스크(투명도)에서 기준점 추정: AI 없이 쓰거나, AI가 빠뜨린 점을 채울 때 ─────────
function maskInfo(canvas) {
  const w = canvas.width;
  const h = canvas.height;
  const d = canvas.getContext("2d", { willReadFrequently: true }).getImageData(0, 0, w, h).data;
  const on = (x, y) => d[(y * w + x) * 4 + 3] > 128;
  let x0 = w, y0 = h, x1 = -1, y1 = -1;
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      if (on(x, y)) {
        if (x < x0) x0 = x;
        if (x > x1) x1 = x;
        if (y < y0) y0 = y;
        if (y > y1) y1 = y;
      }
    }
  }
  if (x1 < 0) {
    x0 = 0; y0 = 0; x1 = w - 1; y1 = h - 1;
  }
  const runsInRow = (y) => {
    y = Math.round(Math.min(h - 1, Math.max(0, y)));
    const runs = [];
    let start = -1;
    for (let x = 0; x <= w; x++) {
      const v = x < w && on(x, y);
      if (v && start < 0) start = x;
      if (!v && start >= 0) {
        if (x - start > 2) runs.push([start, x - 1]);
        start = -1;
      }
    }
    return runs;
  };
  const runsInCol = (x) => {
    x = Math.round(Math.min(w - 1, Math.max(0, x)));
    const runs = [];
    let start = -1;
    for (let y = 0; y <= h; y++) {
      const v = y < h && on(x, y);
      if (v && start < 0) start = y;
      if (!v && start >= 0) {
        if (y - start > 2) runs.push([start, y - 1]);
        start = -1;
      }
    }
    return runs;
  };
  return { w, h, x0, y0, x1, y1, runsInRow, runsInCol };
}

export function guessKeypoints(canvas, category) {
  const m = maskInfo(canvas);
  const bw = m.x1 - m.x0;
  const bh = m.y1 - m.y0;
  const P = {};
  const rowSpan = (y) => {
    const runs = m.runsInRow(y);
    return runs.length ? [runs[0][0], runs[runs.length - 1][1]] : [m.x0, m.x1];
  };
  if (UPPER.includes(category)) {
    const hemY = m.y1 - bh * 0.01;
    const [hl, hr] = rowSpan(hemY);
    const unit = hr - hl; // 밑단 폭을 기준 길이로
    const cx = (hl + hr) / 2;
    const topAtCenter = m.runsInCol(cx)[0]?.[0] ?? m.y0;
    P.neck_center = [cx, Math.min(topAtCenter, m.y0 + unit * 0.05)];
    P.shoulder_left = [hl + unit * 0.02, m.y0 + unit * 0.1];
    P.shoulder_right = [hr - unit * 0.02, m.y0 + unit * 0.1];
    P.armpit_left = [hl + unit * 0.03, m.y0 + unit * 0.45];
    P.armpit_right = [hr - unit * 0.03, m.y0 + unit * 0.45];
    P.hem_left = [hl, hemY];
    P.hem_right = [hr, hemY];
    // 몸판보다 옆으로 튀어나온 부분이 있으면 소매로 보고, 그 끝 열에서 소매단 두 점을 찾는다
    if (m.x0 < hl - unit * 0.06) {
      const col = m.runsInCol(m.x0 + 2)[0] ?? [m.y0 + unit * 0.2, m.y0 + unit * 0.4];
      P.cuff_left_outer = [m.x0, col[0]];
      P.cuff_left_inner = [m.x0 + unit * 0.04, col[1]];
    } else {
      P.cuff_left_outer = [hl - unit * 0.1, m.y0 + unit * 0.3];
      P.cuff_left_inner = [hl + unit * 0.02, m.y0 + unit * 0.55];
    }
    if (m.x1 > hr + unit * 0.06) {
      const col = m.runsInCol(m.x1 - 2)[0] ?? [m.y0 + unit * 0.2, m.y0 + unit * 0.4];
      P.cuff_right_outer = [m.x1, col[0]];
      P.cuff_right_inner = [m.x1 - unit * 0.04, col[1]];
    } else {
      P.cuff_right_outer = [hr + unit * 0.1, m.y0 + unit * 0.3];
      P.cuff_right_inner = [hr - unit * 0.02, m.y0 + unit * 0.55];
    }
  } else if (category === "pants" || category === "skirt") {
    const [wl, wr] = rowSpan(m.y0 + bh * 0.01);
    P.waist_left = [wl, m.y0 + bh * 0.01];
    P.waist_right = [wr, m.y0 + bh * 0.01];
    const hemY = m.y1 - bh * 0.01;
    const runs = m.runsInRow(hemY);
    if (category === "skirt") {
      const [hl, hr] = rowSpan(hemY);
      P.hem_left = [hl, hemY];
      P.hem_right = [hr, hemY];
    } else {
      const cx = (wl + wr) / 2;
      const left = runs.length >= 2 ? runs[0] : [m.x0, cx - bw * 0.03];
      const right = runs.length >= 2 ? runs[runs.length - 1] : [cx + bw * 0.03, m.x1];
      P.hem_left_outer = [left[0], hemY];
      P.hem_left_inner = [left[1], hemY];
      P.hem_right_inner = [right[0], hemY];
      P.hem_right_outer = [right[1], hemY];
      // 가운데 열을 허리부터 아래로 훑어 천이 처음 끊기는 곳 = 가랑이
      const col = m.runsInCol(cx);
      const crotchY = col.length ? col[0][1] : m.y0 + bh * 0.35;
      P.crotch = [cx, Math.min(crotchY, m.y0 + bh * 0.6)];
    }
  }
  const keypoints = {};
  for (const [name, [x, y]] of Object.entries(P)) keypoints[name] = { x: x / m.w, y: y / m.h };
  return {
    keypoints,
    bbox: { x: m.x0 / m.w, y: m.y0 / m.h, width: (m.x1 - m.x0) / m.w, height: (m.y1 - m.y0) / m.h },
  };
}

/**
 * Claude 분석 결과(픽셀 좌표) → 프로그램이 쓰는 형태(0~1 좌표)로 정리하고,
 * 빠지거나 이상한 기준점은 마스크에서 추정한 값으로 채운다.
 * raw: 분석 결과, size: 분석에 보낸 이미지 크기
 */
export function normalizeAnalysis(raw, size) {
  const nx = (v) => Math.min(1, Math.max(0, v / size.width));
  const ny = (v) => Math.min(1, Math.max(0, v / size.height));
  const keypoints = {};
  for (const k of raw.keypoints ?? []) {
    if (Number.isFinite(k.x) && Number.isFinite(k.y)) keypoints[k.name] = { x: nx(k.x), y: ny(k.y) };
  }
  const b = raw.bbox ?? {};
  const bbox =
    b.width > 0 && b.height > 0
      ? { x: nx(b.x), y: ny(b.y), width: nx(b.width), height: ny(b.height) }
      : null;
  return {
    ...raw,
    keypoints,
    bbox,
    outline: (raw.outline ?? []).filter((p) => Number.isFinite(p.x) && Number.isFinite(p.y)).map((p) => ({ x: nx(p.x), y: ny(p.y) })),
  };
}

export function fillMissingKeypoints(garment, maskCanvas) {
  const guess = guessKeypoints(maskCanvas, garment.category);
  const need = [...(REQUIRED_POINTS[garment.category] ?? [])];
  if (UPPER.includes(garment.category) && garment.sleeve !== "none") need.push(...CUFF_POINTS);
  for (const name of need) {
    if (!garment.keypoints[name] && guess.keypoints[name]) garment.keypoints[name] = guess.keypoints[name];
  }
  if (!garment.bbox) garment.bbox = guess.bbox;
}

// 체크무늬 배경 위에 투명 이미지를 그린 썸네일
export function thumbnail(src, size = 96) {
  const c = makeCanvas(size, size);
  const ctx = c.getContext("2d");
  ctx.fillStyle = "#f3efe9";
  ctx.fillRect(0, 0, size, size);
  const k = Math.min(size / src.width, size / src.height) * 0.92;
  const w = src.width * k;
  const h = src.height * k;
  ctx.drawImage(src, (size - w) / 2, (size - h) / 2, w, h);
  return c.toDataURL("image/png");
}
