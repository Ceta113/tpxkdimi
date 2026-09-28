from lib import img, level, box

EYE_ADJ_SVG = '''
<svg viewBox="0 0 720 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="눈의 밝기 조절과 거리 조절 요약">
 <style>.t{font-size:13px;font-weight:700;fill:#1f2430}.s{font-size:11.5px;fill:#5b6272}.h{font-size:14px;font-weight:900}</style>
 <g transform="translate(90,70)">
  <text class="h" x="0" y="-52" text-anchor="middle" fill="#d9772b">밝은 곳</text>
  <ellipse rx="66" ry="36" fill="#fff" stroke="#999"/>
  <circle r="30" fill="#8b5a2b"/><circle r="30" fill="none" stroke="#5a3a1a" stroke-width="2"/>
  <circle r="8" fill="#111"/>
  <text class="t" x="0" y="58" text-anchor="middle">홍채 확장 → 동공 작아짐</text>
  <text class="s" x="0" y="76" text-anchor="middle">들어오는 빛의 양 감소</text>
 </g>
 <g transform="translate(270,70)">
  <text class="h" x="0" y="-52" text-anchor="middle" fill="#334">어두운 곳</text>
  <ellipse rx="66" ry="36" fill="#fff" stroke="#999"/>
  <circle r="30" fill="#8b5a2b"/><circle r="30" fill="none" stroke="#5a3a1a" stroke-width="2"/>
  <circle r="20" fill="#111"/>
  <text class="t" x="0" y="58" text-anchor="middle">홍채 축소 → 동공 커짐</text>
  <text class="s" x="0" y="76" text-anchor="middle">들어오는 빛의 양 증가</text>
 </g>
 <line x1="362" y1="10" x2="362" y2="190" stroke="#d9dde5" stroke-width="2" stroke-dasharray="5 4"/>
 <g transform="translate(450,70)">
  <text class="h" x="0" y="-52" text-anchor="middle" fill="#2f6fd6">가까운 곳</text>
  <rect x="-8" y="-46" width="16" height="12" rx="3" fill="#e27d60"/><rect x="-8" y="34" width="16" height="12" rx="3" fill="#e27d60"/>
  <line x1="0" y1="-34" x2="0" y2="-24" stroke="#999"/><line x1="0" y1="34" x2="0" y2="24" stroke="#999"/>
  <ellipse rx="16" ry="25" fill="#bfe3ff" stroke="#2f6fd6" stroke-width="2"/>
  <text class="s" x="30" y="-36">섬모체 수축</text>
  <text class="t" x="0" y="58" text-anchor="middle">섬모체 수축 → 수정체 두꺼워짐</text>
  <text class="s" x="0" y="76" text-anchor="middle">빛을 많이 굴절</text>
 </g>
 <g transform="translate(630,70)">
  <text class="h" x="0" y="-52" text-anchor="middle" fill="#1f9d62">먼 곳</text>
  <rect x="-8" y="-46" width="16" height="12" rx="3" fill="#f3b6a4"/><rect x="-8" y="34" width="16" height="12" rx="3" fill="#f3b6a4"/>
  <line x1="0" y1="-34" x2="0" y2="-28" stroke="#999"/><line x1="0" y1="34" x2="0" y2="28" stroke="#999"/>
  <ellipse rx="7" ry="28" fill="#bfe3ff" stroke="#1f9d62" stroke-width="2"/>
  <text class="s" x="20" y="-36">섬모체 이완</text>
  <text class="t" x="0" y="58" text-anchor="middle">섬모체 이완 → 수정체 얇아짐</text>
  <text class="s" x="0" y="76" text-anchor="middle">빛을 적게 굴절</text>
 </g>
</svg>'''

LYMPH_SVG = '''
<svg viewBox="0 0 640 170" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="반고리관 림프의 관성">
 <style>.t{font-size:12.5px;font-weight:700;fill:#1f2430}.s{font-size:11px;fill:#5b6272}</style>
 <defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#d6453d"/></marker>
 <marker id="ab" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#2f6fd6"/></marker></defs>
 <g transform="translate(110,78)">
  <circle r="48" fill="none" stroke="#c9a15b" stroke-width="16"/>
  <path d="M -40 -50 A 64 64 0 0 1 40 -50" fill="none" stroke="#333" stroke-width="2.5" marker-end="url(#ar)"/>
  <path d="M 34 34 A 48 48 0 0 1 -34 34" fill="none" stroke="#2f6fd6" stroke-width="3" marker-end="url(#ab)"/>
  <text class="t" x="0" y="82" text-anchor="middle">① 회전 시작</text>
  <text class="s" x="0" y="-60" text-anchor="middle">몸(관) 회전 →</text>
  <text class="s" x="0" y="6" text-anchor="middle">림프는 제자리</text><text class="s" x="0" y="20" text-anchor="middle">(반대로 흐르는 효과)</text>
 </g>
 <g transform="translate(320,78)">
  <circle r="48" fill="none" stroke="#c9a15b" stroke-width="16"/>
  <path d="M -40 -50 A 64 64 0 0 1 40 -50" fill="none" stroke="#333" stroke-width="2.5" marker-end="url(#ar)"/>
  <path d="M -34 34 A 48 48 0 0 0 34 34" fill="none" stroke="#aaa" stroke-width="3" stroke-dasharray="4 3"/>
  <text class="t" x="0" y="82" text-anchor="middle">② 일정하게 계속 회전</text>
  <text class="s" x="0" y="6" text-anchor="middle">림프도 함께 돎</text><text class="s" x="0" y="20" text-anchor="middle">→ 회전 감각 약해짐</text>
 </g>
 <g transform="translate(530,78)">
  <circle r="48" fill="none" stroke="#c9a15b" stroke-width="16"/>
  <text class="s" x="0" y="-60" text-anchor="middle">몸(관) 정지 ■</text>
  <path d="M -34 34 A 48 48 0 0 0 34 34" fill="none" stroke="#2f6fd6" stroke-width="3" marker-end="url(#ab)"/>
  <text class="t" x="0" y="82" text-anchor="middle">③ 갑자기 멈춤</text>
  <text class="s" x="0" y="6" text-anchor="middle">림프는 관성으로</text><text class="s" x="0" y="20" text-anchor="middle">계속 흐름 → 어지러움</text>
 </g>
</svg>'''


def build():
    h = []
    # ---------------- 기본 ----------------
    b = []
    b.append('''<p><b>감각 기관</b>: 환경 변화(자극)를 받아들이는 기관. 모든 감각은 공통 경로를 거친다.</p>
<div class="flow"><span>자극</span><i>→</i><span class="k">감각 기관 (감각 세포)</span><i>→</i><span>감각 신경</span><i>→</i><span class="k">뇌 (감각을 느낌)</span></div>
<table class="t"><tr><th>감각 기관</th><th>받아들이는 자극</th><th>감각 세포 / 감각점</th><th>감각 신경</th><th>감각</th></tr>
<tr><td>눈</td><td>빛</td><td>시각 세포 (망막)</td><td>시각 신경</td><td>시각</td></tr>
<tr><td rowspan="2">귀</td><td>소리 (공기의 진동)</td><td>청각 세포 (달팽이관)</td><td>청각 신경</td><td>청각</td></tr>
<tr><td>몸의 기울어짐·회전</td><td>감각 세포 (전정 기관·반고리관)</td><td>평형 감각 신경</td><td>평형 감각</td></tr>
<tr><td>코</td><td><b>기체</b> 상태의 화학 물질</td><td>후각 세포 (후각 상피)</td><td>후각 신경</td><td>후각</td></tr>
<tr><td>혀</td><td><b>액체</b> 상태의 화학 물질</td><td>맛세포 (맛봉오리)</td><td>미각 신경</td><td>미각</td></tr>
<tr><td>피부</td><td>접촉, 압력, 온도 변화, 통증</td><td>감각점 (촉점·압점·냉점·온점·통점)</td><td>피부 감각 신경</td><td>피부 감각</td></tr></table>''')
    b.append('<h4>① 눈의 구조와 기능</h4><div class="two">' + img('iv_eye_structure', cap='눈의 구조') + '''
<table class="t"><tr><th>구조</th><th>기능 (시험에 나오는 한 줄)</th></tr>
<tr><td>각막</td><td class="l">눈 앞쪽의 <b>투명한 막</b>, 빛이 통과</td></tr>
<tr><td>홍채</td><td class="l"><b>동공의 크기</b>를 조절 → 빛의 양 조절</td></tr>
<tr><td>동공</td><td class="l">홍채 가운데 <b>구멍</b>, 빛이 들어가는 통로</td></tr>
<tr><td>수정체</td><td class="l"><b>볼록 렌즈</b> 모양, 빛을 굴절시켜 망막에 상을 맺음</td></tr>
<tr><td>섬모체</td><td class="l"><b>수정체의 두께</b>를 조절하는 근육</td></tr>
<tr><td>유리체</td><td class="l">눈 속을 채우는 투명 물질, <b>눈의 형태 유지</b></td></tr>
<tr><td>망막</td><td class="l">가장 안쪽 막, <b>시각 세포</b> 분포, <b>상이 맺히는 곳</b></td></tr>
<tr><td>황반</td><td class="l">시각 세포 <b>밀집</b> → 상이 가장 뚜렷</td></tr>
<tr><td>맹점</td><td class="l">시각 신경이 모여 나가는 곳, <b>시각 세포 없음</b> → 상이 맺혀도 안 보임</td></tr>
<tr><td>맥락막</td><td class="l"><b>검은색 색소</b> → 눈 속을 어둡게 (암실)</td></tr>
<tr><td>공막</td><td class="l">가장 바깥 <b>흰색 막</b> (흰자위), 눈 보호·형태 유지</td></tr>
<tr><td>시각 신경</td><td class="l">시각 세포가 받은 자극을 <b>뇌로 전달</b></td></tr></table></div>''')
    b.append('<h4>② 귀의 구조와 기능</h4><div class="two">' + img('iv_ear_structure', cap='귀의 구조') + '''
<table class="t"><tr><th>구조</th><th>기능</th></tr>
<tr><td>귓바퀴</td><td class="l">소리(음파)를 모음</td></tr>
<tr><td>외이도</td><td class="l">소리가 고막까지 지나가는 통로</td></tr>
<tr><td>고막</td><td class="l">얇은 막, 소리에 의해 <b>가장 먼저 진동</b></td></tr>
<tr><td>귓속뼈</td><td class="l">작은 뼈 3개, 고막의 진동을 <b>증폭</b></td></tr>
<tr><td>달팽이관</td><td class="l"><b>청각 세포</b> 분포 → 소리 자극 수용</td></tr>
<tr><td>전정 기관</td><td class="l">몸의 <b>기울어짐</b> 감지</td></tr>
<tr><td>반고리관</td><td class="l">몸의 <b>회전</b> 감지 (반원형 관 3개)</td></tr>
<tr><td>귀인두관</td><td class="l">귀와 목구멍 연결 → 고막 안팎 <b>압력 조절</b></td></tr></table></div>''')
    b.append('<h4>③ 코 · 혀 · 피부</h4><div class="two"><div>' + img('iv_nose', cap='코의 구조') + '''
<ul class="pt"><li>콧속 윗부분 <b>후각 상피</b>에 후각 세포</li><li>자극: <b>기체 상태</b>의 화학 물질</li></ul></div><div>''' +
             img('iv_tongue', cap='혀의 구조') + '''<ul class="pt"><li>혀 표면 돌기 = <b>유두</b>, 유두 옆면에 <b>맛봉오리</b>, 그 안에 <b>맛세포</b></li>
<li>자극: <b>액체 상태</b>의 화학 물질 · 기본 맛 5가지: <b>단맛, 짠맛, 신맛, 쓴맛, 감칠맛</b></li></ul></div></div>''')
    b.append('<div class="two">' + img('iv_skin', cap='피부의 감각점') + '''<div><ul class="pt">
<li><b>촉점</b>: 가볍게 닿는 접촉 · <b>압점</b>: 누르는 압력</li>
<li><b>냉점</b>: 온도가 <b>낮아지는</b> 변화 · <b>온점</b>: 온도가 <b>높아지는</b> 변화</li>
<li><b>통점</b>: 매우 강한 자극(통증) — 분포 수 가장 많음</li>
<li>감각점은 <b>감각 신경의 말단</b>이 특수하게 분화된 것</li></ul></div></div>''')
    h.append(level('b', '감각 기관의 구조와 기능 — 이름·기능·경로 외우기', ''.join(b)))

    # ---------------- 응용 ----------------
    a = []
    a.append('<h4>① 물체를 보는 과정</h4><div class="flow"><span>빛</span><i>→</i><span>각막</span><i>→</i><span>(동공)</span><i>→</i><span>수정체</span><i>→</i><span>유리체</span><i>→</i><span class="k">망막의 시각 세포</span><i>→</i><span>시각 신경</span><i>→</i><span class="k">뇌</span></div>' + img('iv_vision_path', '88%'))
    a.append('<h4>② 눈의 조절 작용 (가장 많이 출제!)</h4>' + EYE_ADJ_SVG + '''
<table class="t"><tr><th>상황</th><th>홍채</th><th>동공</th><th>섬모체</th><th>수정체</th></tr>
<tr><td>어두운 곳 → 밝은 곳</td><td>확장</td><td class="red">작아짐</td><td>-</td><td>-</td></tr>
<tr><td>밝은 곳 → 어두운 곳</td><td>축소</td><td class="blue">커짐</td><td>-</td><td>-</td></tr>
<tr><td>먼 곳 → 가까운 곳</td><td>-</td><td>-</td><td>수축</td><td class="red">두꺼워짐</td></tr>
<tr><td>가까운 곳 → 먼 곳</td><td>-</td><td>-</td><td>이완</td><td class="blue">얇아짐</td></tr></table>''' +
             '<div class="two">' + img('iv_light_adjust', cap='명암 조절') + img('iv_near_far', cap='원근 조절') + '</div>' +
             box('tip', '외우는 요령', '<b>"밝으면 작게, 가까우면 두껍게"</b> — 빛이 많으면 동공을 줄이고, 가까이 보면 렌즈를 두껍게 해서 많이 꺾는다. 홍채는 <u>동공과 반대</u>로 움직인다(홍채 확장 = 동공 축소).'))
    a.append('<h4>③ 소리를 듣는 과정 · 평형 감각</h4><div class="flow"><span>소리</span><i>→</i><span>귓바퀴</span><i>→</i><span>외이도</span><i>→</i><span class="k">고막 (진동)</span><i>→</i><span class="k">귓속뼈 (증폭)</span><i>→</i><span>달팽이관의 청각 세포</span><i>→</i><span>청각 신경</span><i>→</i><span>뇌</span></div>' +
             '<div class="two">' + img('iv_hearing_path', cap='소리를 듣는 과정') + img('iv_balance', cap='평형 감각 기관') + '</div>' +
             '''<table class="t"><tr><th></th><th>전정 기관</th><th>반고리관</th></tr>
<tr><td>감지</td><td>몸의 <b>기울어짐</b> (중력 자극)</td><td>몸의 <b>회전</b></td></tr>
<tr><td>예</td><td class="l">엘리베이터 출발·정지, 경사진 언덕에서 몸을 앞으로 기울임, 눈 감고 한 발로 서기</td><td class="l">제자리 돌기 후 어지러움, 회전의자·놀이기구, 피겨 스핀</td></tr></table>''')
    a.append('<h4>④ 냄새 · 맛 · 피부 감각의 전달</h4>'
             '<div class="flow"><span>기체 상태 화학 물질</span><i>→</i><span>후각 상피의 후각 세포</span><i>→</i><span>후각 신경</span><i>→</i><span>뇌</span></div>'
             '<div class="flow"><span>액체 상태 화학 물질</span><i>→</i><span>맛봉오리의 맛세포</span><i>→</i><span>미각 신경</span><i>→</i><span>뇌</span></div>'
             '<div class="flow"><span>자극</span><i>→</i><span>피부의 감각점</span><i>→</i><span>피부 감각 신경</span><i>→</i><span>뇌</span></div>'
             '''<ul class="pt"><li><b>후각</b>: 매우 예민(아주 적은 양도 감지)하지만 <b>쉽게 피로</b> → 같은 냄새를 계속 맡으면 못 느낌.</li>
<li><b>매운맛·떫은맛은 맛이 아니다!</b> 매운맛 = 통점(+온점), 떫은맛 = 압점 → <b>피부 감각</b>.</li>
<li>우리가 느끼는 음식 맛 = <b>미각 + 후각</b> (+ 온도·촉감) 을 <b>뇌</b>가 종합 → 코감기에 걸리면 맛을 잘 모름.</li>
<li>피부 부위마다 민감도가 다른 까닭: <b>감각점의 분포 밀도(수)</b>가 다르기 때문 (손끝·입술 예민, 등 둔감).</li></ul>''')
    h.append(level('a', '조절 작용과 감각 전달 과정 — 상황에 적용하기', ''.join(a)))

    # ---------------- 발전 ----------------
    d = []
    d.append('<h4>① 탐구 해석 모음</h4><table class="t"><tr><th style="width:24%">탐구</th><th>과정 핵심</th><th>결과 · 결론</th></tr>'
             '<tr><td>맹점 확인 (교과서)</td><td class="l">한쪽 눈을 가리고 다른 눈으로 한 그림을 계속 주시하며 거리를 바꿈</td><td class="l">어느 순간 다른 그림이 안 보임 → 그 상이 <b>맹점</b>(시각 세포 없음)에 맺혔기 때문</td></tr>'
             '<tr><td>빛의 밝기와 눈 (하이탑)</td><td class="l">손전등에 흰 종이(빛이 너무 강하지 않게) · 1분 눈 감았다 뜬 뒤 → 손전등 비춤 · <b>어두운 곳</b>에서 실험</td><td class="l">눈 뜬 직후: 홍채 축소·동공 확대 → 불빛 비추면: 홍채 확장·동공 축소</td></tr>'
             '<tr><td>두 점 구별 (피부)</td><td class="l">이쑤시개 두 개 간격을 줄여가며 두 점으로 느끼는 최소 거리 측정</td><td class="l">최소 거리가 <b>짧을수록 촉점이 많고 예민</b> (손가락 끝 &gt; 손바닥 &gt; 이마 &gt; 팔뚝 &gt; 등)</td></tr>'
             '<tr><td>온도 감각</td><td class="l">한 손 15℃, 다른 손 35℃ 물에 담갔다가 두 손 모두 25℃ 물로</td><td class="l">15℃ 손은 따뜻, 35℃ 손은 차갑게 느낌 → 온점·냉점은 <b>온도 변화(상대적)</b>를 감지</td></tr>'
             '<tr><td>미각 + 후각</td><td class="l">눈을 가리고(+코를 막고) 과일 젤리/주스 맛보기</td><td class="l">코를 막으면 단맛·신맛만 느끼고 과일 종류 구분 못함 → 맛은 미각과 후각의 종합</td></tr>'
             '<tr><td>소리 vs 피부 감각 (교과서 해보기)</td><td class="l">진동하는 스마트 기기를 매달고 귀마개/손바닥으로 비교</td><td class="l">소리는 <b>공기(매질)를 통해</b> 떨어져 있어도 전달, 진동 촉감은 <b>직접 닿아야</b> 느낌</td></tr></table>')
    d.append('<div class="two">' + img('iv_tamgu_eye_setup', cap='빛의 밝기에 따른 눈의 변화 관찰') + img('iv_tamgu_eye_result', cap='결과') + '</div>')
    d.append('<h4>② 원리로 설명하기</h4><ul class="pt">'
             '<li><b>뼈 전도 이어폰</b>: 일반 이어폰은 공기 진동 → 고막 → 귓속뼈 → 달팽이관. 뼈 전도 이어폰은 <b>머리뼈의 진동이 직접 달팽이관</b>으로 전달(고막·귓속뼈를 거치지 않음) → 고막이 손상된 사람도 들을 수 있다.</li>'
             '<li><b>언 아이스크림</b>은 처음엔 단맛이 약하다 → 맛세포는 <b>액체 상태</b> 물질만 받아들이므로 녹아야(침에 녹아야) 맛을 느낌.</li>'
             '<li><b>높은 산·비행기</b>에서 귀가 먹먹 → 고막 안팎 압력 차이. 하품·침 삼키기 → <b>귀인두관</b>이 열려 압력이 같아짐.</li>'
             '<li><b>시각 신경 손상</b>: 망막에 상이 맺혀도 뇌로 전달이 안 되어 볼 수 없다 (수정체·상의 위치 문제는 아님).</li>'
             '<li><b>양쪽 눈을 뜨면 맹점을 못 느낀다</b>: 한쪽 눈의 맹점에 맺힌 부분을 다른 눈이 보완하고, 뇌가 주변 정보로 채움.</li></ul>')
    h.append(level('d', '탐구 결과 해석과 원리 설명 — 서술형 대비', ''.join(d)))

    # ---------------- 심화 ----------------
    s = []
    s.append('<h4>① 시력 이상과 교정</h4><table class="t"><tr><th>종류</th><th>원인</th><th>증상 (상의 위치)</th><th>교정</th></tr>'
             '<tr><td><b>근시</b></td><td class="l">수정체가 두꺼움 / 수정체~망막 거리가 멂</td><td class="l">먼 곳의 상이 <b>망막 앞</b> → 먼 곳이 흐림</td><td><b>오목</b> 렌즈 (빛을 퍼지게)</td></tr>'
             '<tr><td><b>원시</b></td><td class="l">수정체가 얇음 / 수정체~망막 거리가 짧음</td><td class="l">가까운 곳의 상이 <b>망막 뒤</b> → 가까운 곳이 흐림</td><td><b>볼록</b> 렌즈 (빛을 모이게)</td></tr>'
             '<tr><td>난시</td><td class="l">각막 표면이 고르지 않음</td><td class="l">빛이 한 점에 모이지 않아 흐림</td><td>특수(원기둥) 렌즈</td></tr>'
             '<tr><td>노안</td><td class="l">나이가 들어 수정체 탄력 감소</td><td class="l">가까운 곳에 초점 맞추기 어려움</td><td>볼록 렌즈</td></tr></table>'
             '<div class="two">' + img('iv_myopia', cap='근시 → 오목 렌즈') + img('iv_hyperopia', cap='원시 → 볼록 렌즈') + '</div>' +
             box('tip', '오목 렌즈 안경으로 보면 글씨가 작아 보인다', '근시용 <b>오목 렌즈</b>는 빛을 퍼지게 하여 <b>실제보다 작은 상</b>을 만든다 → 근시인 사람의 안경을 통해 책을 보면 글씨가 작게 보인다 (하이탑 실전 1).'))
    s.append('<h4>② 수정체 두께 그래프 읽기</h4><ul class="pt"><li>그래프가 <b>올라감</b> = 수정체 두꺼워짐 = 섬모체 <b>수축</b> = 물체가 <b>가까워짐</b></li>'
             '<li>그래프가 <b>내려감</b> = 수정체 얇아짐 = 섬모체 <b>이완</b> = 물체가 <b>멀어짐</b></li>'
             '<li>그래프가 <b>일정</b> = 거리 변화 없음. 이때 정상 눈이면 상은 계속 <b>망막(황반)</b>에 맺힌다 (맹점·망막 앞 X).</li>'
             '<li>물체가 가까워지면 망막에 맺히는 상의 크기는 커진다 (물체 크기가 변하는 것이 아님).</li></ul>')
    s.append('<h4>③ 반고리관의 원리 — 림프의 관성</h4><p>반고리관 3개는 <b>서로 직각</b>으로 배열되어 모든 방향의 회전을 감지한다. 관 속 <b>림프</b>가 흐르며 감각모를 휘게 해 감각 세포를 자극한다.</p>' + LYMPH_SVG +
             '<p class="small">회전을 멈추어도 림프가 <b>관성</b>에 의해 원래 방향으로 계속 흘러 감각모를 휘게 하므로, 한동안 계속 도는 것처럼 어지럽다. (반고리관·전정 기관·달팽이관 모두 림프로 차 있다)</p>')
    s.append(box('warn', '실수 방지 체크리스트 (오답 1순위)', '''<ul class="pt">
<li>홍채 <b>확장</b> → 동공 <b>축소</b> (반대!) · 어두우면 홍채 <b>축소</b> → 동공 <b>확대</b></li>
<li>빛의 경로에 <b>홍채·맥락막·공막은 없다</b> (각막 → 수정체 → 유리체 → 망막)</li>
<li>시각 세포는 <b>망막</b>에만 · 맹점엔 없음 · <b>황반</b>에 가장 많음</li>
<li>소리에 의해 <b>가장 먼저 진동하는 것은 고막</b> (귓속뼈는 증폭) · 청각 세포는 <b>달팽이관</b></li>
<li><b>달팽이관 = 청각만</b>. 평형 감각은 전정 기관(기울기) + 반고리관(회전). 소리 들을 때 반고리관·전정 기관은 관여 X</li>
<li>귀인두관은 소리 전달 X → <b>압력 조절</b></li>
<li>후각은 미각보다 <b>쉽게 피로</b>해진다 (미각이 아니라 후각!)</li>
<li>코 = <b>기체</b>, 혀 = <b>액체</b> 상태 화학 물질 · 기본 맛에 <b>매운맛 X</b></li>
<li>온점·냉점은 <b>절대 온도가 아닌 온도 변화</b> · 온도가 낮아지면 <b>냉점</b></li>
<li>통점은 촉점보다 <b>강한</b> 자극을 받아들임 · 감각점은 부위마다 <b>분포 수가 다름</b></li></ul>'''))
    h.append(level('s', '시력 이상 · 그래프 · 반고리관 — 고난도 대비', ''.join(s)))
    return '\n'.join(h)
