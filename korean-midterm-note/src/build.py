"""원본 국어 정리노트 PDF에 필기 보충 페이지를 끼워 넣어 보충판을 만든다.

사용: python3 build.py <원본노트.pdf> <출력.pdf>
"""
import os, subprocess, sys, json, tempfile
import pymupdf
import supp

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.expanduser('~/.fonts/f0.ttf')  # Noto Sans KR Regular

# (원본 쪽 번호 뒤에 끼움, 이름, 단원, 설명)
SECTIONS = [
    (8, 'S1', supp.S1, 'Ⅰ-1 시조', '「어져 내 일이야」 vs 「마음이 어린 후이니」 비교 · 4수 화자 태도 · 님이 오마 하거늘 필기 흐름'),
    (13, 'S2', supp.S2, 'Ⅰ-2 현대시', '연탄 한 장 vs 담쟁이 4축 비교 · 특징 9/6 필기 순서 · 감각적 이미지 확인'),
    (21, 'S3', supp.S3, 'Ⅱ 논증의 오류', '필기 이름 ↔ 노트 이름 · 한 줄 정의 · 결합 vs 성급한 일반화 · 허수아비 vs 비탈길 · 상관관계'),
    (28, 'S4', supp.S4, 'Ⅲ 문장의 짜임', '성분별 형식표 · 필수적 vs 이동 불가 부사어 · 접미사 -이 vs 어미 -게 · 간접 인용 규칙'),
    (37, 'S5', supp.S5, '보충 문제', '필기 포인트로 만든 문제 57~74 + 정답과 해설'),
]

JS = """
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(process.argv[2]);
  const b = await chromium.launch(); const p = await b.newPage();
  for (const [html, pdf] of jobs) {
    await p.goto('file://' + html, { waitUntil: 'load' });
    await p.pdf({ path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true });
  }
  await b.close();
})();
"""


def render(items, tmp):
    jobs = []
    for name, body in items:
        h = os.path.join(tmp, name + '.html'); f = os.path.join(tmp, name + '.pdf')
        open(h, 'w', encoding='utf-8').write(supp.page(body))
        jobs.append([h, f])
    js = os.path.join(tmp, 'r.js'); open(js, 'w').write(JS)
    root = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
    subprocess.run(['node', js, json.dumps(jobs)], check=True, env={**os.environ, 'NODE_PATH': root})
    return {n: pymupdf.open(os.path.join(tmp, n + '.pdf')) for n, _ in items}


def main(src, out):
    tmp = tempfile.mkdtemp()
    orig = pymupdf.open(src)
    docs = render([(n, b) for _, n, b, _, _ in SECTIONS], tmp)
    # 새 쪽 번호 계산 (원본 1쪽 뒤에 안내 1쪽)
    order = [('O', 1), ('G', None)]
    for i in range(2, orig.page_count + 1):
        order.append(('O', i))
        for after, n, *_ in SECTIONS:
            if after == i:
                order += [(n, k) for k in range(docs[n].page_count)]
    first = {}
    for idx, (kind, k) in enumerate(order, 1):
        if kind not in ('O', 'G') and kind not in first:
            first[kind] = idx
    rows = []
    for _, n, _, unit, desc in SECTIONS:
        cnt = docs[n].page_count
        rng = f'{first[n]}' if cnt == 1 else f'{first[n]}~{first[n] + cnt - 1}'
        rows.append((rng, unit, desc))
    g = render([('G', supp.guide(rows))], tmp)['G']
    assert g.page_count == 1, g.page_count
    docs['G'] = g

    res = pymupdf.open()
    for kind, k in order:
        if kind == 'O':
            res.insert_pdf(orig, from_page=k - 1, to_page=k - 1)
        elif kind == 'G':
            res.insert_pdf(g)
        else:
            res.insert_pdf(docs[kind], from_page=k, to_page=k)
    total = res.page_count
    for i, pg in enumerate(res):
        kind = order[i][0]
        w = pg.rect.width
        if kind == 'O':
            pg.add_redact_annot(pymupdf.Rect(150, 810, w - 150, 830), fill=(1, 1, 1))
            pg.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE)
        label = f'중3 국어 정리노트 (필기 보충판) · {i + 1} / {total}'
        if kind not in ('O',):
            label += '  · 보충'
        pg.insert_font(fontname='nkr', fontfile=FONT)
        tw = pymupdf.Font(fontfile=FONT).text_length(label, fontsize=7.5)
        pg.insert_text(((w - tw) / 2, 823), label, fontname='nkr', fontsize=7.5, color=(0.53, 0.53, 0.53))
    res.set_metadata({'title': '국어 정리노트 (필기 보충판)'})
    res.save(out, garbage=3, deflate=True)
    print('pages', total, {k: first.get(k) for k in first}, rows)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
