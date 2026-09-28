"""국어 정리노트 보충 페이지 생성 (손글씨 필기 반영)."""
CSS = """
@page{size:A4;margin:12mm 12mm 16mm}
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;font-family:'Noto Sans KR',sans-serif;color:#1d1f24;font-size:9.3pt;line-height:1.55;word-break:keep-all}
.card{border:1px solid #d9dde5;border-radius:9px;margin:0 0 12px;overflow:hidden;break-inside:auto}
.card.s{border-color:#f0b9c4}.card.s .hd{background:#fde8ec}.card.s .bd{background:#d6334a}
.card.d{border-color:#cdbdf0}.card.d .hd{background:#f1ebfd}.card.d .bd{background:#7e57c2}
.card.a{border-color:#b9d3f5}.card.a .hd{background:#eaf2fd}.card.a .bd{background:#2f6fd6}
.card.b{border-color:#b8e0c8}.card.b .hd{background:#e8f6ee}.card.b .bd{background:#1f9d62}
.card.p{border-color:#e4b7d4}.card.p .hd{background:#fbeaf5}.card.p .bd{background:#b0356a}
.hd{display:flex;align-items:center;gap:8px;padding:6px 10px;break-after:avoid}
.bd{color:#fff;font-weight:700;font-size:8.2pt;border-radius:5px;padding:1px 7px}
.hd h3{margin:0;font-size:11.5pt}
.hd .src{margin-left:auto;font-size:7.8pt;color:#7a3a8a;background:#f6ecf9;border-radius:10px;padding:1px 8px}
.in{padding:6px 11px 10px}
table{width:100%;border-collapse:collapse;margin:6px 0;font-size:8.8pt}
th,td{border:1px solid #d3d9e0;padding:4px 6px;vertical-align:top;text-align:left}
th{background:#e3eff3;text-align:center}
td.c{text-align:center}
tr{break-inside:avoid}
b{font-weight:700}.r{color:#c2334a;font-weight:700}.bl{color:#2f6fd6;font-weight:700}
.tip{background:#fff8e6;border:1px solid #f0dca6;border-radius:7px;padding:6px 10px;margin:7px 0;break-inside:avoid}
.tip .l{color:#b77a00;font-weight:700;font-size:8pt;margin-right:5px}
.memo{background:#f7f0fb;border-left:4px solid #9b6bc0;border-radius:0 7px 7px 0;padding:6px 10px;margin:7px 0;break-inside:avoid}
.memo .l{color:#7a3a8a;font-weight:700;font-size:8pt;margin-right:5px}
.warn{background:#fdecee;border:1px solid #f1a9b3;border-radius:7px;padding:6px 10px;margin:7px 0;break-inside:avoid}
.warn .l{color:#c2334a;font-weight:700;font-size:8pt;margin-right:5px}
.vs{display:grid;grid-template-columns:1fr 34px 1fr;gap:0;align-items:stretch;margin:6px 0;break-inside:avoid}
.vs>div{border:1px solid #d3d9e0;border-radius:7px;padding:6px 9px}
.vs .m{border:none;display:flex;align-items:center;justify-content:center;font-weight:900;color:#888}
.vs h4{margin:0 0 3px;font-size:10pt}
ul{margin:3px 0;padding-left:17px}li{margin:1px 0}
.banner{border-radius:10px;padding:12px 16px;color:#fff;background:linear-gradient(90deg,#7a3a8a,#b0356a);margin-bottom:12px}
.banner .k{font-size:8pt;letter-spacing:.2em;opacity:.9;font-weight:700}
.banner h2{margin:2px 0;font-size:17pt}
.banner p{margin:0;font-size:9pt;opacity:.95}
.q{break-inside:avoid;margin:0 0 11px}
.q .h{font-weight:500}.q .n{font-weight:900;margin-right:6px}
.tag{font-size:7.5pt;color:#fff;border-radius:4px;padding:0 5px;margin-right:4px;vertical-align:1px}
.t-a{background:#2f6fd6}.t-d{background:#7e57c2}.t-s{background:#d6334a}.t-w{background:#b77a00}
.box{border:1px solid #9aa1ad;border-radius:6px;padding:5px 9px;margin:5px 0;font-size:9pt}
.ch{list-style:none;padding:0;margin:4px 0;font-size:9pt}
.cols{columns:2;column-gap:16px;column-rule:1px solid #e3e6ec}
.line{border-bottom:1px dashed #b9bfca;height:20px}
.ak td:first-child{width:36px;text-align:center;font-weight:700}
.ak td:nth-child(2){width:24%;color:#c2334a;font-weight:700}
.pb{break-before:page}
"""

def card(kind, badge, title, body, src='✎ 필기 반영'):
    return f'<section class="card {kind}"><div class="hd"><span class="bd">{badge}</span><h3>{title}</h3><span class="src">{src}</span></div><div class="in">{body}</div></section>'


def page(body):
    return f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'


# ------------------------------------------------------------------ S1 시조
S1 = card('d', '발전', '필기 비교 ① 「어져 내 일이야」 vs 「마음이 어린 후이니」', '''
<p>필기에서 두 작품을 직접 맞세운 비교. 둘 다 <b>자신을 탓하는 시조</b>지만 탓하는 이유와 정서가 다르다.</p>
<table><tr><th style="width:20%">비교 기준</th><th>어져 내 일이야 (황진이)</th><th>마음이 어린 후이니 (서경덕)</th></tr>
<tr><td>핵심 정서</td><td><b>후회 · 자책 · 미련</b> → 그리움</td><td><b>기다림 · 그리움</b> (자책 → 체념 → 착각)</td></tr>
<tr><td>화자가 탓하는 것</td><td><b>임을 보낸 자신</b>을 원망 ("내 일이야" = 내가 한 일)</td><td>모든 소리를 <b>임이 온 것이라 착각하는</b> 자신의 어리석음 ("어린" = 어리석은)</td></tr>
<tr><td>시간의 방향</td><td>이미 한 일(임을 보냄)을 <b>돌아봄</b></td><td>지금 임을 <b>기다림</b></td></tr>
<tr><td>시작 방식</td><td>감탄사 '어져' → <b>영탄법</b></td><td>'하는 일이 다 어리다' → <b>일반적 진술</b></td></tr>
<tr><td>핵심 표현</td><td>중장 '제 구태여'의 <b>중의성</b> (임=도치 / 나=행간 걸침)</td><td>'만중운산'(공간적 배경), 자연물(지는 잎·부는 바람)</td></tr></table>
<div class="warn"><span class="l">주의</span>필기의 "임 보낸 <b>자신을</b> 원망"은 맞는 말이다. 하지만 "화자가 <b>임을</b> 원망한다"는 틀린 선지(이 노트 9쪽 시조 함정표). 원망의 대상이 <b>자기 자신</b>이라는 점만 기억.</div>''')
S1 += card('d', '발전', '필기 흐름 ② 시조 4수 — 화자 태도 한 줄 암기', '''
<table><tr><th style="width:24%">작품</th><th>초장</th><th>중장</th><th>종장</th></tr>
<tr><td>마음이 어린 후이니</td><td>일반 진술 · <b>자신의 어리석음 자책</b></td><td>구체 진술 · 임이 올 수 없다는 <b>체념</b>과 그리움 (만중운산 = 임이 찾아오기 어려움 → 심리적·정서적 거리감)</td><td>자연물 소재 · 작은 소리에도 임이 온 것으로 <b>착각</b> ("나뭇잎 떨어지는 소리, 바람 부는 소리가 임 오는 소리 아닐까?")</td></tr>
<tr><td>어져 내 일이야</td><td>영탄법 · 임을 떠나보낸 것에 대한 <b>후회</b></td><td>임을 붙잡을 수 있었으리라는 <b>미련</b></td><td>떠난 임에 대한 <b>그리움</b></td></tr>
<tr><td>님이 오마 하거늘</td><td>임이 온다는 소식 듣고 <b>기다림</b></td><td>임을 만나러 <b>허겁지겁</b> 달려갔으나 착각임을 알게 됨</td><td>자신의 행동을 <b>부끄러워함</b> (감정 드러냄)</td></tr></table>
<div class="memo"><span class="l">✎ 필기</span>「님이 오마 하거늘」: <b>음성 상징어 → 과장 → 그리움</b>. '곰븨님븨 님븨곰븨'(의태어)에 필기로 "과장 - 그리움"이라고 적어 둠. 음성 상징어로 행동을 부풀려 그릴수록 임에 대한 그리움이 크게 느껴지는 구조. 초·중장은 <b>시간적 순서로 열거</b>, 종장은 <b>감정</b> → 사설시조 특유의 <b>낙천성·해학성</b>.</div>
<div class="memo"><span class="l">✎ 필기</span>해학을 만드는 장면 4가지: ① 버선과 신발을 벗어 들고 허둥지둥 달려감 ② 진 곳 마른 곳 가리지 않고 마구 달려감 ③ <b>주추리 삼대(일상적 소재)</b>가 자신을 속인 거라고 말함 ④ 남들이 자신의 행동을 보지 못해 다행이라 여김.</div>''')

# ------------------------------------------------------------------ S2 현대시
S2 = card('d', '발전', '필기 비교 ③ 「연탄 한 장」 vs 「담쟁이」 — 4가지 축', '''
<p>이 노트 15쪽 비교표에 없는 <b>필기만의 대비 축</b>. 서술형 "두 시의 차이점" 문제에 그대로 쓰기 좋다.</p>
<table><tr><th style="width:20%">축</th><th>연탄 한 장</th><th>담쟁이</th></tr>
<tr><td>대상의 결말</td><td>재가 되어 <b>소멸</b> (산산이 으깨져 길에 뿌려짐)</td><td>벽을 덮으며 <b>뻗어 나감 · 확장</b> (잎 하나 → 수천 개)</td></tr>
<tr><td>삶의 가치</td><td><b>자기희생</b> (나 아닌 그 누구에게)</td><td><b>연대</b> (여럿이 함께 손을 잡고)</td></tr>
<tr><td>화자의 태도</td><td><b>반성</b> (연탄 한 장도 되지 못하였네)</td><td><b>의지</b> (단호한 어조로 극복 의지 강조)</td></tr>
<tr><td>시간 방향</td><td><b>과거 · 성찰</b> (몰랐네, 몰랐었네 — 지난 삶을 돌아봄)</td><td><b>미래 · 목표</b> (결국 그 벽을 넘는다 — 나아갈 방향 제시)</td></tr></table>
<div class="vs"><div><h4>연탄 <span style="font-weight:500;font-size:8.5pt">희생적 존재, 박애적 사랑</span></h4><ul><li>몸에 불이 붙으면 하염없이 뜨거워짐</li><li>재가 되어도 산산이 으깨져 길에 뿌려짐</li></ul></div><div class="m">vs</div>
<div><h4>화자 <span style="font-weight:500;font-size:8.5pt">고마움 모르고 삶</span></h4><ul><li>매일 따스한 밥과 국물을 퍼먹음</li><li>한 덩이 재로 쓸쓸하게 남는 게 두려움</li></ul></div></div>
<div class="vs"><div><h4>담쟁이 <span style="font-weight:500;font-size:8.5pt">극복</span></h4><ul><li>말없이 벽을 오름 · 서두르지 않고 나아감</li><li>손 잡고 올라감 · 결국 벽을 넘음</li></ul></div><div class="m">vs</div>
<div><h4>우리 <span style="font-weight:500;font-size:8.5pt">체념</span></h4><ul><li>어쩔 수 없는 벽 · 절망의 벽</li><li>넘을 수 없는 벽이라고 고개 떨굼</li></ul></div></div>
<p style="font-size:8.6pt;color:#555">→ 둘 다 <b>벽(시련)을 대하는 태도</b> / <b>연탄을 대하는 태도</b>의 대비로 주제를 드러냄.</p>''')
S2 += card('d', '발전', '필기 순서대로 — 「연탄 한 장」 특징 9 · 「담쟁이」 특징 6', '''
<table><tr><th style="width:5%">#</th><th style="width:47%">연탄 한 장 (필기 순서)</th><th>근거 시어 · 효과</th></tr>
<tr><td class="c">1</td><td>일상적인 소재에 <b>상징적 의미</b> 부여</td><td>연탄 = 희생·이타</td></tr>
<tr><td class="c">2</td><td>이타적인 연탄과 이기적인 화자를 <b>대비</b> → 자기반성 강조</td><td>연탄 ↔ "따스한 밥과 국물 퍼먹으면서도 몰랐네"</td></tr>
<tr><td class="c">3</td><td><b>의인법</b> — 연탄의 모습을 효과적으로 표현</td><td>"해야 할 일이 무엇인가를 알고 있다는 듯이", "일단 <b>제</b> 몸에" ← 필기에서 '제'에 동그라미</td></tr>
<tr><td class="c">4</td><td><b>은유법</b></td><td>삶이란 … 연탄 한 장 되는 것</td></tr>
<tr><td class="c">5</td><td><b>도치법</b></td><td>"…몰랐었네, 나는" → 여운·반성</td></tr>
<tr><td class="c">6</td><td>종결 어미 <b>'-네'</b> → 운율 형성, <b>깨달음 전달</b>, 고백적 어조</td><td>거라네 · 몰랐네 · 못하였네 · 몰랐었네</td></tr>
<tr><td class="c">7</td><td>화자 시선: 연탄(<b>외부</b>) → 자신(<b>내면</b>) → 자아 성찰 심화</td><td>"몰랐네"부터 시선이 자신에게</td></tr>
<tr><td class="c">8</td><td><b>음성 상징어</b>로 생동감 부여</td><td>부릉부릉</td></tr>
<tr><td class="c">9</td><td><b>촉각적 · 청각적</b> 이미지 사용 <span class="r">(필기 표현)</span></td><td>촉각: 선득선득, 따스한, 뜨거워지는 / 청각: 부릉부릉</td></tr></table>
<div class="warn"><span class="l">확인 필요</span>필기 9번은 "<b>촉각적, 청각적</b> 이미지", 이 노트 12쪽 특징 4는 "<b>촉각적, 시각적</b> 이미지"로 서로 다르다. 학습지 빈칸 답을 한 번 확인하자. 시험 대비로는 <b>촉각(선득선득·따스한·뜨거워지는), 청각(부릉부릉), 시각(눈 내려 미끄러운 아침 · 한 덩이 재)</b>을 모두 근거 시어와 함께 알아 두면 어느 쪽으로 나와도 풀 수 있다. "청각적 이미지<b>만</b>" 같은 선지는 여전히 틀림.</div>
<table><tr><th style="width:5%">#</th><th style="width:47%">담쟁이 (필기 순서)</th><th>근거 · 효과</th></tr>
<tr><td class="c">1</td><td>일상적 소재 <b>벽, 담쟁이</b>에 상징적 의미 부여</td><td>벽 = 시련·절망 / 담쟁이 = 극복 의지</td></tr>
<tr><td class="c">2</td><td>담쟁이 <b>의인화</b> → 주제 의식 드러냄</td><td>말없이 오른다, 손을 잡고</td></tr>
<tr><td class="c">3</td><td>'~할 때 ~다' <b>유사한 통사 구조 반복</b> → <b>점층적</b>으로 제시</td><td>오른다 → 나아간다 → 올라간다 → 넘는다</td></tr>
<tr><td class="c">4</td><td><b>현재형 어미</b>로 생동감 부여</td><td>-ㄴ다</td></tr>
<tr><td class="c">5</td><td><b>단호한 어조</b>로 담쟁이의 의지 강조</td><td>"바로 그 절망을 잡고 놓지 않는다"</td></tr>
<tr><td class="c">6</td><td><b>색채어</b>로 이미지 선명하게 전달</td><td>"<b>푸르게</b> 절망을 다 덮을 때까지" → 벽을 다 덮은 푸른색 담쟁이(희망)</td></tr></table>
<div class="memo"><span class="l">✎ 필기 해설</span>「연탄 한 장」 — 연탄을 인간에 비유하여 바람직한 삶의 자세와 이타적인 사랑의 의미를 <b>교훈적으로</b> 형상화. 헌신적인 연탄과 달리 <b>개인주의</b>였던 자신의 모습을 성찰하여 반성. '-네'를 반복하여 운율을 형성하고 고백적인 어조를 드러냄.<br>「담쟁이」 — 1980~90년대 시대 상황을 반영하면 <b>집단적 연대</b>를 통해 사회적 변화를 추구하는 시대 정신 형상화. 잎 하나 = <b>선구자</b>적인 모습.</div>''')

# ------------------------------------------------------------------ S3 오류
S3 = card('d', '발전', '필기 이름 ↔ 노트 이름 대응 · 필기 한 줄 정의', '''
<p>필기와 2번 노트에서 <b>오류 이름이 다르게 적힌 것</b>이 5개 있다. 시험지에는 어느 이름이든 나올 수 있으니 둘 다 알아 두자.</p>
<table><tr><th style="width:5%">#</th><th style="width:22%">필기 이름</th><th style="width:22%">2번 노트 이름</th><th>필기 한 줄 정의 (암기용)</th></tr>
<tr><td class="c">1</td><td><b>결합</b>의 오류</td><td>합성(결합)의 오류</td><td>부분적으로는 옳은 주장들을 무리하게 합쳐 발생</td></tr>
<tr><td class="c">2</td><td>논점 일탈의 오류</td><td>같음</td><td>주장과 관련 없는 다른 내용을 끌어들여 발생</td></tr>
<tr><td class="c">3</td><td>피장파장의 오류</td><td>같음</td><td>주장이 옳은지 따지지 않고, 상대방도 똑같은 잘못을 하고 있다고 지적해 주장 자체를 무력화</td></tr>
<tr><td class="c">4</td><td>인신공격의 오류</td><td>같음</td><td>주장하는 사람의 인격·성격·배경을 공격해 주장을 무너뜨리려 함</td></tr>
<tr><td class="c">5</td><td>성급한 일반화의 오류</td><td>같음</td><td>소수의 사례만을 근거로 결론 지음</td></tr>
<tr><td class="c">6</td><td><b>이분법</b>의 오류</td><td>흑백 사고의 오류 (이분법적 사고)</td><td>더 많은 선택지가 있음에도 불구하고 둘뿐인 것처럼</td></tr>
<tr><td class="c">7</td><td>감정·동정에 호소하는 오류</td><td>같음</td><td>불쌍한 처지·억울함을 호소해 동정심을 유발하며 요구 사항을 주장</td></tr>
<tr><td class="c">8</td><td><b>군중</b>에 호소하는 오류</td><td>대중에 호소하는 오류</td><td>대중의 규모에 비추어 자신의 주장이 옳다고 주장</td></tr>
<tr><td class="c">9</td><td><b>잘못된</b> 권위에 호소하는 오류</td><td>부적절한 권위에 호소하는 오류</td><td>논점과 다른 영역에서 얻은 권위로 주장을 정당화</td></tr>
<tr><td class="c">10</td><td>미끄러운 비탈길의 오류</td><td>같음</td><td>한 사건 → 연쇄적으로 극단적 결과가 뒤따를 것이라 주장하나 근거 불충분</td></tr>
<tr><td class="c">11</td><td>허수아비 공격의 오류</td><td>같음</td><td>실제 주장을 왜곡·과장한 뒤 그것을 반박하고 실제 주장을 논파한 것처럼 구는 오류</td></tr>
<tr><td class="c">12</td><td><b>인과 관계</b>의 오류</td><td>잘못된 인과 관계의 오류</td><td>시간적·<b>상관 관계</b>만으로 원인-결과 관계가 있다고 판단</td></tr></table>''')
S3 += card('s', '심화', '필기 구별 도식 — 두 쌍 더', '''
<div class="vs"><div><h4>성급한 일반화</h4><p style="margin:0"><b>소수 사례</b> → (전체로 넓힘) → 결론 오류</p><p style="margin:2px 0 0;font-size:8.6pt">"내가 본 ○○중 학생 두 명이 불친절 → ○○중 학생은 다 불친절"</p></div><div class="m">vs</div>
<div><h4>결합(합성)</h4><p style="margin:0"><b>부분은 옳음</b> → (억지로 합침) → 결론 오류</p><p style="margin:2px 0 0;font-size:8.6pt">"고추장도 좋아하고 빵도 좋아함 → 초고추장 바른 빵도 좋아함"</p></div></div>
<p style="font-size:8.6pt;margin:2px 0 8px">판별: 근거가 <b>"몇 개의 사례"</b>이면 성급한 일반화, 근거가 <b>"각각은 맞는 부분들"</b>이면 결합.</p>
<div class="vs"><div><h4>허수아비 공격</h4><p style="margin:0"><b>엉뚱한 해석</b>: A를 말했는데 B로 바꿔 공격 (A → B)</p><p style="margin:2px 0 0;font-size:8.6pt">"운동 좀 더 하자" → "하루 종일 헬스장에서 살라는 거야?"</p></div><div class="m">vs</div>
<div><h4>미끄러운 비탈길</h4><p style="margin:0"><b>극단적 해석</b>: 근거 없는 <b>중간 과정</b>을 줄줄이 이어 극단적 결과로</p><p style="margin:2px 0 0;font-size:8.6pt">"숙제 안 함 → 내일도 안 함 → 학교 그만둠 → 대학 못 감 → 취업 실패"</p></div></div>
<p style="font-size:8.6pt;margin:2px 0 8px">판별: <b>상대의 말을 바꿔 치기</b>하면 허수아비, <b>"~하면 → ~하고 → 결국 ~"의 연쇄</b>가 보이면 비탈길. 허수아비는 상대가 있는 <b>대화</b>에서, 비탈길은 <b>한 사람의 예측</b>에서 주로 나온다.</p>
<div class="tip"><span class="l">TIP</span><b>인과 관계의 오류</b>는 필기처럼 두 종류를 모두 알아 두자. ① <b>시간적 선후</b>: "검은 고양이가 지나간 다음 날 사고 → 고양이 때문" ② <b>상관 관계</b>: "아이스크림이 많이 팔리는 달에 물놀이 사고도 많다 → 아이스크림이 사고 원인" (실제로는 <b>더운 날씨</b>라는 제3의 원인이 둘 다를 늘림). 함께 변한다고 해서 원인과 결과인 것은 아니다.</div>''')

# ------------------------------------------------------------------ S4 문법
S4 = card('b', '기본', '필기식 정리 — 문장 성분별 "형식" 한눈표', '''
<p>필기는 성분마다 <b>"형식"</b>(어떤 말이 와서 그 성분이 되는가)으로 정리했다. 문장 성분 찾기 문제는 이 형식을 거꾸로 적용하면 빨리 풀린다.</p>
<table><tr><th style="width:12%">구분</th><th style="width:13%">성분</th><th style="width:17%">뜻 (필기)</th><th>형식</th></tr>
<tr><td rowspan="4" class="c"><b>주성분</b><br><span style="font-size:8pt">필수적인 성분</span></td><td>주어</td><td>문장의 주체</td><td>① 체언 ② 체언 + 주격 조사 ③ 체언 + 보조사 <span style="color:#666">(①은 조사 생략: "차은우 어디 있어?")</span></td></tr>
<tr><td>서술어</td><td>풀이 성분</td><td>① 동사(어찌하다) ② 형용사(어떠하다) ③ 체언 + 이다(무엇이다)</td></tr>
<tr><td>목적어</td><td>동작 대상</td><td>① 체언 + 을/를 ② 체언 + 보조사 ③ 체언 + 보조사 + 을/를 ④ 체언(조사 생략)</td></tr>
<tr><td>보어</td><td>의미 보충</td><td><b>'되다, 아니다' 앞</b>의 체언 + 이/가(보격 조사)</td></tr>
<tr><td rowspan="2" class="c"><b>부속 성분</b><br><span style="font-size:8pt">꾸며 주는 성분</span></td><td>관형어</td><td>체언 꾸며 줌</td><td>① 관형사 ② 체언 + 의 ③ 용언 어간 + 관형사형 어미 → <b>시제 파악</b>: 만난(과거)·만날(미래)·만나던(회상) 사람</td></tr>
<tr><td>부사어</td><td>용언 등 꾸며 줌</td><td>① 부사 ② 체언 + 부사격 조사 ③ 용언 어간 + -게</td></tr>
<tr><td class="c"><b>독립 성분</b></td><td>독립어</td><td>홀로 쓰임</td><td>① 감탄사 ② 체언 + 호격 조사 ③ 제시어, 표제어</td></tr></table>''')
S4 += card('s', '심화', '필기 ★ — 필수적 부사어 vs 이동 불가 부사어 (포함 관계 X)', '''
<p>필기에 두 개념을 괄호로 묶고 <b>"포함 관계 X"</b>라고 적어 둠. 둘은 <b>따지는 기준이 다른 별개의 개념</b>이다. "이동 불가 부사어는 모두 필수적 부사어다" 같은 선지는 틀림.</p>
<table><tr><th style="width:18%"></th><th>필수적 부사어</th><th>위치 이동이 불가능한 부사어</th></tr>
<tr><td>기준</td><td><b>빼면</b> 문장이 불완전해지는가?</td><td><b>자리를 옮기면</b> 문장이 어색해지는가?</td></tr>
<tr><td>필기 예문</td><td>강아지가 <b>귀엽게</b> 생겼다<br><span style="font-size:8.4pt;color:#555">→ "강아지가 생겼다"는 뜻이 달라짐</span></td><td>애가 아직 잠에 <b>안</b> 들었다<br><span style="font-size:8.4pt;color:#555">→ "안 애가 아직 잠에 들었다" ✗ (부정 부사 '안'은 꾸미는 용언 바로 앞에만)</span></td></tr>
<tr><td>더 볼 예</td><td>그는 친구<b>에게</b> 선물을 주었다 / 나는 너<b>와</b> 다르다 / 그를 제자<b>로</b> 삼았다</td><td>나는 밥을 <b>못</b> 먹었다 / <b>잘</b> 모르겠다</td></tr>
<tr><td>빼 보면</td><td>문장이 어색 → 꼭 필요</td><td>문장은 성립 (애가 아직 잠에 들었다 — 뜻만 바뀜) → 필수는 아님</td></tr></table>''')
S4 += card('s', '심화', '필기 ★ — 부사 파생 접미사 "-이" vs 부사형 어미 "-게, -도록"', '''
<table><tr><th style="width:18%"></th><th>부사 파생 <b>접미사</b> -이 (-히)</th><th>부사형 전성 <b>어미</b> -게, -도록</th></tr>
<tr><td>품사 변화</td><td class="r">O — 새 단어(부사)가 만들어짐</td><td class="bl">X — 원래 품사(동사·형용사) 그대로, 활용형일 뿐</td></tr>
<tr><td>예</td><td>없- + -이 → <b>없이</b>(부사) / 깨끗이, 조용히, 같이</td><td>나- + -게 → <b>나게</b>(동사 '나다'의 활용형) / 나도록, 빠르게</td></tr>
<tr><td>부사절 예문</td><td>진우가 [예고도 <b>없이</b>] 돌아왔다.</td><td>드라마가 [눈물이 나<b>게</b>] 슬프다. / 민후는 [땀이 나<b>도록</b>] 뛰었다.</td></tr></table>
<p style="font-size:8.6pt;margin:3px 0">공통점: 둘 다 앞의 절을 <b>부사절(부사어 역할)</b>로 만든다. 차이점만 "품사 변화 O / X"로 기억. (필기: 접미사 = 품사 변화 O, 어미 = 품사 변화 X)</p>''')
S4 += card('a', '응용', '보충 — 인용절: 직접 인용 → 간접 인용 바꾸는 규칙', '''
<p>필기: 직접 인용 = 큰따옴표 + 조사 <b>'라고'</b> / 간접 인용 = 조사 <b>'고'</b>. 간접 인용으로 바꿀 때는 따옴표를 없애고, 종결 어미를 아래처럼 바꾼다.</p>
<table><tr><th>원래 문장 종류</th><th>직접 인용</th><th>간접 인용</th></tr>
<tr><td>평서</td><td>그는 "시험을 통과했어."<b>라고</b> 말했다.</td><td>그는 시험을 통과했<b>다고</b> 말했다.</td></tr>
<tr><td>의문</td><td>선생님께서 "숙제는 다 했니?"<b>라고</b> 물으셨다.</td><td>선생님께서 숙제는 다 했<b>냐고</b> 물으셨다.</td></tr>
<tr><td>명령</td><td>엄마는 "일찍 자라."<b>라고</b> 하셨다.</td><td>엄마는 일찍 자<b>라고</b> 하셨다.</td></tr>
<tr><td>청유</td><td>친구가 "같이 가자."<b>라고</b> 말했다.</td><td>친구가 같이 가<b>자고</b> 말했다.</td></tr></table>
<p style="font-size:8.6pt;margin:3px 0">인칭도 전달하는 사람 입장으로: "<b>나는</b> 내일 갈게." → <b>자기는</b> 내일 가겠다고. 인용절은 직접이든 간접이든 <b>부사어</b> 역할.</p>
<div class="memo"><span class="l">✎ 필기</span>이어진 문장 판별의 핵심 한 줄: <b>대등</b> = 절 순서 바꿔도 의미 차이 X (나열 -고·-(으)며 / 대조 -(으)나·-지만 / 선택 -거나·-든지) · <b>종속</b> = 순서 바꾸면 의미 차이 O (시간 -고 / 원인 -아서·-(으)니 / 조건 -(으)면·-거든 / 의도 -(으)러·-(으)려고 / 상황 -는데 / 양보 -(으)ㄹ지라도·-아도).</div>''')


# ------------------------------------------------------------------ S5 문제
def q(n, tag, cls, text, box=None, ch=None, lines=0):
    s = f'<div class="q"><div class="h"><span class="n">{n}</span><span class="tag {cls}">{tag}</span>{text}</div>'
    if box:
        s += '<div class="box">' + '<br>'.join(box) + '</div>'
    if ch:
        s += '<ul class="ch">' + ''.join(f'<li>{"①②③④⑤"[i]} {c}</li>' for i, c in enumerate(ch)) + '</ul>'
    s += '<div class="line"></div>' * lines + '</div>'
    return s


QS = [
 q(57, '발전', 't-d', '(가) 「어져 내 일이야」와 (나) 「마음이 어린 후이니」를 비교한 것으로 적절하지 <u>않은</u> 것은?', ch=[
   '(가)는 임을 보낸 자신을, (나)는 임이 온 것으로 착각하는 자신의 어리석음을 탓한다.', '(가)는 감탄사로, (나)는 일반적 진술로 시상을 시작한다.',
   '(가)는 후회·미련·그리움을, (나)는 자책·체념·그리움을 드러낸다.', '(가)는 공간적 배경을 통해 임과의 정서적 거리감을 드러낸다.', '두 작품 모두 평시조이며 종장의 첫 음보가 3음절이다.']),
 q(58, '서술형', 't-w', '「님이 오마 하거늘」에서 \'곰븨님븨 님븨곰븨\', \'위렁충창\' 같은 음성 상징어가 화자의 정서를 드러내는 방식을 \'과장\', \'그리움\'이라는 말을 넣어 쓰시오.', lines=2),
 q(59, '발전', 't-d', '「연탄 한 장」과 「담쟁이」를 비교한 것으로 적절하지 <u>않은</u> 것은?', ch=[
   '연탄은 재가 되어 소멸하고, 담쟁이는 벽을 덮으며 뻗어 나간다.', '「연탄 한 장」은 자기희생을, 「담쟁이」는 연대를 강조한다.', '「연탄 한 장」은 반성을, 「담쟁이」는 의지를 드러낸다.',
   '「연탄 한 장」은 미래의 목표를, 「담쟁이」는 과거에 대한 성찰을 중심으로 한다.', '두 작품 모두 일상적 소재에 상징적 의미를 부여한다.']),
 q(60, '응용', 't-a', '"연탄은, 일단 제 몸에 불이 옮겨붙었다 하면 / 하염없이 뜨거워지는 것"에 쓰인 표현법을 쓰고, 그 효과를 쓰시오.', lines=2),
 q(61, '응용', 't-a', '「연탄 한 장」의 시어와 감각적 이미지를 바르게 연결하시오.', box=['(1) 방구들 선득선득해지는 날　(2) 연탄 차가 부릉부릉　(3) 매일 따스한 밥과 국물', '㉠ 촉각적 이미지　㉡ 청각적 이미지']),
 q(62, '서술형', 't-w', '「담쟁이」에서 \'~라고 ~할 때 / 담쟁이는 ~ㄴ다\'의 구조를 반복한 효과를 두 가지 쓰시오.', lines=2),
 q(63, '응용', 't-a', '정의를 보고 오류의 이름을 쓰시오. (다른 이름이 있으면 함께 쓰시오.)', box=['(1) 더 많은 선택지가 있는데도 둘뿐인 것처럼 제시한다.', '(2) 대중의 규모에 비추어 자신의 주장이 옳다고 한다.', '(3) 논점과 다른 영역에서 얻은 권위를 이용한다.', '(4) 부분적으로 옳은 주장들을 무리하게 합친다.', '(5) 시간적·상관 관계만으로 원인과 결과라고 판단한다.']),
 q(64, '발전', 't-d', '(가), (나)에 나타난 오류를 각각 쓰고, 둘을 구별하는 기준을 쓰시오.', box=['(가) 아들: 용돈을 조금만 올려 주세요. / 아빠: 그럼 네가 번 돈처럼 마음대로 다 써 버리겠다는 거구나.', '(나) 용돈을 올려 주면 군것질이 늘고, 그러면 이가 다 썩고, 결국 치과비 때문에 집안 형편이 어려워질 거야.'], lines=2),
 q(65, '응용', 't-a', '인과 관계의 오류에 해당하는 것은?', ch=[
   '아이스크림이 많이 팔리는 달에 물놀이 사고도 많으니, 아이스크림이 사고의 원인이다.', '이 식당은 늘 손님이 많으니 틀림없이 맛있을 것이다.', '너도 지각했으면서 나한테 뭐라고 하니?',
   '인기 가수가 광고한 운동화니까 달리기 기록이 좋아질 거야.', '우리 반 두 명이 안경을 쓰니 우리 학교 학생은 모두 눈이 나쁘다.']),
 q(66, '발전', 't-d', '(가), (나)의 오류 이름을 쓰시오.', box=['(가) 이 팀 선수들은 한 명 한 명이 모두 뛰어나다. 그러므로 이 팀은 최고의 팀이다.', '(나) 어제 본 그 영화사의 영화가 지루했으니, 그 영화사의 영화는 다 지루하다.']),
 q(67, '심화', 't-s', '오류가 <u>없는</u> 논증은?', ch=[
   '모든 포유류는 폐로 호흡한다. 고래는 포유류이다. 그러므로 고래는 폐로 호흡한다.', '공부를 안 하면 꼴찌가 되고, 꼴찌가 되면 인생이 끝난다.', '너는 나를 도와주든지, 나를 싫어하든지 둘 중 하나야.',
   '이 물건을 만든 사람들은 형편이 어려우니 꼭 사 주세요.', '그의 의견은 틀렸어. 그는 시험에서 낙제한 적이 있거든.']),
 q(68, '심화', 't-s', '(1) 밑줄 친 부사어를 빼면 문장이 불완전해지는 것을 모두 고르시오. (2) ④의 \'안\'이 지닌 특징을 쓰시오.', ch=[
   '강아지가 <u>귀엽게</u> 생겼다.', '나는 <u>너와</u> 다르다.', '그는 <u>빨리</u> 달렸다.', '애가 아직 잠에 <u>안</u> 들었다.', '그는 <u>친구에게</u> 선물을 주었다.']),
 q(69, '심화', 't-s', '밑줄 친 말 중 품사가 <b>부사</b>인 것을 모두 고르고, 판단 근거를 쓰시오.', box=['ㄱ. 진우가 예고도 <u>없이</u> 돌아왔다.　ㄴ. 드라마가 눈물이 <u>나게</u> 슬프다.', 'ㄷ. 방을 <u>깨끗이</u> 치웠다.　ㄹ. 자동차가 <u>빠르게</u> 달린다.'], lines=1),
 q(70, '응용', 't-a', '직접 인용을 간접 인용으로 바꾸시오.', box=['(1) 선생님께서 "숙제는 다 했니?"라고 물으셨다.', '(2) 엄마는 "일찍 자라."라고 하셨다.', '(3) 친구가 "같이 가자."라고 말했다.']),
 q(71, '응용', 't-a', '[　] 안 성분의 형식이 \'체언 + 보조사\'인 것은?', ch=['[동생도] 학교에 왔다.', '[정부에서] 정책을 발표했다.', '[너] 어디 가?', '나는 [사과만을] 먹었다.', '[우리가] 이겼다.']),
 q(72, '응용', 't-a', '이어진 방식이 나머지와 <u>다른</u> 것은?', ch=['그는 키가 크지만 동생은 작다.', '비가 와도 경기는 열린다.', '산은 높고 물은 맑다.', '커피를 마시거나 차를 마셔라.', '형은 노래하며 동생은 춤춘다.']),
 q(73, '발전', 't-d', '겹문장을 모두 고르시오.', box=['(1) 그는 반장이 되었다.　(2) 코끼리는 코가 길다.　(3) 나는 가수가 아니다.', '(4) 이 꽃은 향기가 좋다.　(5) 물이 얼음이 되었다.']),
 q(74, '서술형', 't-w', '"진우가 예고도 없이 돌아왔다."에서 안긴 절의 종류와 역할을 쓰고, \'없이\'의 \'-이\'가 \'나게\'의 \'-게\'와 어떻게 다른지 쓰시오.', lines=3),
]

ANS = [
 (57, '④', '공간적 배경(만중운산)으로 정서적 거리감을 드러내는 것은 (나). (가)의 핵심 표현은 영탄법과 중장의 중의성.'),
 (58, '예시 답', '의태어·의성어로 버선과 신을 벗어 들고 허둥지둥 달려가는 행동을 과장되게 묘사하여, 임을 빨리 만나고 싶은 간절한 그리움을 해학적으로 드러낸다.'),
 (59, '④', '반대. 「연탄 한 장」은 과거·성찰(몰랐네), 「담쟁이」는 미래·목표(결국 그 벽을 넘는다).'),
 (60, '의인법', '연탄을 \'제 몸\'을 가진 사람처럼 표현하여, 자신을 불태워 남을 따뜻하게 하는 연탄의 희생적 면모를 효과적으로 드러낸다. (\'뜨거워지는\' = 촉각적 이미지)'),
 (61, '(1)㉠ (2)㉡ (3)㉠', '선득선득·따스한 = 촉각, 부릉부릉 = 청각(음성 상징어·의성어).'),
 (62, '예시 답', '① 운율을 형성한다. ② \'우리\'의 체념과 담쟁이의 극복을 대조하고, 서술어(오른다→나아간다→올라간다→넘는다)를 점층적으로 제시하여 담쟁이의 극복 의지를 강조한다.'),
 (63, '이름', '(1) 이분법의 오류(흑백 사고) (2) 군중(대중)에 호소하는 오류 (3) 잘못된(부적절한) 권위에 호소하는 오류 (4) 결합(합성)의 오류 (5) (잘못된) 인과 관계의 오류'),
 (64, '(가) 허수아비 (나) 비탈길', '(가)는 "조금 올려 달라"는 말을 "마음대로 다 쓰겠다"로 바꿔(엉뚱한 해석 A→B) 공격. (나)는 근거 없는 중간 과정을 연쇄적으로 이어 극단적 결과를 예측.'),
 (65, '①', '함께 늘어나는 것(상관 관계)일 뿐, 실제 원인은 더운 날씨. ② 군중 ③ 피장파장 ④ 잘못된 권위 ⑤ 성급한 일반화'),
 (66, '(가) 결합 (나) 성급한 일반화', '(가) 각 부분(선수 개인)이 뛰어나다는 옳은 사실을 합쳐 전체(팀)도 최고라고 판단. (나) 한 편(소수 사례)으로 전체를 판단.'),
 (67, '①', '대전제·소전제가 참인 연역 논증. ② 비탈길 ③ 이분법 ④ 동정에 호소 ⑤ 인신공격'),
 (68, '(1) ①②⑤', '(2) 위치를 옮길 수 없는 부사어(부정 부사 \'안\'은 서술어 바로 앞에만). 빼도 문장은 성립하므로 필수적 부사어는 아님 → 두 개념은 포함 관계가 아니다.'),
 (69, 'ㄱ, ㄷ', '없이·깨끗이는 부사 파생 접미사 \'-이\'가 붙어 품사가 부사로 바뀜(품사 변화 O). 나게·빠르게는 부사형 어미 \'-게\'가 붙은 동사·형용사의 활용형(품사 변화 X).'),
 (70, '간접 인용', '(1) 선생님께서 숙제는 다 했냐고 물으셨다. (2) 엄마는 일찍 자라고 하셨다. (3) 친구가 같이 가자고 말했다.'),
 (71, '①', '동생 + 보조사 \'도\'. ② 주격 조사(단체) ③ 조사 생략 ④ 체언+보조사+목적격 조사 ⑤ 주격 조사'),
 (72, '②', '\'-어도\'(양보) → 종속적으로 이어진문장. 나머지는 대조·나열·선택·나열 → 대등.'),
 (73, '(2), (4)', '\'주어 + 주어 + 서술어\' → 서술절을 가진 안은문장. (1)(3)(5)는 \'되다/아니다\' 앞 보어가 있는 홑문장.'),
 (74, '부사절 · 부사어', '\'예고도 없이\'는 부사절로 부사어 역할을 한다. \'-이\'는 부사 파생 접미사라 \'없다\'를 부사 \'없이\'로 바꾸지만(품사 변화 O), \'-게\'는 부사형 어미라 \'나다\'의 품사는 동사 그대로다(품사 변화 X).'),
]

S5 = ('<div class="banner"><div class="k">SUPPLEMENT · 필기 반영</div><h2>보충 문제 57~74</h2><p>손글씨 필기에만 있던 비교·구별 포인트로 만든 문제 18개 (변형 문제 56에 이어서)</p></div>'
      '<div class="cols">' + ''.join(QS) + '</div>'
      '<div class="pb"></div><section class="card p"><div class="hd"><span class="bd">정답</span><h3>보충 문제 57~74 · 정답과 해설</h3></div><div class="in"><table class="ak"><tr><th>번호</th><th>정답</th><th>해설</th></tr>'
      + ''.join(f'<tr><td>{n}</td><td>{a}</td><td>{e}</td></tr>' for n, a, e in ANS) + '</table></div></section>')


def guide(pages):
    rows = ''.join(f'<tr><td class="c"><b>{p}쪽</b></td><td>{w}</td><td>{d}</td></tr>' for p, w, d in pages)
    return ('<div class="banner"><div class="k">보충판 안내</div><h2>손글씨 필기 반영 보충판</h2><p>수업 필기 8쪽(문장 성분 · 문장의 짜임 · 논증 오류 · 시조 3수 · 연탄 한 장 · 담쟁이)을 기존 노트와 한 줄씩 대조해, 노트에 없거나 다르게 적힌 부분만 보충 페이지로 끼워 넣었습니다.</p></div>'
            + card('p', '목록', '끼워 넣은 보충 페이지', f'<table><tr><th style="width:12%">위치</th><th style="width:26%">단원</th><th>보충 내용</th></tr>{rows}</table>', src='새 쪽 번호 기준')
            + card('s', '확인', '필기와 노트가 다르게 적힌 곳', '''<ul>
<li><b>「연탄 한 장」 감각적 이미지</b> — 필기: 촉각·<b>청각</b> / 노트(12쪽): 촉각·<b>시각</b>. 학습지 빈칸 답을 확인하고, 셋 다 근거 시어로 알아 두기.</li>
<li><b>오류 이름 5개</b> — 결합=합성, 이분법=흑백 사고, 군중=대중, 잘못된 권위=부적절한 권위, 인과 관계=잘못된 인과. 뜻은 같고 이름만 다름.</li>
<li><b>「마음이 어린 후이니」 만중운산</b> — 필기 "심리적 거리감", 노트 "정서적 거리감". 같은 뜻이니 어느 쪽으로 써도 됨.</li>
<li><b>「어져 내 일이야」</b> — 필기 "임 보낸 자신을 원망" = 자기 자신에 대한 후회·자책 (임을 원망하는 것 X).</li></ul>''', src='')
            + card('a', '계획', '남은 이틀 — 보충 페이지 끼워 넣기', '''<table><tr><th style="width:22%">날짜</th><th>할 일 (기존 계획 + 보충)</th></tr>
<tr><td>9/27 (일) D-2</td><td>기존 계획(오류 12 · 논증 학습지 · 변형 27~40 · 문법 개념) + <b>오류 보충 · 문법 보충 페이지</b></td></tr>
<tr><td>9/28 (월) D-1</td><td>문법 확인 문제 · 변형 41~56 + <b>시조·현대시 보충 페이지</b> + <b>보충 문제 57~74</b> → 틀린 것만 다시</td></tr>
<tr><td>9/29 (화) 당일</td><td>한 장 요약 + 각 단원 함정표 + 보충판 안내의 "다르게 적힌 곳"만 훑기</td></tr></table>''', src=''))
