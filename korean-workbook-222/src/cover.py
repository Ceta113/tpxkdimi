"""표지·뒤표지 (화이트 + 네이비, 미니멀)."""
NAVY = '#14213d'

COVER = """
<style>@page{size:A4;margin:0}body{margin:0}*{box-sizing:border-box}
.cv{width:210mm;height:297mm;position:relative;overflow:hidden;background:#fbfaf7;color:#111;font-family:'Noto Sans KR'}
.cv .g{position:absolute;left:24mm;top:26mm;font-size:10pt;font-weight:500;letter-spacing:.3em;color:#6b7280}
.cv h1{position:absolute;left:22mm;top:52mm;margin:0;font-family:'Noto Serif KR';font-weight:900;font-size:112pt;line-height:1.08;letter-spacing:-.03em}
.cv .rule{position:absolute;left:24mm;top:152mm;width:22mm;height:1.4mm;background:#14213d}
.cv .sub{position:absolute;left:24mm;top:160mm;font-size:13pt;font-weight:500;color:#374151;letter-spacing:.04em}
.cv .blk{position:absolute;left:0;right:0;bottom:0;height:92mm;background:#14213d;color:#fff}
.cv .num{position:absolute;left:21mm;bottom:14mm;font-family:'Cormorant Garamond';font-weight:700;font-size:150pt;line-height:.8;letter-spacing:-.02em}
.cv .ed{position:absolute;right:22mm;bottom:18mm;text-align:right;font-size:8.5pt;letter-spacing:.2em;color:#aab3c5;line-height:1.9}
</style>
<div class="cv">
 <div class="g">중학 국어 3-2</div>
 <h1>국어<br>기출</h1>
 <div class="rule"></div>
 <div class="sub">2학기 1차 정기시험 대비</div>
 <div class="blk"><div class="num">222</div><div class="ed">4단계 완성<br>정답과 해설</div></div>
</div>"""

_items = [
 '시조 종장 첫 음보는 <b>3음절</b> — 사설시조(모쳐라)도 지킨다',
 '어린 = <b>어리석은</b> · 만중운산 = <b>공간적</b> · 월침삼경 = <b>시간적·시각</b> · 낸들 어이하리오 = <b>설의법</b>',
 '어져 = <b>감탄사(영탄법)</b> · 제 구태여 = 임이면 <b>도치</b>, 나면 <b>행간 걸침</b>',
 '위렁충창 = <b>의성어</b> · 곰븨님븨·천방지방 = <b>의태어</b> · 주추리 삼대 = 착각 대상',
 "연탄 한 장: 촉각·<b>청각</b> 이미지, '-네', 도치(몰랐었네, 나는), 시선 외부→내면",
 '담쟁이: 오른다→나아간다→올라간다→넘는다(<b>점층</b>), 푸르게 = <b>희망</b>, 잎 하나 = <b>선구자</b>',
 '기다려라: 서론 <b>연역</b> · 본론 <b>귀납</b>(브레송·세잔·정선) · 결론 <b>유추</b>(음식 ≈ 삶)',
 '오류: 허수아비 = 바꿔 치기 / 비탈길 = 연쇄 / 결합 = 부분 합침 / 성급한 일반화 = 소수 사례',
 "보어 = <b>되다·아니다</b> 앞 '이/가' · 주어+[주어+서술어] = <b>서술절</b>",
 "-이(없이) = 품사 변화 O / -게(나게) = 품사 변화 X · 간접 인용 = 조사 '고'"]

BACK = """<style>@page{size:A4;margin:0}body{margin:0}*{box-sizing:border-box}
.bk{width:210mm;height:297mm;position:relative;background:#fbfaf7;color:#111;font-family:'Noto Sans KR';padding:30mm 24mm}
.bk h2{margin:0;font-family:'Noto Serif KR';font-weight:900;font-size:22pt}
.bk .rule{width:18mm;height:1.2mm;background:#14213d;margin:6mm 0 8mm}
.bk ol{margin:0;padding-left:6mm;font-size:10.6pt;line-height:2.1;color:#222}
.bk b{color:#14213d}
.bk .blk{position:absolute;left:0;right:0;bottom:0;height:22mm;background:#14213d}
</style><div class="bk"><h2>시험장 들어가기 전 마지막 체크</h2><div class="rule"></div><ol>""" + ''.join(f'<li>{t}</li>' for t in _items) + """</ol><div class="blk"></div></div>"""
