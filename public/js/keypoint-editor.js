// 2D 기준점 편집기: 옷 사진 위의 점을 끌어서 Claude가 찍은 위치를 바로잡는다.
import { CUFF_POINTS, REQUIRED_POINTS, UPPER } from "./imageproc.js";

const LABELS = {
  neck_center: "목",
  shoulder_left: "어깨",
  shoulder_right: "어깨",
  armpit_left: "겨드랑이",
  armpit_right: "겨드랑이",
  cuff_left_outer: "소매끝 바깥",
  cuff_left_inner: "소매끝 안",
  cuff_right_outer: "소매끝 바깥",
  cuff_right_inner: "소매끝 안",
  hem_left: "밑단",
  hem_right: "밑단",
  waist_left: "허리",
  waist_right: "허리",
  crotch: "가랑이",
  hem_left_outer: "밑단 바깥",
  hem_left_inner: "밑단 안",
  hem_right_outer: "밑단 바깥",
  hem_right_inner: "밑단 안",
};

// 함께 선으로 이어 그릴 점들 (사각형 매핑 영역이 보이도록)
const OUTLINES = {
  upper: [["shoulder_left", "shoulder_right", "hem_right", "hem_left"], ["shoulder_left", "armpit_left", "cuff_left_inner", "cuff_left_outer"], ["shoulder_right", "armpit_right", "cuff_right_inner", "cuff_right_outer"]],
  pants: [["waist_left", "waist_right", "hem_right_outer", "hem_right_inner", "crotch", "hem_left_inner", "hem_left_outer"]],
  skirt: [["waist_left", "waist_right", "hem_right", "hem_left"]],
};

const colorFor = (name) =>
  name.includes("cuff") ? "#7b61ff" : name.includes("hem") ? "#ff6b35" : name.includes("armpit") || name === "crotch" ? "#06a77d" : "#1b7ce0";

export class KeypointEditor {
  constructor(canvas, onChange) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.onChange = onChange;
    this.garment = null;
    this.dragging = null;
    canvas.addEventListener("pointerdown", (e) => this.#down(e));
    canvas.addEventListener("pointermove", (e) => this.#move(e));
    canvas.addEventListener("pointerup", () => this.#up());
    canvas.addEventListener("pointercancel", () => this.#up());
  }

  setGarment(garment) {
    this.garment = garment;
    this.draw();
  }

  #names() {
    const g = this.garment;
    const names = [...(REQUIRED_POINTS[g.category] ?? [])];
    if (UPPER.includes(g.category) && g.sleeve !== "none") names.push(...CUFF_POINTS);
    return names.filter((n) => g.keypoints[n]);
  }

  #layout() {
    const g = this.garment;
    const src = g.editedCanvas;
    const cssW = this.canvas.clientWidth || 300;
    const scale = cssW / src.width;
    const cssH = src.height * scale;
    const dpr = window.devicePixelRatio || 1;
    if (this.canvas.width !== Math.round(cssW * dpr) || this.canvas.height !== Math.round(cssH * dpr)) {
      this.canvas.width = Math.round(cssW * dpr);
      this.canvas.height = Math.round(cssH * dpr);
      this.canvas.style.height = `${cssH}px`;
    }
    return { cssW, cssH, dpr };
  }

  draw() {
    const g = this.garment;
    if (!g) return;
    const { cssW, cssH, dpr } = this.#layout();
    const ctx = this.ctx;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    // 체크무늬 배경 (투명 부분이 보이도록)
    const cell = 10;
    for (let y = 0; y < cssH; y += cell) {
      for (let x = 0; x < cssW; x += cell) {
        ctx.fillStyle = ((x + y) / cell) % 2 ? "#ece7df" : "#f8f5f0";
        ctx.fillRect(x, y, cell, cell);
      }
    }
    ctx.drawImage(g.editedCanvas, 0, 0, cssW, cssH);

    const P = (n) => g.keypoints[n] && [g.keypoints[n].x * cssW, g.keypoints[n].y * cssH];
    const group = UPPER.includes(g.category) ? "upper" : g.category;
    ctx.lineWidth = 1.5;
    ctx.strokeStyle = "rgba(20,20,40,0.55)";
    ctx.setLineDash([5, 4]);
    for (const loop of OUTLINES[group] ?? []) {
      const pts = loop.map(P);
      if (pts.some((p) => !p)) continue;
      ctx.beginPath();
      pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)));
      ctx.closePath();
      ctx.stroke();
    }
    ctx.setLineDash([]);

    if (g.category === "hat" || g.category === "shoes") {
      const b = g.bbox;
      ctx.strokeStyle = "#1b7ce0";
      ctx.strokeRect(b.x * cssW, b.y * cssH, b.width * cssW, b.height * cssH);
    }

    ctx.font = "600 11px system-ui, sans-serif";
    for (const n of this.#names()) {
      const [x, y] = P(n);
      ctx.beginPath();
      ctx.arc(x, y, this.dragging === n ? 8 : 6, 0, Math.PI * 2);
      ctx.fillStyle = colorFor(n);
      ctx.fill();
      ctx.lineWidth = 2;
      ctx.strokeStyle = "#fff";
      ctx.stroke();
      const label = LABELS[n] ?? n;
      const tx = x + 9;
      const ty = y - 7;
      ctx.lineWidth = 3;
      ctx.strokeStyle = "rgba(255,255,255,0.9)";
      ctx.strokeText(label, tx, ty);
      ctx.fillStyle = "#1d1b26";
      ctx.fillText(label, tx, ty);
    }
  }

  #toNorm(e) {
    const r = this.canvas.getBoundingClientRect();
    return { x: (e.clientX - r.left) / r.width, y: (e.clientY - r.top) / r.height, r };
  }

  #down(e) {
    if (!this.garment) return;
    const p = this.#toNorm(e);
    let best = null;
    let bestD = 18; // CSS 픽셀 반경 안에서 가장 가까운 점
    for (const n of this.#names()) {
      const k = this.garment.keypoints[n];
      const d = Math.hypot((k.x - p.x) * p.r.width, (k.y - p.y) * p.r.height);
      if (d < bestD) {
        bestD = d;
        best = n;
      }
    }
    if (best) {
      this.dragging = best;
      this.canvas.setPointerCapture(e.pointerId);
      e.preventDefault();
      this.draw();
    }
  }

  #move(e) {
    if (!this.dragging) return;
    const p = this.#toNorm(e);
    this.garment.keypoints[this.dragging] = { x: Math.min(1, Math.max(0, p.x)), y: Math.min(1, Math.max(0, p.y)) };
    this.draw();
    if (!this.pending) {
      this.pending = requestAnimationFrame(() => {
        this.pending = 0;
        this.onChange(this.garment);
      });
    }
  }

  #up() {
    if (!this.dragging) return;
    this.dragging = null;
    this.draw();
    this.onChange(this.garment);
  }
}
