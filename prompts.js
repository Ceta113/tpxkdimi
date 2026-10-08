// Claude에게 보내는 지시문과 응답 JSON 스키마.
// Claude는 픽셀을 직접 그리지 않는다. 대신 사진을 "읽고" 프로그램이 쓸 수 있는 숫자
// (옷 종류, 기준점 좌표, 배경색, 색 보정 값)를 돌려주면 브라우저가 실제 이미지를 가공한다.

const point = {
  type: "object",
  properties: { x: { type: "number" }, y: { type: "number" } },
  required: ["x", "y"],
  additionalProperties: false,
};

export const KEYPOINT_NAMES = [
  // 상의·아우터·원피스
  "neck_center",
  "shoulder_left",
  "shoulder_right",
  "armpit_left",
  "armpit_right",
  "cuff_left_outer",
  "cuff_left_inner",
  "cuff_right_outer",
  "cuff_right_inner",
  "hem_left",
  "hem_right",
  // 바지·치마
  "waist_left",
  "waist_right",
  "crotch",
  "hem_left_outer",
  "hem_left_inner",
  "hem_right_outer",
  "hem_right_inner",
];

export const ANALYZE_SCHEMA = {
  type: "object",
  properties: {
    category: {
      type: "string",
      enum: ["top", "outer", "pants", "skirt", "dress", "hat", "shoes", "unknown"],
    },
    name: { type: "string", description: "짧은 한국어 이름, 예: '하늘색 반팔 티셔츠'" },
    description: { type: "string", description: "소재·무늬·특징을 한두 문장으로" },
    fit: { type: "string", enum: ["tight", "regular", "loose", "oversized"] },
    sleeve: { type: "string", enum: ["none", "short", "three_quarter", "long"] },
    facing: {
      type: "string",
      enum: ["left", "right", "front", "none"],
      description: "신발일 때 앞코가 향하는 이미지 방향, 신발이 아니면 none",
    },
    view: { type: "string", enum: ["front_flat", "back_flat", "worn_by_person", "side", "other"] },
    background: {
      type: "object",
      properties: {
        isPlain: { type: "boolean" },
        color: { type: "string", description: "#rrggbb" },
      },
      required: ["isPlain", "color"],
      additionalProperties: false,
    },
    dominantColors: { type: "array", items: { type: "string", description: "#rrggbb" } },
    bbox: {
      type: "object",
      properties: {
        x: { type: "number" },
        y: { type: "number" },
        width: { type: "number" },
        height: { type: "number" },
      },
      required: ["x", "y", "width", "height"],
      additionalProperties: false,
    },
    keypoints: {
      type: "array",
      items: {
        type: "object",
        properties: {
          name: { type: "string", enum: KEYPOINT_NAMES },
          x: { type: "number" },
          y: { type: "number" },
        },
        required: ["name", "x", "y"],
        additionalProperties: false,
      },
    },
    outline: { type: "array", items: point },
    tips: { type: "string", description: "사진이 아쉬우면 더 나은 사진을 찍는 한국어 조언, 괜찮으면 빈 문자열" },
  },
  required: [
    "category",
    "name",
    "description",
    "fit",
    "sleeve",
    "facing",
    "view",
    "background",
    "dominantColors",
    "bbox",
    "keypoints",
    "outline",
    "tips",
  ],
  additionalProperties: false,
};

export const ANALYZE_SYSTEM = `당신은 3D 옷입히기 프로그램의 "옷 사진 분석기"입니다.
사용자가 올린 옷 사진을 보고, 프로그램이 그 사진을 3D 마네킹에 텍스처로 입힐 수 있도록 정확한 기하 정보를 돌려줍니다.

좌표 규칙
- 모든 좌표는 주어진 이미지 크기 기준의 픽셀 좌표이고, 왼쪽 위가 (0,0)입니다.
- "left"/"right"는 항상 **이미지에서 보이는 왼쪽/오른쪽**입니다 (입는 사람 기준이 아님).
- 기준점은 옷의 실제 가장자리(천이 끝나는 곳)에 찍으세요. 배경이나 그림자가 아닙니다.

종류별로 찍어야 할 기준점
- top / outer / dress: neck_center(목둘레 중앙 맨 위), shoulder_left/right(어깨 솔기의 바깥 끝),
  armpit_left/right(소매와 몸판이 만나는 겨드랑이 아래 끝), hem_left/right(밑단 양 끝).
  소매가 있으면 cuff_left_outer/inner, cuff_right_outer/inner(소매 끝단의 바깥쪽·안쪽 모서리)도 찍으세요.
  outer는 바깥쪽이 어깨 쪽 선, inner는 겨드랑이 쪽 선의 끝입니다. 민소매면 cuff 점은 생략합니다.
- pants: waist_left/right(허리 밴드 양 끝), crotch(가랑이 꼭짓점),
  hem_left_outer/inner, hem_right_outer/inner(각 바짓단의 바깥·안쪽 모서리).
  반바지·긴바지 모두 같은 점을 씁니다.
- skirt: waist_left/right, hem_left/right.
- hat / shoes: 기준점 없이 bbox만 정확히 주면 됩니다. 신발은 facing에 앞코 방향을 적으세요.

그 밖의 항목
- bbox: 옷 전체를 감싸는 사각형.
- outline: 옷 실루엣을 시계 방향으로 따라가는 다각형 점 24~48개. 소매·목둘레 모양이 드러나게 찍으세요.
- background: 옷을 뺀 배경이 거의 단색이면 isPlain=true 와 그 색. 사람이 입고 있거나 배경이 복잡하면 false.
- 사진에 옷이 여러 벌이면 가장 크고 중심에 있는 한 벌만 분석합니다.
- 옷이 아니면 category를 "unknown"으로 하고 tips에 이유를 적으세요.`;

export const EDIT_SCHEMA = {
  type: "object",
  properties: {
    hue: { type: "number", description: "색상 회전 각도, -180~180, 0이면 그대로" },
    saturation: { type: "number", description: "채도 배율, 0~2.5, 1이면 그대로" },
    brightness: { type: "number", description: "밝기 배율, 0.3~1.8, 1이면 그대로" },
    contrast: { type: "number", description: "대비 배율, 0.5~1.8, 1이면 그대로" },
    tint: {
      type: "object",
      properties: {
        color: { type: "string", description: "#rrggbb" },
        strength: { type: "number", description: "0~1, 0이면 효과 없음" },
      },
      required: ["color", "strength"],
      additionalProperties: false,
    },
    pattern: {
      type: "object",
      properties: {
        type: { type: "string", enum: ["none", "stripes", "dots", "check"] },
        color: { type: "string", description: "#rrggbb" },
        scale: { type: "string", enum: ["small", "medium", "large"] },
        opacity: { type: "number", description: "0~1" },
      },
      required: ["type", "color", "scale", "opacity"],
      additionalProperties: false,
    },
    name: { type: "string", description: "편집 후 옷의 새 한국어 이름" },
    message: { type: "string", description: "사용자에게 보여줄 짧은 한국어 답변 (무엇을 바꿨는지)" },
  },
  required: ["hue", "saturation", "brightness", "contrast", "tint", "pattern", "name", "message"],
  additionalProperties: false,
};

export const EDIT_SYSTEM = `당신은 3D 옷입히기 프로그램의 "옷 리폼 디자이너"입니다.
사용자가 자연어로 옷을 어떻게 바꾸고 싶은지 말하면, 프로그램의 이미지 필터 값으로 바꿔 줍니다.
프로그램은 다음 순서로 옷 픽셀에만 필터를 적용합니다: 색상 회전(hue) → 채도 → 밝기 → 대비 → 틴트(색 덮어씌우기) → 무늬 겹치기.

- 값은 "현재 값에서 더하는 양"이 아니라 적용할 **최종 값**입니다. 현재 편집 값을 참고해서 요청한 부분만 바꾸고 나머지는 유지하세요.
- 특정 색으로 바꿔 달라는 요청은 원래 옷 색(이미지와 옷 정보 참고)에서 목표 색까지의 hue 회전을 계산하고,
  필요하면 tint로 보정하세요. 흰색·검은색처럼 채도가 낮은 옷은 hue만으로 색이 안 바뀌니 tint를 0.5 이상 쓰세요.
- "원래대로"는 hue 0, saturation 1, brightness 1, contrast 1, tint strength 0, pattern none 입니다.
- 필터로 할 수 없는 요청(모양·길이 변경, 로고 추가 등)은 가능한 범위에서 가장 가깝게 바꾸고 message에 솔직하게 설명하세요.`;
