from lib import img, level, box

PHENO_COLOR = {'둥글고 노란색': '#ffe27a', '둥글고 초록색': '#b9e59a', '주름지고 노란색': '#ffc98a', '주름지고 초록색': '#8fcf8f'}


def geno(a, b):
    """두 생식세포 유전자 조합을 표준 표기로 (대문자 먼저)."""
    r = ''.join(sorted([a[0], b[0]], key=lambda c: (c.islower(), c)))
    y = ''.join(sorted([a[1], b[1]], key=lambda c: (c.islower(), c)))
    return r + y


def pheno(g):
    return ('둥글고 ' if 'R' in g[:2] else '주름지고 ') + ('노란색' if 'Y' in g[2:] else '초록색')


def dihybrid_table():
    gam = ['RY', 'Ry', 'rY', 'ry']
    rows = ['<table class="t" style="max-width:520px;margin:8px auto"><tr><th>♀ \\ ♂</th>' + ''.join(f'<th>{g}</th>' for g in gam) + '</tr>']
    for a in gam:
        cells = ''
        for b in gam:
            g = geno(a, b)
            cells += f'<td style="background:{PHENO_COLOR[pheno(g)]};font-weight:700">{g}</td>'
        rows.append(f'<tr><th>{a}</th>{cells}</tr>')
    rows.append('</table>')
    legend = ' '.join(f'<span style="background:{c};padding:1px 8px;border-radius:4px;margin:2px;display:inline-block">{p}</span>' for p, c in PHENO_COLOR.items())
    return ''.join(rows) + f'<p style="text-align:center;font-size:9.5pt">{legend}<br>둥글고 노란색 9 : 둥글고 초록색 3 : 주름지고 노란색 3 : 주름지고 초록색 1</p>'


MONO_TABLE = '''<table class="t" style="max-width:300px;margin:8px auto"><tr><th>♀ \\ ♂</th><th>R</th><th>r</th></tr>
<tr><th>R</th><td style="background:#ffe27a"><b>RR</b></td><td style="background:#ffe27a"><b>Rr</b></td></tr>
<tr><th>r</th><td style="background:#ffe27a"><b>Rr</b></td><td style="background:#cfd8e3"><b>rr</b></td></tr></table>
<p style="text-align:center;font-size:9.5pt">유전자형 RR : Rr : rr = 1 : 2 : 1 · 표현형 둥근 : 주름진 = 3 : 1</p>'''


def build():
    h = []
    b = []
    b.append('''<table class="t"><tr><th style="width:18%">용어</th><th>뜻</th><th style="width:28%">예</th></tr>
<tr><td>유전</td><td class="l">어버이의 형질이 자손에게 전해지는 현상</td><td class="l"></td></tr>
<tr><td>형질</td><td class="l">생물이 지닌 고유한 특성 (모양, 색, 크기 등)</td><td class="l">완두씨의 모양, 색깔</td></tr>
<tr><td>대립 형질</td><td class="l">하나의 형질에 대해 서로 <b>뚜렷하게 대비</b>되는 특성</td><td class="l">둥근 씨 ↔ 주름진 씨</td></tr>
<tr><td>표현형</td><td class="l">겉으로 드러나는 형질</td><td class="l">둥글다, 노란색</td></tr>
<tr><td>유전자형</td><td class="l">형질을 나타내는 유전자 구성을 <b>기호</b>로 표시한 것</td><td class="l">RR, Rr, rr</td></tr>
<tr><td>대립유전자</td><td class="l">대립 형질을 결정하는 유전자, <b>상동 염색체의 같은 위치</b>에 있음. 우성 = 대문자, 열성 = 소문자</td><td class="l">R 와 r</td></tr>
<tr><td>순종</td><td class="l">몇 세대를 자가 수분해도 계속 같은 형질만 나타나는 개체 (대립유전자 구성이 같음)</td><td class="l">RR, rr, RRYY, rryy</td></tr>
<tr><td>잡종</td><td class="l">대립 형질이 다른 순종끼리 교배하여 얻은 자손 (대립유전자 구성이 다름)</td><td class="l">Rr, RrYy</td></tr>
<tr><td>우성 / 열성</td><td class="l">대립 형질이 다른 순종끼리 교배했을 때 잡종 1대에 <b>나타나는 형질 / 나타나지 않는 형질</b></td><td class="l">둥근(우성) / 주름진(열성)</td></tr>
<tr><td>자가 수분 / 타가 수분</td><td class="l">한 그루 안에서의 수분 / 다른 그루의 꽃가루를 옮겨 수분</td><td class="l"></td></tr></table>''')
    b.append('<div class="two">' + img('v_pea7', cap='멘델이 연구한 완두의 7가지 대립 형질 (위: 우성, 아래: 열성)') +
             '''<div><table class="t"><tr><th>형질</th><th>우성</th><th>열성</th></tr><tr><td>씨 모양</td><td>둥글다</td><td>주름지다</td></tr><tr><td>씨 색깔</td><td>노란색</td><td>초록색</td></tr>
<tr><td>꽃 색깔</td><td>보라색</td><td>흰색</td></tr><tr><td>콩깍지 모양</td><td>매끈하다</td><td>잘록하다</td></tr><tr><td>콩깍지 색깔</td><td>초록색</td><td>노란색</td></tr>
<tr><td>꽃 위치</td><td>줄기 옆</td><td>줄기 끝</td></tr><tr><td>줄기의 키</td><td>크다</td><td>작다</td></tr></table>
<p class="small">씨 색깔은 <b>노란색</b>이 우성이지만 콩깍지 색깔은 <b>초록색</b>이 우성 — 헷갈림 주의!</p></div></div>''')
    b.append(box('key', '멘델이 완두를 실험 재료로 선택한 까닭', '① 주변에서 구하기 쉽고 재배가 쉽다 ② <b>한 세대가 짧다</b> ③ <b>자손의 수가 많아</b> 통계적 분석에 유리 ④ <b>대립 형질이 뚜렷</b> ⑤ 자가 수분과 타가 수분(인위적 교배)이 모두 가능 → 순종을 얻기 쉽다') +
             box('warn', '우성 ≠ 우수', '우성은 "잡종 1대에서 나타나는 형질"일 뿐, 더 좋거나 더 흔한 형질이라는 뜻이 아니다.'))
    h.append(level('b', '유전 용어와 완두의 대립 형질 — 정확한 정의', ''.join(b)))

    a = []
    a.append('<h4>① 한 가지 형질의 유전 (순종 둥근 × 순종 주름진)</h4><div class="two">' + img('v_mono_exp', cap='멘델의 실험') +
             '''<div><div class="flow"><span>어버이 RR × rr</span><i>→</i><span class="k">잡종 1대: 모두 둥근 (Rr)</span><i>→ 자가 수분 →</i><span class="k">잡종 2대: 둥근 5474 : 주름진 1850 ≈ 3 : 1</span></div>''' + MONO_TABLE + '</div></div>')
    a.append(box('exp', '멘델의 가설 (교과서)', '1. 한 가지 형질은 <b>한 쌍의 유전 인자</b>(=유전자)에 의해 결정되며, 유전 인자는 부모에게서 하나씩 자손으로 전달된다.<br>2. 한 쌍의 유전 인자가 서로 다를 때 <b>하나만 형질로 표현</b>되고 나머지는 표현되지 않는다.<br>3. 한 쌍의 유전 인자는 생식세포가 만들어질 때 <b>나뉘어</b> 각 생식세포로 들어가고, 수정될 때 다시 쌍을 이룬다.'))
    a.append('''<table class="t"><tr><th style="width:20%">원리</th><th>내용</th><th style="width:30%">확인되는 곳</th></tr>
<tr><td><b>우열의 원리</b></td><td class="l">대립 형질이 다른 순종끼리 교배하면 잡종 1대에서 <b>우성 형질만</b> 나타난다</td><td class="l">잡종 1대가 모두 둥근 완두 (Rr)</td></tr>
<tr><td><b>분리의 법칙</b></td><td class="l">생식세포를 만들 때(감수 분열) 쌍을 이루던 <b>대립유전자가 분리</b>되어 서로 다른 생식세포로 들어간다</td><td class="l">잡종 1대(Rr)가 R : r = 1 : 1로 생식세포를 만들어 잡종 2대 3 : 1</td></tr></table>''' +
             box('tip', '분리의 법칙 ↔ 감수 1분열', '대립유전자는 상동 염색체의 같은 위치에 있다 → <b>감수 1분열 후기에 상동 염색체가 분리</b>될 때 대립유전자도 분리된다.'))
    a.append('<h4>② 검정 교배 — 우성 개체가 순종인지 잡종인지 알아내기</h4><p>우성 표현형 개체를 <b>열성 순종(rr)</b>과 교배한다.</p><table class="t"><tr><th>자손</th><th>판단</th><th>까닭</th></tr>'
             '<tr><td>모두 우성</td><td><b>RR</b> (순종)</td><td class="l">R만 만들어 자손이 모두 Rr</td></tr><tr><td>우성 : 열성 = 1 : 1</td><td><b>Rr</b> (잡종)</td><td class="l">R : r = 1 : 1 생식세포 → Rr : rr = 1 : 1</td></tr></table>'
             '<p class="small">자가 수분으로도 알 수 있다: 자손이 모두 우성이면 순종, 우성 : 열성 = 3 : 1이면 잡종.</p>')
    h.append(level('a', '한 가지 형질의 유전 — 우열의 원리 · 분리의 법칙', ''.join(a)))

    d = []
    d.append('<h4>① 두 가지 형질의 유전 (순종 둥글고 노란색 RRYY × 순종 주름지고 초록색 rryy)</h4><div class="two">' + img('v_di_exp', cap='멘델의 두 가지 형질 교배 실험') +
             '''<div><div class="flow"><span>잡종 1대: 모두 둥글고 노란색 (RrYy)</span></div><p>잡종 1대의 생식세포: <b>RY : Ry : rY : ry = 1 : 1 : 1 : 1</b><br>잡종 2대: 둥노 315 : 둥초 108 : 주노 101 : 주초 32 ≈ <b>9 : 3 : 3 : 1</b></p>
<ul class="pt"><li>씨 모양만: 둥근 (315+108) : 주름진 (101+32) = 423 : 133 ≈ <b>3 : 1</b></li><li>씨 색깔만: 노란 (315+101) : 초록 (108+32) = 416 : 140 ≈ <b>3 : 1</b></li></ul>
<p><b>독립의 법칙</b>: 두 쌍 이상의 대립유전자가 <b>서로 영향을 미치지 않고</b> 각각 분리의 법칙에 따라 독립적으로 유전된다.</p></div></div>''' + dihybrid_table())
    d.append('<h4>② 잡종 2대 16칸 해부</h4><table class="t"><tr><th>표현형 (비)</th><th>유전자형 (칸 수)</th><th>그중 순종</th></tr>'
             '<tr><td>둥글고 노란색 (9)</td><td>RRYY 1, RRYy 2, RrYY 2, RrYy 4</td><td>RRYY → 1/9</td></tr>'
             '<tr><td>둥글고 초록색 (3)</td><td>RRyy 1, Rryy 2</td><td>RRyy → 1/3</td></tr>'
             '<tr><td>주름지고 노란색 (3)</td><td>rrYY 1, rrYy 2</td><td>rrYY → 1/3</td></tr>'
             '<tr><td>주름지고 초록색 (1)</td><td>rryy 1</td><td>rryy → 1 (모두 순종)</td></tr></table>'
             '<p class="small">잡종 2대 전체에서 순종(RRYY, RRyy, rrYY, rryy)은 4/16 = 1/4. 유전자형의 종류는 9가지, 표현형은 4가지.</p>')
    d.append('<h4>③ 모의 실험</h4><div class="two">' + img('v_go_stones', cap='바둑알 모의 실험 (하이탑)') + '''<ul class="pt">
<li>주머니 2개 = 암술(난세포)·수술(꽃가루)의 <b>잡종 1대(Rr)</b>, 바둑알 = <b>생식세포</b>, R(검정)·r(흰) = 씨 모양 대립유전자</li>
<li>보지 않고 하나씩 꺼냄 = 생식세포 형성 시 <b>대립유전자의 분리</b>(분리의 법칙) · 짝 짓기 = <b>수정</b></li>
<li>20회 결과 예: RR 5 : Rr 10 : rr 5 → 1 : 2 : 1, 표현형 3 : 1</li>
<li>교과서는 <b>동전 2개(Y/y)</b>를 동시에 던짐 → 학급 전체를 합할수록 1 : 2 : 1에 가까워진다 (시행 횟수가 많을수록 이론값에 가까움)</li></ul></div>''')
    h.append(level('d', '두 가지 형질의 유전 — 독립의 법칙 · 16칸 해석', ''.join(d)))

    s = []
    s.append('<h4>① 확률로 푸는 유전 계산 (곱의 법칙)</h4><p>독립적으로 유전되는 두 형질은 <b>각각의 확률을 곱한다</b>.</p>'
             '<table class="t"><tr><th>질문 (RrYy 자가 수분)</th><th>계산</th><th>답</th></tr>'
             '<tr><td class="l">둥글고 노란색</td><td>3/4 × 3/4</td><td>9/16</td></tr>'
             '<tr><td class="l">주름지고 노란색</td><td>1/4 × 3/4</td><td>3/16</td></tr>'
             '<tr><td class="l">유전자형이 RrYy</td><td>1/2 × 1/2</td><td>1/4</td></tr>'
             '<tr><td class="l">잡종 2대 1600개 중 둥글고 초록색</td><td>1600 × 3/16</td><td>300개</td></tr>'
             '<tr><td class="l">둥근 완두(잡종 2대) 중 잡종(Rr)</td><td>Rr 2 / (RR 1 + Rr 2)</td><td>2/3</td></tr>'
             '<tr><td class="l">AaBbDd의 생식세포 종류</td><td>2 × 2 × 2</td><td>8가지</td></tr></table>')
    s.append('<h4>② 자손의 비로 부모 유전자형 거꾸로 찾기</h4><table class="t"><tr><th>자손의 표현형 비</th><th>부모 유전자형</th></tr>'
             '<tr><td>모두 우성</td><td>AA × AA, AA × Aa, AA × aa (한쪽이 AA)</td></tr><tr><td>우성 : 열성 = 3 : 1</td><td>Aa × Aa</td></tr>'
             '<tr><td>우성 : 열성 = 1 : 1</td><td>Aa × aa (검정 교배)</td></tr><tr><td>모두 열성</td><td>aa × aa</td></tr>'
             '<tr><td>9 : 3 : 3 : 1</td><td>AaBb × AaBb</td></tr><tr><td>1 : 1 : 1 : 1</td><td>AaBb × aabb 또는 Aabb × aaBb</td></tr>'
             '<tr><td>3 : 1 : 3 : 1</td><td>AaBb × Aabb (또는 AaBb × aaBb)</td></tr></table>'
             '<p class="small">예) 둥글고 노란색 (가) × rryy → 둥노 : 주노 = 1 : 1 → 씨 모양이 1:1이므로 Rr, 색은 모두 노란색이므로 YY → (가) = <b>RrYY</b>.</p>')
    s.append('<h4>③ 유전자와 염색체</h4><div class="two">' + img('v_indep_side', '70%', cap='독립의 법칙과 염색체') + '''<ul class="pt">
<li><b>서턴</b>: 유전 인자의 행동 = 감수 분열 때 염색체의 행동 → 유전자는 염색체에 있다 (염색체설)</li>
<li><b>모건</b>: 초파리 연구 → 유전자는 염색체의 일정한 위치에 있다 (유전자설)</li>
<li>독립의 법칙은 두 유전자가 <b>서로 다른 상동 염색체</b>에 있을 때만 성립한다. 같은 염색체에 있으면 함께 이동하므로(RrYy가 RY, ry 두 종류만 생성) 9:3:3:1이 나오지 않는다.</li></ul></div>''')
    s.append(box('exp', '멘델 원리의 예외 — 중간 유전 (교과서 최종 점검 09)', '분꽃 빨간색(RR) × 흰색(WW) → 자손 1대 <b>분홍색(RW)</b> → 자가 수분 → 빨강 : 분홍 : 흰 = <b>1 : 2 : 1</b>.<br>두 대립유전자 사이의 <b>우열 관계가 뚜렷하지 않아</b> 우열의 원리는 따르지 않지만, 대립유전자가 분리되어 생식세포로 들어가므로 <b>분리의 법칙은 따른다</b>. (표현형 비 = 유전자형 비)'))
    s.append('<h4>④ 멘델 유전 실험의 의의</h4><p>형질이 물감처럼 <b>섞여서 유전되지 않음</b>을 증명(당시의 혼합설 반박)하고, <b>유전 인자(유전자)</b>를 바탕으로 유전 원리를 설명하였다. 오늘날에도 여러 생물의 유전 현상을 연구하는 기본 원리이다.</p>')
    s.append(box('warn', '실수 방지 체크리스트', '''<ul class="pt">
<li>잡종 1대 Rr은 둥근 대립유전자만 가진 것이 아니다 — <b>r도 가지고 있다</b> (표현만 안 됨)</li>
<li>잡종 2대의 둥근 완두가 모두 순종인 것은 아니다 (RR 1 : Rr 2)</li>
<li>순종 판정: RR, rr, RRYY, <b>aaBBdd</b>(모든 쌍이 같으면 순종) / Rryy는 잡종</li>
<li>3 : 1은 <b>표현형</b> 비, 1 : 2 : 1은 <b>유전자형</b> 비</li>
<li>우열의 원리는 잡종 1대, 분리의 법칙은 잡종 2대(와 생식세포 형성), 독립의 법칙은 두 형질 이상에서 확인</li>
<li>"유전 인자는 염색체에 있다"는 멘델이 아니라 <b>서턴</b>의 주장 · 멘델은 한 세대가 <b>짧은</b> 완두를 사용</li>
<li>주름진 유전자와 초록색 유전자가 항상 함께 행동하지 않는다 (독립)</li></ul>'''))
    h.append(level('s', '확률 계산 · 역추적 · 염색체와의 연결 — 고난도 대비', ''.join(s)))
    return '\n'.join(h)
