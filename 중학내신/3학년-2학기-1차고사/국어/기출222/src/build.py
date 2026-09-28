"""국어 기출 222 문제집 조판.  실행: python3 src/build.py"""
import os, re, sys, json, subprocess, tempfile
import pymupdf
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import s1, s2, s3, s4
from q import C

STAGES = [s1.S, s2.S, s3.S, s4.S]
COL = {'b': ('#1f9d62', '#e8f6ee'), 'a': ('#2f6fd6', '#eaf2fd'), 'd': ('#7e57c2', '#f1ebfd'), 's': ('#d6334a', '#fde8ec')}
AREAS = ['시조', '현대시', '논증', '문법']
AREA_FULL = {'시조': 'Ⅰ-1 시조', '현대시': 'Ⅰ-2 현대시', '논증': 'Ⅱ 논증', '문법': 'Ⅲ 문장의 짜임'}
OUT = os.path.join(os.path.dirname(HERE), '국어기출222_문제집.pdf')

CSS = r"""
@page{size:A4;margin:13mm 12mm 15mm}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;font-family:'Noto Sans KR',sans-serif;color:#1b1d22;font-size:9.4pt;line-height:1.55;word-break:keep-all}
.serif{font-family:'Noto Serif KR',serif}
.pb{break-before:page}
/* divider */
.div{height:268mm;border-radius:14px;padding:26mm 18mm;color:#fff;position:relative;overflow:hidden;display:flex;flex-direction:column;justify-content:space-between}
.div .st{font-family:'Black Han Sans';font-size:30pt;letter-spacing:.06em;opacity:.95}
.div h1{font-family:'Black Han Sans';font-size:44pt;margin:4mm 0 2mm;font-weight:400;line-height:1.1}
.div p{font-size:12pt;opacity:.95;margin:0}
.div .big{position:absolute;right:-10mm;bottom:-22mm;font-family:'Black Han Sans';font-size:230pt;opacity:.13;line-height:1}
.div table{border-collapse:collapse;background:rgba(255,255,255,.14);border-radius:10px;overflow:hidden;width:100%;font-size:11pt}
.div td,.div th{padding:7px 12px;border-bottom:1px solid rgba(255,255,255,.25);text-align:left}
/* running header */
.rh{display:flex;align-items:center;gap:8px;border-bottom:2.5px solid var(--c);padding-bottom:4px;margin-bottom:8px}
.rh .tg{background:var(--c);color:#fff;font-family:'Black Han Sans';font-size:12pt;padding:1px 10px;border-radius:5px}
.rh .tt{font-weight:900;font-size:11pt}
.rh .rng{margin-left:auto;font-size:8.5pt;color:#666}
.area{column-span:all;display:flex;align-items:center;gap:8px;margin:6px 0 8px;break-after:avoid}
.area span{background:var(--l);color:var(--c);border:1.5px solid var(--c);font-weight:900;border-radius:14px;padding:1px 12px;font-size:9.5pt}
.area i{flex:1;border-top:1px dashed #bbb}
.cols{columns:2;column-gap:9mm;column-rule:1px solid #d5d9e0}
.grp{margin:0 0 9px}.grp .gh{break-after:avoid}.psg .sec{position:relative;padding-left:30px;margin:2px 0 7px}.psg .sec+.sec{border-top:1px dashed #b8bec8;padding-top:7px}.psg .lb{position:absolute;left:0;top:0;font-weight:900;font-family:'Noto Sans KR'}.psg .sec+.sec .lb{top:7px}.psg .poem div{min-height:1.2em}.psg .sgap{height:.7em}.psg .prose p{margin:0 0 3px;text-indent:.7em;text-align:left;word-break:normal;line-break:strict}.psg .au2{text-align:right;font-family:'Noto Sans KR';font-size:8pt;color:#555;margin-top:2px}.psg .pnote{font-family:'Noto Sans KR';font-size:7.4pt;color:#555;margin-top:3px;line-height:1.45}.psg .mk{font-family:'Noto Sans KR';font-weight:700;margin-right:1px}.psg u{text-underline-offset:2px}.psg .pf{margin:2px 0 4px;text-indent:0;break-inside:avoid}.psg .pf.r{float:right;margin-left:8px}.psg .pf.l{float:left;margin-right:8px}.psg .pf img{width:100%;display:block;border:1px solid #bbb}.psg .pf figcaption{font-family:'Noto Sans KR';font-size:6.6pt;color:#444;line-height:1.3;margin-top:2px;text-indent:0}.given{border:1px solid #9aa1ad;background:#f7f8fa;border-radius:3px;padding:5px 8px;margin:5px 0 2px;font-weight:400;font-size:8.8pt}
.grp .gh{font-weight:700;margin-bottom:4px}
.psg{border:1px solid #9aa1ad;padding:7px 10px;font-family:'Noto Serif KR',serif;font-size:9pt;line-height:1.7;background:#fcfcfa}
.psg .au{float:right;font-family:'Noto Sans KR';font-size:8pt;color:#555}
.q{break-inside:avoid;margin:0 0 13px}
.qh{display:flex;gap:6px}
.qn{font-family:'Black Han Sans';font-size:14pt;line-height:1.05;color:var(--c);min-width:30px}
.qt{flex:1}
.tag{display:inline-block;font-size:7.3pt;font-weight:700;border-radius:3px;padding:0 5px;margin-right:4px;vertical-align:1px;border:1px solid}
.t-학습지{color:#b25e00;border-color:#e3a45a;background:#fff4e6}.t-빈출{color:#c2334a;border-color:#ee9aa8;background:#fdecee}
.t-필기{color:#7a3a8a;border-color:#c79ad3;background:#f6ecf9}.t-함정{color:#fff;background:#c2334a;border-color:#c2334a}
.t-고난도{color:#fff;background:#222;border-color:#222}.t-교과서{color:#1f7a5a;border-color:#8fd0b5;background:#e9f7f1}
.t-외적{color:#2f6fd6;border-color:#9bbcf0;background:#eaf2fd}.t-서술형{color:#fff;background:#b77a00;border-color:#b77a00}
.box{border:1px solid #8e95a1;border-radius:3px;padding:6px 9px;margin:6px 0 5px 36px;font-size:8.9pt;position:relative}
.box.bogi{padding-top:9px}.box.bogi:before{content:'보기';position:absolute;top:-8px;left:50%;transform:translateX(-50%);background:#fff;padding:0 6px;font-size:8pt;font-weight:700}
.ch{list-style:none;padding:0;margin:5px 0 0 36px;display:grid;gap:1px 8px;font-size:9pt}
.ch.g1{grid-template-columns:1fr}.ch.g3{grid-template-columns:repeat(3,1fr)}.ch.g5{grid-template-columns:repeat(5,auto)}
.ans{margin:6px 0 0 36px}.ans div{border-bottom:1px dashed #aab;height:21px}
.ans .lab{font-size:8pt;color:#888}
/* front matter */
.fm h2{font-family:'Black Han Sans';font-weight:400;font-size:20pt;margin:0 0 6px}
.fm .lead{color:#555;margin:0 0 12px}
.feat{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px}
.feat div{border-radius:10px;padding:10px 12px;color:#fff}
.feat b{display:block;font-family:'Black Han Sans';font-weight:400;font-size:14pt}
.tbl{width:100%;border-collapse:collapse;font-size:9pt;margin:6px 0 12px}
.tbl th,.tbl td{border:1px solid #cfd5dd;padding:5px 7px}
.tbl th{background:#f0f2f6}
.tbl td.c{text-align:center}
.tags{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 12px}
/* answers */
.quick{display:grid;grid-template-columns:repeat(10,1fr);border-top:2px solid #222;border-left:1px solid #ccc;margin-bottom:10px}
.quick div{border-right:1px solid #ccc;border-bottom:1px solid #ccc;padding:2px 3px;font-size:8.3pt;display:flex;gap:4px;min-height:21px;align-items:center}
.quick b{font-family:'Black Han Sans';font-weight:400;color:#888;min-width:22px}
.quick span{font-weight:700;color:#c2334a}
.quick .sa{color:#b77a00;font-size:7.5pt}
.exp{columns:2;column-gap:8mm;column-rule:1px solid #ddd;font-size:8.6pt}
.exp .e{break-inside:avoid;margin:0 0 7px;padding-bottom:5px;border-bottom:1px dotted #ccc}
.exp .e b.n{font-family:'Black Han Sans';font-weight:400;font-size:11pt;margin-right:5px;color:var(--c)}
.exp .e .a{font-weight:900;color:#c2334a;margin-right:6px}
.shd{font-family:'Black Han Sans';font-weight:400;font-size:15pt;margin:4px 0 6px;padding:3px 10px;color:#fff;border-radius:6px;column-span:all;break-after:avoid}
"""

from cover import COVER


def ch_cls(ch):
    m = max(len(re.sub('<[^>]+>', '', c)) for c in ch)
    return 'g5' if m <= 5 else ('g3' if m <= 7 else 'g1')


def tagh(t):
    if not t:
        return ''
    k = t.split()[0]
    return f'<span class="tag t-{k}">{t}</span>'


def render_q(n, d):
    s = f'<div class="q"><div class="qh"><div class="qn">{n:02d}</div><div class="qt">{tagh(d.get("tag"))}{d["q"]}</div></div>'
    if d.get('box'):
        s += f'<div class="box{" bogi" if d.get("bogi") else ""}">{d["box"]}</div>'
    if d['kind'] == 'mc':
        s += f'<ul class="ch {ch_cls(d["ch"])}">' + ''.join(f'<li>{C[i]} {c}</li>' for i, c in enumerate(d['ch'])) + '</ul>'
    else:
        s += '<div class="ans">' + '<div></div>' * d.get('lines', 1) + '</div>'
    return s + '</div>'


def build_body():
    out, key, n = [], [], 0
    # front matter
    total = {st.key: st.count() for st in STAGES}
    area_cnt = {st.key: {a: sum(1 for it in st.items if it[0] == 'q' and it[1]['area'] == a) for a in AREAS} for st in STAGES}
    rows = ''.join(f'<tr><td><b style="color:{COL[st.key][0]}">{st.name}</b> {st.title}</td>' + ''.join(f'<td class="c">{area_cnt[st.key][a]}</td>' for a in AREAS) + f'<td class="c"><b>{total[st.key]}</b></td></tr>' for st in STAGES)
    tot_a = ''.join(f'<td class="c"><b>{sum(area_cnt[k][a] for k in area_cnt)}</b></td>' for a in AREAS)
    out.append(f'''<section class="fm"><h2>이 책의 구성과 특징</h2><p class="lead">위례한빛중 3학년 2학기 국어 학습지(학습지 11~13, 수업 필기)와 교과서 내용을 바탕으로, 시험에 나올 수 있는 문항을 4단계로 나누어 222문항을 실었습니다.</p>
<div class="feat"><div style="background:#1f9d62"><b>STEP 1 기본</b>작품 정보·어휘·용어·개념을 한 문제씩 확인합니다.</div><div style="background:#2f6fd6"><b>STEP 2 응용</b>지문 속 시어·구절·문장에 개념을 적용합니다.</div>
<div style="background:#7e57c2"><b>STEP 3 발전</b>작품 비교, 오류 구별, 서술형으로 한 단계 올라갑니다.</div><div style="background:#d6334a"><b>STEP 4 심화</b>함정 선지·외적 준거·복합 문법으로 실전 감각을 완성합니다.</div></div>
<h2 style="font-size:15pt">단계별 · 단원별 문항 수</h2><table class="tbl"><tr><th>단계</th>{''.join(f'<th>{AREA_FULL[a]}</th>' for a in AREAS)}<th>합계</th></tr>{rows}<tr><td><b>합계</b></td>{tot_a}<td class="c"><b>222</b></td></tr></table>
<h2 style="font-size:15pt">문항 표시</h2><div class="tags">{''.join(tagh(t) for t in ['학습지','교과서','필기','빈출','함정','고난도','외적 준거','서술형'])}</div>
<p style="font-size:8.8pt;color:#444;margin:-4px 0 12px">학습지 = 학습지 빈칸·확인 문제를 그대로 또는 조건만 바꿔 출제 · 필기 = 수업 필기에만 있던 포인트 · 함정 = 학습지 함정표 유형 · 외적 준거 = &lt;보기&gt;를 참고해 감상하는 유형</p>
<h2 style="font-size:15pt">학습 계획 · 채점표</h2><table class="tbl"><tr><th>단계</th><th>문항</th><th>푼 날짜</th><th>맞은 개수</th><th>틀린 문항 번호</th></tr>''' +
               ''.join(f'<tr><td><b style="color:{COL[st.key][0]}">{st.name}</b></td><td class="c">{rng}</td><td></td><td class="c">/ {total[st.key]}</td><td style="height:28px"></td></tr>' for st, rng in zip(STAGES, ['01~56', '57~114', '115~170', '171~222'])) +
               '</table><p style="font-size:8.8pt;color:#555">권장 시간: 객관식 1문항 1분, 서술형 3분 · 틀린 문항은 해설의 핵심 한 줄을 소리 내어 읽고 다음 날 다시 풀기.</p></section>')

    for st in STAGES:
        c, l = COL[st.key]
        first = n + 1
        last = n + st.count()
        cnt = area_cnt[st.key]
        out.append(f'<section class="pb div" style="background:linear-gradient(145deg,{c},{c}cc)"><div><div class="st">{st.name}</div><h1>{st.title.split(" — ")[0]}<br>{st.title.split(" — ")[1]}</h1><p>{st.desc}</p></div>'
                   f'<table><tr><th>단원</th><th>문항 수</th></tr>' + ''.join(f'<tr><td>{AREA_FULL[a]}</td><td>{cnt[a]}문항</td></tr>' for a in AREAS) + f'<tr><td><b>문항 번호</b></td><td><b>{first:02d} ~ {last}</b></td></tr></table><div class="big">{st.name[-1]}</div></section>')
        body, cur_area = [], None
        items = st.items
        i = 0
        while i < len(items):
            it = items[i]
            if it[0] == 'grp':
                _, area, header, psg = it
                if area != cur_area:
                    body.append(f'<div class="area"><span>{AREA_FULL[area]}</span><i></i></div>'); cur_area = area
                j, k = i + 1, 0
                while j < len(items) and items[j][0] == 'q':
                    k += 1; j += 1
                if header:
                    h = re.sub(r'^\[[^\]]*\]\s*', '', header)
                    body.append(f'<div class="grp"><div class="gh">[{n + 1:02d}~{n + k:02d}] {h}</div>' + (f'<div class="psg">{psg}</div>' if psg else '') + '</div>')
                i += 1; continue
            d = it[1]
            if d['area'] != cur_area:
                body.append(f'<div class="area"><span>{AREA_FULL[d["area"]]}</span><i></i></div>'); cur_area = d['area']
            n += 1
            body.append(render_q(n, d))
            key.append((n, st, d))
            i += 1
        out.append(f'<section class="pb" style="--c:{c};--l:{l}"><div class="rh"><span class="tg">{st.name}</span><span class="tt">{st.title}</span><span class="rng">{first:02d} ~ {last}</span></div><div class="cols">{"".join(body)}</div></section>')

    # answers
    qk = ''.join(f'<div><b>{m:03d}</b>' + (f'<span>{C[d["a"] - 1]}</span>' if d['kind'] == 'mc' else '<span class="sa">해설 참고</span>') + '</div>' for m, st, d in key)
    out.append(f'<section class="pb"><div class="rh" style="--c:#222"><span class="tg">정답과 해설</span><span class="tt">빠른 정답 222</span></div><div class="quick">{qk}</div><p style="font-size:8.5pt;color:#666">단답·서술형은 다음 쪽 해설의 모범 답안을 참고하세요. 서술형은 핵심어가 모두 들어가면 정답으로 채점합니다.</p></section>')
    exp = []
    for st in STAGES:
        c, _ = COL[st.key]
        exp.append(f'<div class="shd" style="background:{c}">{st.name} {st.title}</div>')
        for m, s_, d in key:
            if s_ is not st:
                continue
            a = C[d['a'] - 1] if d['kind'] == 'mc' else ('모범 답안' if d['a'].startswith('서술형') else d['a'])
            e = d.get('e') or ''
            exp.append(f'<div class="e" style="--c:{c}"><b class="n">{m:03d}</b><span class="a">{a}</span>{e}</div>')
    out.append(f'<section class="pb"><div class="rh" style="--c:#222"><span class="tg">정답과 해설</span><span class="tt">문항별 해설</span></div><div class="exp">{"".join(exp)}</div></section>')
    return ''.join(out)


from cover import BACK

JS = """
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(process.argv[2]);
  const b = await chromium.launch(); const p = await b.newPage();
  for (const [html, pdf, foot] of jobs) {
    await p.goto('file://' + html, { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    const o = { path: pdf, format: 'A4', printBackground: true, preferCSSPageSize: true };
    if (foot) { o.displayHeaderFooter = true; o.headerTemplate = '<span></span>';
      o.footerTemplate = '<div style="width:100%;font-size:7.5px;color:#888;font-family:Noto Sans KR;display:flex;justify-content:space-between;padding:0 12mm"><span>국어 기출 222 · 중3 2학기 1차 정기시험 대비</span><span class="pageNumber"></span></div>'; }
    await p.pdf(o);
  }
  await b.close();
})();
"""


def main():
    tmp = tempfile.mkdtemp()
    parts = [('cover', COVER, False), ('body', f'<style>{CSS}</style>' + build_body(), True), ('back', BACK, False)]
    jobs = []
    for name, html, foot in parts:
        h = os.path.join(tmp, name + '.html')
        open(h, 'w', encoding='utf-8').write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"></head><body>{html}</body></html>')
        jobs.append([h, os.path.join(tmp, name + '.pdf'), foot])
    js = os.path.join(tmp, 'r.js'); open(js, 'w').write(JS)
    root = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
    subprocess.run(['node', js, json.dumps(jobs)], check=True, env={**os.environ, 'NODE_PATH': root})
    res = pymupdf.open()
    for _, pdf, _ in jobs:
        res.insert_pdf(pymupdf.open(pdf))
    res.set_metadata({'title': '국어 기출 222'})
    res.save(OUT, garbage=4, deflate=True)
    print(OUT, res.page_count, os.path.getsize(OUT) // 1024, 'KB')


if __name__ == '__main__':
    main()
