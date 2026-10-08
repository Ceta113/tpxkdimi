// AI 3D 옷입히기 — 서버
// 정적 파일(public/)을 제공하고, 옷 사진 분석·편집 요청을 Claude API로 전달한다.
// API 키는 서버에만 두고 브라우저에는 절대 내려보내지 않는다.

import http from "node:http";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import Anthropic from "@anthropic-ai/sdk";
import { ANALYZE_SCHEMA, ANALYZE_SYSTEM, EDIT_SCHEMA, EDIT_SYSTEM } from "./prompts.js";

const here = path.dirname(fileURLToPath(import.meta.url));
const PORT = Number(process.env.PORT) || 3000;
const MODEL = process.env.CLAUDE_MODEL || "claude-opus-5-5";
const MAX_BODY = 12 * 1024 * 1024;

const STATIC_ROOTS = {
  "/vendor/three/": path.join(here, "node_modules/three/"),
  "/": path.join(here, "public/"),
};
const MIME = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".svg": "image/svg+xml",
};

const client = new Anthropic();
const keyConfigured = Boolean(process.env.ANTHROPIC_API_KEY || process.env.ANTHROPIC_AUTH_TOKEN);

// Claude에게 이미지 + 지시문을 보내고, JSON 스키마에 맞는 결과를 받는다.
async function askClaude({ system, schema, image, text, effort }) {
  const content = [];
  if (image) {
    content.push({ type: "image", source: { type: "base64", media_type: image.mediaType, data: image.data } });
  }
  content.push({ type: "text", text });

  const response = await client.beta.messages.create({
    model: MODEL,
    max_tokens: 16000,
    betas: ["server-side-fallback-2026-07-01"],
    fallbacks: "default", // 안전 분류기가 거절하면 서버에서 다른 모델로 자동 재시도
    output_config: { effort, format: { type: "json_schema", schema } },
    system,
    messages: [{ role: "user", content }],
  });

  if (response.stop_reason === "refusal") {
    throw new UserError("Claude가 이 이미지를 처리하지 않았어요. 다른 사진으로 시도해 주세요.");
  }
  if (response.stop_reason === "max_tokens") {
    throw new UserError("응답이 너무 길어 잘렸어요. 다시 시도해 주세요.");
  }
  const textBlock = response.content.find((b) => b.type === "text");
  if (!textBlock) throw new UserError("Claude 응답에 결과가 없어요.");
  return JSON.parse(textBlock.text);
}

class UserError extends Error {}

function describeApiError(error) {
  if (error instanceof UserError) return { status: 422, message: error.message };
  if (error instanceof Anthropic.AuthenticationError) {
    return { status: 401, message: "API 키가 없거나 올바르지 않아요. ANTHROPIC_API_KEY를 확인해 주세요." };
  }
  if (error instanceof Anthropic.RateLimitError) {
    return { status: 429, message: "요청이 너무 많아요. 잠시 후 다시 시도해 주세요." };
  }
  if (error instanceof Anthropic.BadRequestError) {
    return { status: 400, message: `요청 오류: ${error.message}` };
  }
  if (error instanceof Anthropic.APIError) {
    return { status: 502, message: `Claude API 오류 (${error.status ?? "연결 실패"}): ${error.message}` };
  }
  if (error instanceof SyntaxError) return { status: 400, message: "요청 형식이 올바르지 않아요." };
  if (!keyConfigured) {
    // 요청을 보내기도 전에 SDK가 인증 정보를 찾지 못한 경우
    return { status: 401, message: "Claude 인증 정보가 없어요. ANTHROPIC_API_KEY를 설정하고 서버를 다시 켜 주세요." };
  }
  return { status: 500, message: `서버 오류: ${error.message}` };
}

function validateImage(image) {
  const ok =
    image &&
    typeof image.data === "string" &&
    ["image/jpeg", "image/png", "image/webp", "image/gif"].includes(image.mediaType);
  if (!ok) throw new UserError("이미지 형식이 올바르지 않아요.");
}

async function handleAnalyze(body) {
  validateImage(body.image);
  const { width, height } = body.image;
  const hint = body.categoryHint && body.categoryHint !== "auto" ? `사용자가 고른 종류: ${body.categoryHint}` : "";
  const text = [
    `이 옷 사진을 분석해 주세요. 이미지 크기는 가로 ${width}px, 세로 ${height}px 입니다.`,
    "모든 좌표는 이 크기 기준의 픽셀 좌표(왼쪽 위가 0,0)로 답해 주세요.",
    hint,
  ].join("\n");
  return askClaude({ system: ANALYZE_SYSTEM, schema: ANALYZE_SCHEMA, image: body.image, text, effort: "medium" });
}

async function handleEdit(body) {
  if (typeof body.instruction !== "string" || !body.instruction.trim()) {
    throw new UserError("어떻게 바꿀지 적어 주세요.");
  }
  if (body.image) validateImage(body.image);
  const text = [
    `옷 정보: ${JSON.stringify(body.garment ?? {})}`,
    `현재 편집 값: ${JSON.stringify(body.current ?? {})}`,
    `사용자 요청: ${body.instruction.slice(0, 500)}`,
  ].join("\n");
  return askClaude({ system: EDIT_SYSTEM, schema: EDIT_SCHEMA, image: body.image, text, effort: "low" });
}

const API_ROUTES = { "/api/analyze": handleAnalyze, "/api/edit": handleEdit };

async function readJson(req) {
  const chunks = [];
  let size = 0;
  for await (const chunk of req) {
    size += chunk.length;
    if (size > MAX_BODY) throw new UserError("이미지가 너무 커요.");
    chunks.push(chunk);
  }
  return JSON.parse(Buffer.concat(chunks).toString("utf8"));
}

function sendJson(res, status, data) {
  res.writeHead(status, { "Content-Type": MIME[".json"] });
  res.end(JSON.stringify(data));
}

async function serveStatic(req, res) {
  let urlPath;
  try {
    urlPath = decodeURIComponent(new URL(req.url, "http://x").pathname);
  } catch {
    return sendJson(res, 400, { error: "bad request" });
  }
  const prefix = Object.keys(STATIC_ROOTS).find((p) => urlPath.startsWith(p));
  const root = STATIC_ROOTS[prefix];
  let filePath = path.join(root, urlPath.slice(prefix.length));
  if (!filePath.startsWith(root)) return sendJson(res, 403, { error: "forbidden" });
  if (urlPath.endsWith("/")) filePath = path.join(filePath, "index.html");
  try {
    const data = await fs.readFile(filePath);
    res.writeHead(200, { "Content-Type": MIME[path.extname(filePath)] ?? "application/octet-stream" });
    res.end(data);
  } catch {
    sendJson(res, 404, { error: "not found" });
  }
}

const server = http.createServer(async (req, res) => {
  const { pathname } = new URL(req.url, "http://x");
  if (req.method === "GET" && pathname === "/api/status") {
    return sendJson(res, 200, { keyConfigured, model: MODEL });
  }
  const route = API_ROUTES[pathname];
  if (route && req.method === "POST") {
    try {
      const result = await route(await readJson(req));
      return sendJson(res, 200, result);
    } catch (error) {
      const { status, message } = describeApiError(error);
      console.error(`[${pathname}]`, error.message);
      return sendJson(res, status, { error: message });
    }
  }
  if (req.method === "GET") return serveStatic(req, res);
  sendJson(res, 405, { error: "method not allowed" });
});

server.listen(PORT, () => {
  console.log(`👗 AI 3D 옷입히기: http://localhost:${PORT}`);
  console.log(`   모델: ${MODEL}${keyConfigured ? "" : "  (ANTHROPIC_API_KEY 없음 → 자동 분석 대신 수동 모드)"}`);
});
