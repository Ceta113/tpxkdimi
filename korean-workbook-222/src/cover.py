"""표지·뒤표지 (네이비 + 골드, 미니멀)."""

_rings = ''.join(f'<circle cx="168" cy="112" r="{r}" fill="none" stroke="#c9a96a" stroke-width="{0.35 if r % 20 else 0.6}" opacity="{0.5 - r / 400:.2f}"/>' for r in range(18, 190, 10))
_ticks = ''.join(f'<line x1="{x}" y1="286" x2="{x}" y2="{283 if x % 10 else 281}" stroke="#c9a96a" stroke-width="0.3" opacity=".7"/>' for x in range(22, 189, 2))

COVER = f"""
<style>@page{{size:A4;margin:0}}body{{margin:0}}*{{box-sizing:border-box}}
.cv{{width:210mm;height:297mm;position:relative;overflow:hidden;background:#0f1724;color:#f4efe4;font-family:'Noto Sans KR'}}
.cv svg.bg{{position:absolute;left:0;top:0;width:210mm;height:297mm}}
.cv .ser{{position:absolute;left:22mm;top:21mm;font-family:Montserrat;font-weight:700;font-size:8pt;letter-spacing:.42em;color:#c9a96a}}
.cv .yr{{position:absolute;right:20mm;top:21mm;font-family:Montserrat;font-weight:500;font-size:8pt;letter-spacing:.3em;color:#8a93a3}}
.cv svg.num{{position:absolute;left:0;top:0;width:210mm;height:297mm}}
.cv .ttl{{position:absolute;left:22mm;top:150mm}}
.cv .ttl .g{{font-size:11pt;font-weight:500;color:#a9b1bf;letter-spacing:.18em}}
.cv .ttl h1{{margin:3mm 0 0;font-family:'Noto Serif KR';font-weight:900;font-size:76pt;line-height:1.02;letter-spacing:-.02em;color:#f4efe4}}
.cv .ttl h1 span{{color:#c9a96a}}
.cv .ttl .rule{{width:34mm;height:1.2mm;background:#c9a96a;margin:7mm 0 5mm}}
.cv .ttl .sub{{font-size:13pt;font-weight:500;letter-spacing:.06em}}
.cv .steps{{position:absolute;left:22mm;top:236mm;display:flex;gap:7mm;font-family:Montserrat;font-size:7.5pt;letter-spacing:.22em;color:#a9b1bf;font-weight:500}}
.cv .steps i{{display:inline-block;width:2.2mm;height:2.2mm;border-radius:50%;margin-right:2mm;vertical-align:.2mm}}
.cv .foot{{position:absolute;left:22mm;right:20mm;top:262mm;border-top:.3mm solid #c9a96a;padding-top:4mm;display:flex;justify-content:space-between;align-items:flex-end}}
.cv .nm{{font-family:Montserrat;font-size:7.5pt;letter-spacing:.3em;color:#8a93a3}}
.cv .nm b{{display:inline-block;width:52mm;border-bottom:.25mm solid #5d6778;margin-left:3mm}}
.cv .ed{{text-align:right;font-family:'Cormorant Garamond';font-weight:500;font-size:13pt;color:#c9a96a;letter-spacing:.08em}}
.cv .ed small{{display:block;font-family:'Noto Sans KR';font-size:6.8pt;color:#8a93a3;letter-spacing:.05em}}
.cv .side{{position:absolute;left:10mm;top:150mm;transform-origin:left top;transform:rotate(-90deg);font-family:Montserrat;font-size:6.5pt;letter-spacing:.5em;color:#5d6778;white-space:nowrap}}
</style>
<div class="cv">
 <svg class="bg" viewBox="0 0 210 297" preserveAspectRatio="none">{_rings}{_ticks}
  <line x1="16" y1="18" x2="16" y2="279" stroke="#c9a96a" stroke-width="0.25" opacity=".55"/></svg>
 <div class="ser">KOREAN · EXAM MASTER</div><div class="yr">2026</div>
 <svg class="num" viewBox="0 0 210 297"><defs><linearGradient id="gd" x1="0" y1="0" x2="0.25" y2="1"><stop offset="0" stop-color="#f1dfae"/><stop offset=".5" stop-color="#c9a96a"/><stop offset="1" stop-color="#8f6f36"/></linearGradient></defs><text x="197" y="128" text-anchor="end" font-family="Cormorant Garamond" font-weight="700" font-size="104" letter-spacing="-3" fill="url(#gd)">222</text></svg>
 <div class="side">MIDDLE SCHOOL KOREAN 3-2</div>
 <div class="ttl"><div class="g">중학 국어 3-2</div><h1>국어<br><span>기출</span></h1><div class="rule"></div><div class="sub">2학기 1차 정기시험 대비</div></div>
 <div class="steps"><span><i style="background:#1f9d62"></i>BASIC</span><span><i style="background:#2f6fd6"></i>APPLY</span><span><i style="background:#7e57c2"></i>ADVANCE</span><span><i style="background:#d6334a"></i>MASTER</span></div>
 <div class="foot"><div class="nm">NAME<b></b></div><div class="ed">Self Study Edition<small>개인 학습용</small></div></div>
</div>"""

BACK = f"""<style>@page{{size:A4;margin:0}}body{{margin:0}}*{{box-sizing:border-box}}</style>
<div style="width:210mm;height:297mm;background:#0f1724;color:#f4efe4;font-family:'Noto Sans KR';position:relative;padding:30mm 22mm;overflow:hidden">
<svg style="position:absolute;left:0;top:0;width:210mm;height:297mm" viewBox="0 0 210 297">{_rings.replace('cx="168" cy="112"', 'cx="40" cy="250"')}</svg>
<div style="position:relative;font-family:Montserrat;font-weight:700;font-size:8pt;letter-spacing:.42em;color:#c9a96a">LAST CHECK</div>
<div style="position:relative;font-family:'Noto Serif KR';font-weight:900;font-size:24pt;margin:3mm 0 2mm">시험장 들어가기 전 마지막 체크</div>
<div style="position:relative;width:26mm;height:1mm;background:#c9a96a;margin-bottom:7mm"></div>
<ol style="position:relative;font-size:10.8pt;line-height:2.05;padding-left:6mm;margin:0">
<li>시조 종장 첫 음보는 <b style="color:#e3c98f">3음절</b> — 사설시조(모쳐라)도 지킨다</li>
<li>어린 = <b style="color:#e3c98f">어리석은</b> · 만중운산 = <b style="color:#e3c98f">공간적</b> · 월침삼경 = <b style="color:#e3c98f">시간적·시각</b> · 낸들 어이하리오 = <b style="color:#e3c98f">설의법</b></li>
<li>어져 = <b style="color:#e3c98f">감탄사(영탄법)</b> · 제 구태여 = 임이면 <b style="color:#e3c98f">도치</b>, 나면 <b style="color:#e3c98f">행간 걸침</b></li>
<li>위렁충창 = <b style="color:#e3c98f">의성어</b> · 곰븨님븨·천방지방 = <b style="color:#e3c98f">의태어</b> · 주추리 삼대 = 착각 대상</li>
<li>연탄 한 장: 촉각·<b style="color:#e3c98f">청각</b> 이미지, '-네', 도치(몰랐었네, 나는), 시선 외부→내면</li>
<li>담쟁이: 오른다→나아간다→올라간다→넘는다(<b style="color:#e3c98f">점층</b>), 푸르게 = <b style="color:#e3c98f">희망</b>, 잎 하나 = <b style="color:#e3c98f">선구자</b></li>
<li>기다려라: 서론 <b style="color:#e3c98f">연역</b> · 본론 <b style="color:#e3c98f">귀납</b>(브레송·세잔·정선) · 결론 <b style="color:#e3c98f">유추</b>(음식 ≈ 삶)</li>
<li>오류: 허수아비 = 바꿔 치기 / 비탈길 = 연쇄 / 결합 = 부분 합침 / 성급한 일반화 = 소수 사례</li>
<li>보어 = <b style="color:#e3c98f">되다·아니다</b> 앞 '이/가' · 주어+[주어+서술어] = <b style="color:#e3c98f">서술절</b></li>
<li>-이(없이) = 품사 변화 O / -게(나게) = 품사 변화 X · 간접 인용 = 조사 '고'</li></ol>
<div style="position:absolute;right:16mm;bottom:14mm;font-family:'Cormorant Garamond';font-weight:700;font-size:92pt;line-height:1;color:#c9a96a;opacity:.35">222</div>
<div style="position:absolute;left:22mm;right:22mm;bottom:22mm;border-top:.3mm solid #c9a96a;padding-top:3mm;font-family:Montserrat;font-size:7pt;letter-spacing:.3em;color:#8a93a3">KOREAN · EXAM MASTER · SELF STUDY EDITION</div>
</div>"""
