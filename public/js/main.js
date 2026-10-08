import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { createMannequin } from "./mannequin.js";
import { buildGarmentMesh, SLOTS, SOLID_CATEGORIES } from "./garments.js";
import {
  DEFAULT_ADJUST,
  UPPER,
  applyAdjustments,
  bleedColors,
  canvasToPayload,
  fillMissingKeypoints,
  guessKeypoints,
  loadImageToCanvas,
  makeBackCanvas,
  normalizeAdjust,
  normalizeAnalysis,
  removeBackground,
  thumbnail,
} from "./imageproc.js";
import { SAMPLES } from "./samples.js";
import { KeypointEditor } from "./keypoint-editor.js";

const $ = (sel) => document.querySelector(sel);
const CATEGORY_LABEL = { top: "상의", outer: "아우터", dress: "원피스", pants: "바지", skirt: "치마", hat: "모자", shoes: "신발" };

// ── 3D 장면 ─────────────────────────────────────────────────────────
const stage = $("#stage");
const renderer = new THREE.WebGLRenderer({ canvas: $("#scene"), antialias: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xebe6de);
const camera = new THREE.PerspectiveCamera(30, 1, 0.05, 50);
camera.position.set(0, 1.1, 4.3);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 0.88, 0);
controls.enableDamping = true;
controls.minDistance = 1.0;
controls.maxDistance = 7;
controls.maxPolarAngle = Math.PI * 0.55;
controls.update();

scene.add(new THREE.HemisphereLight(0xffffff, 0x9a8f80, 1.4));
const key = new THREE.DirectionalLight(0xffffff, 2.2);
key.position.set(2.5, 4.5, 3.5);
key.castShadow = true;
key.shadow.mapSize.set(2048, 2048);
key.shadow.camera.left = -1.2;
key.shadow.camera.right = 1.2;
key.shadow.camera.top = 2.2;
key.shadow.camera.bottom = -0.2;
key.shadow.bias = -0.0004;
key.shadow.normalBias = 0.02;
scene.add(key);
const rim = new THREE.DirectionalLight(0xfff1e0, 1.0);
rim.position.set(-3, 2.5, -3);
scene.add(rim);

const floor = new THREE.Mesh(new THREE.CircleGeometry(1.1, 64), new THREE.MeshStandardMaterial({ color: 0xd8cfc2, roughness: 0.9 }));
floor.rotation.x = -Math.PI / 2;
floor.receiveShadow = true;
scene.add(floor);

const turntable = new THREE.Group();
turntable.add(createMannequin());
scene.add(turntable);

let spinning = false;
let targetRotation = 0;
const timer = new THREE.Timer();

function resize() {
  const { clientWidth: w, clientHeight: h } = stage;
  renderer.setSize(w, h, false);
  camera.aspect = w / Math.max(h, 1);
  camera.updateProjectionMatrix();
}
new ResizeObserver(resize).observe(stage);
resize();

renderer.setAnimationLoop((time) => {
  timer.update(time);
  const dt = Math.min(timer.getDelta(), 0.05);
  if (spinning) {
    turntable.rotation.y += dt * 0.6;
  } else {
    // 가장 가까운 방향으로 부드럽게 돌아가기
    let diff = targetRotation - turntable.rotation.y;
    diff = Math.atan2(Math.sin(diff), Math.cos(diff));
    turntable.rotation.y += diff * Math.min(1, dt * 6);
  }
  controls.update();
  renderer.render(scene, camera);
});

// ── 상태 ────────────────────────────────────────────────────────────
const state = { garments: [], selectedId: null, worn: {}, ai: false, nextId: 1 };
const byId = (id) => state.garments.find((g) => g.id === id);
const isWorn = (g) => Object.values(state.worn).includes(g.id);

function toast(message, ms = 3200) {
  const el = $("#toast");
  el.textContent = message;
  el.classList.add("show");
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => el.classList.remove("show"), ms);
}

async function api(path, body) {
  const res = await fetch(path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `요청 실패 (${res.status})`);
  return data;
}

async function checkStatus() {
  const chip = $("#ai-status");
  try {
    const res = await fetch("/api/status");
    const s = await res.json();
    state.ai = s.keyConfigured;
    chip.textContent = s.keyConfigured ? `Claude 연결됨 · ${s.model}` : "API 키 없음 · 수동 모드";
    chip.className = `chip ${s.keyConfigured ? "ok" : "off"}`;
    chip.title = s.keyConfigured ? "" : "ANTHROPIC_API_KEY를 설정하고 서버를 다시 켜면 Claude 분석을 쓸 수 있어요";
  } catch {
    chip.textContent = "서버 연결 안 됨";
    chip.className = "chip off";
  }
}

// ── 옷 추가 · 처리 ───────────────────────────────────────────────────
async function addGarment(sourceCanvas, { analysis = null, hint = "auto" } = {}) {
  const g = {
    id: state.nextId++,
    name: "분석 중…",
    category: hint === "auto" ? "top" : hint,
    status: "busy",
    sourceCanvas,
    width: sourceCanvas.width,
    height: sourceCanvas.height,
    adjust: structuredClone(DEFAULT_ADJUST),
    thumbUrl: thumbnail(sourceCanvas),
    keypoints: {},
    bbox: null,
    outline: [],
    bgPlain: true,
    bgTol: 60,
    fit: "regular",
    sleeve: "short",
    facing: "left",
    description: "",
    tips: "",
  };
  state.garments.push(g);
  renderList();

  let size = { width: sourceCanvas.width, height: sourceCanvas.height };
  if (!analysis && state.ai) {
    try {
      const payload = canvasToPayload(sourceCanvas);
      size = payload;
      analysis = await api("/api/analyze", { image: payload, categoryHint: hint });
    } catch (e) {
      toast(`${e.message} → 자동 추정으로 대신할게요`, 5000);
    }
  }

  if (analysis) {
    const a = normalizeAnalysis(analysis, size);
    Object.assign(g, {
      name: a.name || "새 옷",
      description: a.description || "",
      tips: a.tips || "",
      fit: a.fit || "regular",
      sleeve: a.sleeve || "short",
      facing: a.facing || "left",
      keypoints: a.keypoints,
      bbox: a.bbox,
      outline: a.outline,
      bgPlain: a.background?.isPlain ?? true,
      dominantColors: a.dominantColors ?? [],
    });
    if (hint !== "auto") g.category = hint;
    else if (a.category && a.category !== "unknown") g.category = a.category;
    else g.tips ||= "옷 종류를 알아보지 못했어요. 오른쪽 편집에서 종류를 골라 주세요.";
  } else {
    g.name = `새 ${CATEGORY_LABEL[g.category]}`;
    if (!state.ai) g.tips = "API 키가 없어서 사진 모양으로 기준점을 추정했어요. 점을 끌어서 맞춰 주세요.";
  }

  processImage(g);
  g.status = "ready";
  wear(g);
  select(g);
  if (g.tips) toast(g.tips, 5000);
}

function processImage(g) {
  g.maskCanvas = removeBackground(g.sourceCanvas, { plain: g.bgPlain, tolerance: g.bgTol, outline: g.outline, bbox: g.bbox });
  fillMissingKeypoints(g, g.maskCanvas);
  updateTexture(g);
}

function canvasTexture(old, canvas) {
  if (old && old.image.width === canvas.width && old.image.height === canvas.height) {
    old.image = canvas;
    old.needsUpdate = true;
    return old;
  }
  old?.dispose();
  const tex = new THREE.CanvasTexture(canvas);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
  return tex;
}

// 편집 값 → 화면용 이미지(editedCanvas) → 3D용 텍스처(앞판·등판)
function updateTexture(g) {
  g.editedCanvas = applyAdjustments(g.maskCanvas, g.adjust);
  const front = bleedColors(g.editedCanvas, { opaque: SOLID_CATEGORIES.includes(g.category) });
  g.textures ??= {};
  g.textures.front = canvasTexture(g.textures.front, front);
  if (UPPER.includes(g.category)) {
    g.textures.back = canvasTexture(g.textures.back, bleedColors(makeBackCanvas(g.editedCanvas)));
  } else {
    g.textures.back?.dispose();
    delete g.textures.back;
  }
  g.thumbUrl = thumbnail(g.editedCanvas);
  rebuildMesh(g);
  renderList();
}

function disposeMesh(mesh) {
  if (!mesh) return;
  turntable.remove(mesh);
  mesh.traverse((o) => {
    if (o.isMesh) {
      o.geometry.dispose();
      [o.material].flat().forEach((m) => m.dispose());
      o.customDepthMaterial?.dispose();
    }
  });
}

function rebuildMesh(g) {
  disposeMesh(g.mesh);
  g.mesh = buildGarmentMesh(g, g.textures);
  if (isWorn(g)) turntable.add(g.mesh);
}

function wear(g) {
  for (const slot of SLOTS[g.category] ?? []) {
    const other = byId(state.worn[slot]);
    if (other && other !== g) unwear(other);
    state.worn[slot] = g.id;
  }
  if (g.mesh && !g.mesh.parent) turntable.add(g.mesh);
  renderList();
}

function unwear(g) {
  for (const [slot, id] of Object.entries(state.worn)) if (id === g.id) delete state.worn[slot];
  if (g.mesh) turntable.remove(g.mesh);
  renderList();
}

function removeGarment(g) {
  unwear(g);
  disposeMesh(g.mesh);
  g.textures?.front?.dispose();
  g.textures?.back?.dispose();
  state.garments = state.garments.filter((x) => x !== g);
  if (state.selectedId === g.id) select(null);
  renderList();
}

// ── 옷장 목록 ────────────────────────────────────────────────────────
function renderList() {
  const ul = $("#garment-list");
  ul.replaceChildren();
  for (const g of state.garments) {
    const li = document.createElement("li");
    li.className = `garment${g.id === state.selectedId ? " selected" : ""}${g.status === "busy" ? " busy" : ""}`;
    const img = document.createElement("img");
    img.src = g.thumbUrl;
    img.alt = "";
    const meta = document.createElement("div");
    meta.className = "meta";
    const name = document.createElement("div");
    name.className = "name";
    name.textContent = g.name;
    const kind = document.createElement("div");
    kind.className = "kind";
    kind.textContent = g.status === "busy" ? (state.ai ? "Claude가 분석 중" : "처리 중") : CATEGORY_LABEL[g.category];
    meta.append(name, kind);
    li.append(img, meta);
    if (g.status === "ready") {
      const btn = document.createElement("button");
      const worn = isWorn(g);
      btn.className = `wear${worn ? " on" : ""}`;
      btn.textContent = worn ? "입는 중" : "입기";
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        worn ? unwear(g) : wear(g);
      });
      li.append(btn);
      li.addEventListener("click", () => select(g));
    }
    ul.append(li);
  }
  $("#wardrobe-empty").hidden = state.garments.length > 0;
  $("#garment-count").textContent = state.garments.length ? `${state.garments.length}벌` : "";
}

// ── 편집 패널 ────────────────────────────────────────────────────────
const kpEditor = new KeypointEditor($("#kp-canvas"), (g) => rebuildMesh(g));
window.addEventListener("resize", () => kpEditor.draw());
const selected = () => byId(state.selectedId);

function select(g) {
  state.selectedId = g?.id ?? null;
  renderList();
  $("#editor-empty").hidden = Boolean(g);
  $("#editor-body").hidden = !g;
  if (!g) return;
  $("#ed-name").value = g.name;
  $("#ed-desc").textContent = g.description;
  $("#ed-tips").textContent = g.tips;
  $("#ed-tips").hidden = !g.tips;
  $("#ai-edit-reply").hidden = true;
  $("#ed-category").value = g.category;
  $("#ed-fit").value = g.fit;
  $("#ed-sleeve").value = g.sleeve;
  $("#sleeve-field").hidden = !UPPER.includes(g.category);
  $("#bg-plain").checked = g.bgPlain;
  setSlider("#bg-tol", g.bgTol);
  syncAdjustInputs(g);
  kpEditor.setGarment(g);
}

function setSlider(sel, value, fmt = (v) => v) {
  const input = $(sel);
  input.value = value;
  const out = input.parentElement.querySelector("output");
  if (out) out.textContent = fmt(Number(value));
}

const pct = (v) => `${Math.round(v * 100)}%`;
function syncAdjustInputs(g) {
  const a = g.adjust;
  setSlider("#adj-hue", a.hue, (v) => `${v}°`);
  setSlider("#adj-saturation", a.saturation, pct);
  setSlider("#adj-brightness", a.brightness, pct);
  setSlider("#adj-contrast", a.contrast, pct);
  setSlider("#adj-tint", a.tint.strength);
  $("#adj-tint-color").value = a.tint.color;
  $("#pat-type").value = a.pattern.type;
  $("#pat-scale").value = a.pattern.scale;
  $("#pat-color").value = a.pattern.color;
  setSlider("#pat-opacity", a.pattern.opacity, pct);
}

// 슬라이더는 연속으로 바뀌므로 한 프레임에 한 번만 다시 그린다
let adjustFrame = 0;
function scheduleTextureUpdate(g) {
  if (adjustFrame) return;
  adjustFrame = requestAnimationFrame(() => {
    adjustFrame = 0;
    updateTexture(g);
    kpEditor.draw();
  });
}

const adjustBindings = {
  "#adj-hue": (a, v) => (a.hue = Number(v)),
  "#adj-saturation": (a, v) => (a.saturation = Number(v)),
  "#adj-brightness": (a, v) => (a.brightness = Number(v)),
  "#adj-contrast": (a, v) => (a.contrast = Number(v)),
  "#adj-tint": (a, v) => (a.tint.strength = Number(v)),
  "#adj-tint-color": (a, v) => {
    a.tint.color = v;
    if (a.tint.strength === 0) a.tint.strength = 0.6;
  },
  "#pat-type": (a, v) => (a.pattern.type = v),
  "#pat-scale": (a, v) => (a.pattern.scale = v),
  "#pat-color": (a, v) => (a.pattern.color = v),
  "#pat-opacity": (a, v) => (a.pattern.opacity = Number(v)),
};
for (const [sel, apply] of Object.entries(adjustBindings)) {
  $(sel).addEventListener("input", (e) => {
    const g = selected();
    if (!g) return;
    apply(g.adjust, e.target.value);
    syncAdjustInputs(g);
    scheduleTextureUpdate(g);
  });
}

$("#ed-name").addEventListener("input", (e) => {
  const g = selected();
  if (!g) return;
  g.name = e.target.value;
  renderList();
});

$("#ed-category").addEventListener("change", (e) => {
  const g = selected();
  if (!g) return;
  const wasWorn = isWorn(g);
  unwear(g);
  g.category = e.target.value;
  // 새 종류에 필요한 기준점을 다시 추정
  g.keypoints = guessKeypoints(g.maskCanvas, g.category).keypoints;
  fillMissingKeypoints(g, g.maskCanvas);
  updateTexture(g);
  if (wasWorn) wear(g);
  select(g);
});

$("#ed-fit").addEventListener("change", (e) => {
  const g = selected();
  if (!g) return;
  g.fit = e.target.value;
  rebuildMesh(g);
});

$("#ed-sleeve").addEventListener("change", (e) => {
  const g = selected();
  if (!g) return;
  g.sleeve = e.target.value;
  fillMissingKeypoints(g, g.maskCanvas);
  rebuildMesh(g);
  kpEditor.draw();
});

$("#kp-reset").addEventListener("click", () => {
  const g = selected();
  if (!g) return;
  const guess = guessKeypoints(g.maskCanvas, g.category);
  g.keypoints = guess.keypoints;
  g.bbox = guess.bbox;
  rebuildMesh(g);
  kpEditor.draw();
});

function reprocessBackground() {
  const g = selected();
  if (!g) return;
  processImage(g);
  kpEditor.draw();
}
$("#bg-plain").addEventListener("change", (e) => {
  const g = selected();
  if (!g) return;
  g.bgPlain = e.target.checked;
  reprocessBackground();
});
let tolTimer = 0;
$("#bg-tol").addEventListener("input", (e) => {
  const g = selected();
  if (!g) return;
  g.bgTol = Number(e.target.value);
  setSlider("#bg-tol", g.bgTol);
  clearTimeout(tolTimer);
  tolTimer = setTimeout(reprocessBackground, 120);
});

$("#ed-delete").addEventListener("click", () => {
  const g = selected();
  if (g && confirm(`"${g.name}"을(를) 옷장에서 지울까요?`)) removeGarment(g);
});

// Claude에게 리폼 요청: 자연어 → 필터 값
$("#ai-edit-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const g = selected();
  const input = $("#ai-edit-input");
  const instruction = input.value.trim();
  if (!g || !instruction) return;
  if (!state.ai) {
    toast("이 기능은 Claude API 키가 필요해요. 대신 아래 슬라이더로 직접 바꿔 보세요.", 4500);
    return;
  }
  const button = $("#ai-edit-submit");
  button.disabled = true;
  button.textContent = "…";
  try {
    const res = await api("/api/edit", {
      instruction,
      garment: { name: g.name, category: g.category, description: g.description, dominantColors: g.dominantColors },
      current: g.adjust,
      image: canvasToPayload(g.maskCanvas, 384),
    });
    if (selected() !== g) return;
    g.adjust = normalizeAdjust(res);
    if (res.name) g.name = res.name;
    $("#ed-name").value = g.name;
    $("#ai-edit-reply").textContent = res.message;
    $("#ai-edit-reply").hidden = !res.message;
    input.value = "";
    syncAdjustInputs(g);
    updateTexture(g);
    kpEditor.draw();
  } catch (err) {
    toast(err.message, 5000);
  } finally {
    button.disabled = false;
    button.textContent = "요청";
  }
});
$("#quick-edits").addEventListener("click", (e) => {
  if (e.target.tagName !== "BUTTON") return;
  $("#ai-edit-input").value = e.target.textContent;
  $("#ai-edit-form").requestSubmit();
});

// ── 업로드 ──────────────────────────────────────────────────────────
async function addFiles(files) {
  const hint = $("#category-hint").value;
  for (const file of files) {
    if (!file.type.startsWith("image/")) continue;
    try {
      const canvas = await loadImageToCanvas(file);
      addGarment(canvas, { hint });
    } catch {
      toast(`${file.name}을(를) 열 수 없어요.`);
    }
  }
}
$("#file-input").addEventListener("change", (e) => {
  addFiles([...e.target.files]);
  e.target.value = "";
});
for (const zone of [$("#dropzone"), stage]) {
  zone.addEventListener("dragover", (e) => {
    e.preventDefault();
    $("#dropzone").classList.add("over");
  });
  zone.addEventListener("dragleave", () => $("#dropzone").classList.remove("over"));
  zone.addEventListener("drop", (e) => {
    e.preventDefault();
    $("#dropzone").classList.remove("over");
    addFiles([...e.dataTransfer.files]);
  });
}

for (const sample of SAMPLES) {
  const btn = document.createElement("button");
  btn.textContent = sample.label;
  btn.addEventListener("click", () => {
    const { canvas, analysis } = sample.make();
    addGarment(canvas, { analysis });
  });
  $("#sample-buttons").append(btn);
}

// ── 툴바 ────────────────────────────────────────────────────────────
function setSpin(on) {
  spinning = on;
  $("#spin").setAttribute("aria-pressed", String(on));
}
document.querySelectorAll("[data-view]").forEach((btn) =>
  btn.addEventListener("click", () => {
    setSpin(false);
    targetRotation = -THREE.MathUtils.degToRad(Number(btn.dataset.view));
  }),
);
$("#spin").addEventListener("click", () => {
  setSpin(!spinning);
  if (!spinning) targetRotation = turntable.rotation.y;
});
$("#undress").addEventListener("click", () => state.garments.forEach(unwear));
$("#snapshot").addEventListener("click", () => {
  renderer.render(scene, camera);
  const a = document.createElement("a");
  a.href = renderer.domElement.toDataURL("image/png");
  a.download = "ai-dress-up.png";
  a.click();
});

// ── 시작 ────────────────────────────────────────────────────────────
await checkStatus();
for (const id of ["tshirt", "jeans"]) {
  const { canvas, analysis } = SAMPLES.find((s) => s.id === id).make();
  await addGarment(canvas, { analysis });
}
select(null);
window.__dressUp = { state, scene, turntable }; // 디버깅용
