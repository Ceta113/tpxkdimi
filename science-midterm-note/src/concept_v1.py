from lib import img, level, box

DNA_SVG = '''
<svg viewBox="0 0 700 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="세포 분열 중 핵 1개당 DNA 상대량 변화">
 <style>.ax{stroke:#1f2430;stroke-width:1.4}.gd{stroke:#e3e6ec}.t{font-size:11.5px;fill:#5b6272}.h{font-size:13.5px;font-weight:900;fill:#1f2430}.v{font-size:11px;fill:#1f2430}</style>
 <g transform="translate(20,20)">
  <text class="h" x="160" y="0" text-anchor="middle">체세포 분열</text>
  <line class="gd" x1="30" y1="40" x2="310" y2="40"/><line class="gd" x1="30" y1="70" x2="310" y2="70"/><line class="gd" x1="30" y1="100" x2="310" y2="100"/><line class="gd" x1="30" y1="130" x2="310" y2="130"/>
  <line class="ax" x1="30" y1="160" x2="312" y2="160"/><line class="ax" x1="30" y1="20" x2="30" y2="160"/>
  <text class="v" x="22" y="44" text-anchor="end">4</text><text class="v" x="22" y="104" text-anchor="end">2</text><text class="v" x="22" y="134" text-anchor="end">1</text>
  <polyline points="30,100 85,100 130,40 235,40 235,100 310,100" fill="none" stroke="#d9772b" stroke-width="3"/>
  <line x1="130" y1="30" x2="130" y2="160" stroke="#aab" stroke-dasharray="3 3"/><line x1="235" y1="30" x2="235" y2="160" stroke="#aab" stroke-dasharray="3 3"/>
  <text class="t" x="80" y="176" text-anchor="middle">간기 (DNA 복제)</text><text class="t" x="182" y="176" text-anchor="middle">분열기 (전·중·후·말)</text><text class="t" x="272" y="176" text-anchor="middle">딸세포</text>
  <text class="t" x="160" y="196" text-anchor="middle">염색체 수: 2n → 2n (변화 없음) · DNA: 2 → 4 → 2</text>
 </g>
 <g transform="translate(360,20)">
  <text class="h" x="160" y="0" text-anchor="middle">생식세포 분열 (감수 분열)</text>
  <line class="gd" x1="30" y1="40" x2="310" y2="40"/><line class="gd" x1="30" y1="70" x2="310" y2="70"/><line class="gd" x1="30" y1="100" x2="310" y2="100"/><line class="gd" x1="30" y1="130" x2="310" y2="130"/>
  <line class="ax" x1="30" y1="160" x2="312" y2="160"/><line class="ax" x1="30" y1="20" x2="30" y2="160"/>
  <text class="v" x="22" y="44" text-anchor="end">4</text><text class="v" x="22" y="104" text-anchor="end">2</text><text class="v" x="22" y="134" text-anchor="end">1</text>
  <polyline points="30,100 70,100 110,40 175,40 175,100 245,100 245,130 310,130" fill="none" stroke="#7b4bd1" stroke-width="3"/>
  <line x1="110" y1="30" x2="110" y2="160" stroke="#aab" stroke-dasharray="3 3"/><line x1="175" y1="30" x2="175" y2="160" stroke="#aab" stroke-dasharray="3 3"/><line x1="245" y1="30" x2="245" y2="160" stroke="#aab" stroke-dasharray="3 3"/>
  <text class="t" x="70" y="176" text-anchor="middle">간기 (복제)</text><text class="t" x="142" y="176" text-anchor="middle">감수 1분열</text><text class="t" x="210" y="176" text-anchor="middle">감수 2분열</text><text class="t" x="280" y="176" text-anchor="middle">생식세포</text>
  <text class="t" x="160" y="196" text-anchor="middle">염색체 수: 2n → n (감수1) → n (감수2) · DNA: 2 → 4 → 2 → 1</text>
 </g>
</svg>'''


def build():
    h = []
    b = []
    b.append('<h4>① 세포 분열이 필요한 까닭</h4><p>생물이 자랄 때(<b>생장</b>) 세포가 계속 커지는 것이 아니라 <b>세포의 수가 늘어난다</b>. 세포가 커지면 <b>부피가 증가하는 비율보다 표면적이 증가하는 비율이 작아</b> 부피에 대한 표면적의 비(표면적/부피)가 작아지고, 표면을 통한 <b>물질 교환이 비효율적</b>이 된다. → 어느 정도 커지면 분열한다.</p>'
             '<table class="t"><tr><th>정육면체 한 변</th><th>1 cm</th><th>2 cm</th><th>3 cm</th></tr><tr><td>표면적 (6×한 변²)</td><td>6</td><td>24</td><td>54</td></tr><tr><td>부피 (한 변³)</td><td>1</td><td>8</td><td>27</td></tr><tr><td><b>표면적/부피</b></td><td class="red">6</td><td>3</td><td>2</td></tr></table>'
             '<p class="small">용어: 분열 전 세포 = <b>모세포</b>, 분열로 생긴 세포 = <b>딸세포</b>.</p>')
    b.append('<h4>② 염색체 · DNA · 유전자</h4><div class="two"><div>' + img('v_chrom_structure', cap='염색체의 구조') + img('v_homologous', '60%', cap='상동 염색체와 염색 분체') + '</div><div><ul class="pt">'
             '<li><b>염색체</b> = <b>DNA + 단백질</b>. 분열하지 않을 때는 핵 속에 실처럼 풀어져 있다가, <b>분열할 때 응축되어 막대 모양</b>으로 보인다.</li>'
             '<li><b>염색 분체</b>: 하나의 염색체를 이루는 두 가닥. 분열 전 <b>DNA가 복제</b>되어 만들어졌으므로 <b>유전 정보가 같다</b>.</li>'
             '<li><b>유전자</b>: DNA에서 유전 정보를 저장하고 있는 특정 부위. (정보막대=염색체, 저장된 파일=유전자)</li>'
             '<li><b>상동 염색체</b>: 모양과 크기가 같은 한 쌍. <b>부모에게서 하나씩</b> 물려받으므로 유전 정보는 서로 <b>다를 수 있다</b>.</li>'
             '<li><b>상염색체</b>: 남녀 공통 (사람 1~22번, 44개) · <b>성염색체</b>: 성 결정 (X, Y)</li>'
             '<li>사람 체세포: <b>46개 = 23쌍</b>. 여자 <b>44+XX</b>, 남자 <b>44+XY</b>.<br>남자의 X는 <b>어머니</b>, Y는 <b>아버지</b>에게서. 여자의 X는 부모에게서 하나씩.</li>'
             '<li>핵상 표기: 상동 염색체 쌍이 있으면 <b>2n</b>(사람 2n=46), 없으면 <b>n</b>(생식세포 n=23).</li></ul></div></div>')
    b.append('<div class="two">' + img('v_karyotype', cap='여자 44+XX / 남자 44+XY') +
             '<table class="t"><tr><th>생물</th><th>염색체 수</th><th>생물</th><th>염색체 수</th></tr><tr><td>사람</td><td>46</td><td>초파리</td><td>8</td></tr><tr><td>개</td><td>78</td><td>벼</td><td>24</td></tr><tr><td>고양이</td><td>38</td><td>완두</td><td>14</td></tr><tr><td>침팬지</td><td>48</td><td>감자</td><td>48</td></tr></table></div>' +
             box('warn', '주의', '염색체 수가 많다고 더 진화한 생물이 아니다. 침팬지와 감자는 48개로 같지만 염색체의 모양과 크기가 다르다. 같은 종이면 생식세포를 제외한 모든 세포의 염색체 수가 같다.'))
    b.append('<h4>③ 생식 기관과 생식세포</h4><div class="two">' + img('v_repro_organs', cap='남자와 여자의 생식 기관') + '''<table class="t">
<tr><th></th><th>정자</th><th>난자</th></tr><tr><td>생성 장소</td><td>정소</td><td>난소</td></tr><tr><td>염색체 수</td><td>23</td><td>23</td></tr>
<tr><td>크기</td><td>작다</td><td>크다</td></tr><tr><td>양분(세포질)</td><td>거의 없다</td><td>많다</td></tr><tr><td>운동성</td><td>있다 (꼬리)</td><td>없다</td></tr></table></div>
<ul class="pt"><li>정소(정자 생성) → 부정소(정자가 잠시 머물며 성숙) → 수정관(정자 이동 통로)</li><li>난소(난자 생성·배란) → 수란관(수정이 일어나는 곳, 난자·수정란 이동) → 자궁(태아가 자라는 곳) → 질</li></ul>''')
    h.append(level('b', '세포 분열 · 염색체 · 생식 기관 — 용어 확실히', ''.join(b)))

    a = []
    a.append('<h4>① 체세포 분열 — 염색체 수 유지 (2n → 2n)</h4><p><b>세포 주기</b> = 간기 + 분열기. <b>간기</b>: 세포가 자라고 <b>DNA 복제</b>, 세포 주기의 대부분을 차지, 핵막이 뚜렷하고 염색체는 안 보인다.</p>' + img('v_mitosis_table', cap='체세포 분열 과정 (하이탑)') + '''
<table class="t"><tr><th>시기</th><th>핵심 한 줄</th></tr>
<tr><td>전기</td><td class="l"><b>핵막이 사라지고</b>, 두 가닥의 염색 분체로 된 <b>막대 모양 염색체</b>가 나타남, 방추사 형성</td></tr>
<tr><td>중기</td><td class="l">염색체가 <b>세포 가운데 배열</b> → 염색체 관찰에 가장 좋은 시기</td></tr>
<tr><td>후기</td><td class="l"><b>염색 분체가 분리</b>되어 양 끝(양극)으로 이동</td></tr>
<tr><td>말기</td><td class="l">염색체가 풀어지고 <b>핵막이 다시 나타나</b> 2개의 핵 → 세포질 분열</td></tr></table>''' +
             '<div class="two">' + img('v_cytokinesis', cap='세포질 분열') + '<ul class="pt"><li><b>동물 세포</b>: 세포막이 바깥에서 안쪽으로 <b>잘록하게 함입</b></li><li><b>식물 세포</b>: 두 핵 사이에 <b>세포판</b>이 생겨 안에서 바깥으로 자람</li>'
             '<li><b>결과·의의</b>: 모세포와 <b>염색체 수·유전 정보가 같은</b> 딸세포 2개 → <b>생장</b>(다세포), <b>재생</b>(도마뱀 꼬리, 상처), <b>번식</b>(단세포 생물: 아메바·짚신벌레·세균의 분열법)</li>'
             '<li>관찰 장소: 식물 <b>뿌리 끝·줄기 끝 생장점, 형성층</b> / 동물 온몸</li></ul></div>')
    a.append('<h4>② 생식세포 분열 (감수 분열) — 염색체 수 절반 (2n → n)</h4>' + img('v_bivalent', '38%', cap='상동 염색체가 접합한 2가 염색체') +
             img('v_meiosis1', cap='감수 1분열') + img('v_meiosis2', cap='감수 2분열') + '''
<table class="t"><tr><th></th><th>감수 1분열</th><th>감수 2분열</th></tr>
<tr><td>핵심 사건</td><td>전기에 <b>2가 염색체</b> 형성 → 후기에 <b>상동 염색체 분리</b></td><td>간기 없이(<b>DNA 복제 없이</b>) 바로 시작 → 후기에 <b>염색 분체 분리</b></td></tr>
<tr><td>염색체 수</td><td class="red">2n → n (절반)</td><td>n → n (변화 없음)</td></tr>
<tr><td>DNA양 (핵 1개당)</td><td>4 → 2</td><td>2 → 1</td></tr>
<tr><td>결과</td><td>딸세포 2개</td><td>딸세포 4개 (정자·난자)</td></tr></table>''' +
             box('key', '생식세포 분열의 의의', '① 염색체 수가 절반인 생식세포가 수정하므로 <b>세대를 거듭해도 자손의 염색체 수가 일정</b>하게 유지된다 (23+23=46).<br>② 감수 1분열 중기에 상동 염색체 쌍이 <b>무작위로 배열·분리</b> → 유전적으로 <b>다양한 생식세포</b> → 자손의 다양성.') +
             img('v_chrom_constant', '70%', cap='세대를 거듭해도 염색체 수 유지'))
    a.append('<h4>③ 수정과 발생</h4>' + img('v_early_dev', '78%', cap='사람의 초기 발생 과정') + '''
<div class="flow"><span>배란 (난소)</span><i>→</i><span class="k">수정 (수란관)</span><i>→</i><span>난할 (수란관을 따라 이동)</span><i>→</i><span class="k">착상 (수정 약 1주 후, 포배 상태로 자궁 안쪽 벽)</span><i>→</i><span>태반 형성 · 태아 발생</span><i>→</i><span>출산 (수정 약 266일=38주)</span></div>
<ul class="pt"><li><b>수정란</b>: 정자(23) + 난자(23) → <b>46</b> (체세포와 같다)</li>
<li><b>난할</b>: 수정란의 초기 세포 분열 (체세포 분열의 일종). 딸세포가 <b>자라지 않고</b> 빠르게 분열 → 세포 수 ↑, 세포 하나 크기 ↓, 염색체 수 그대로, 배아 전체 크기는 수정란과 비슷</li>
<li><b>포배</b>: 속이 빈 공 모양의 배 · <b>임신</b>: 착상된 때부터 · <b>태아</b>: 수정 후 8주 이후(사람의 모습)</li>
<li><b>태반</b>: 모체와 태아 사이 물질 교환 (영양소·산소 → 태아, 이산화 탄소·노폐물 → 모체)</li>
<li><b>발생</b>: 수정란이 세포 분열을 하며 조직·기관을 형성하여 하나의 개체가 되는 과정 (세포 수 증가 + 세포의 종류가 다양해짐)</li></ul>''' +
             '<div class="two">' + img('v_cleavage_model', cap='난할 과정 모형') + img('v_fetus', cap='태아의 발생 (6주·8주·16주·24주)') + '</div>')
    h.append(level('a', '체세포 분열 · 생식세포 분열 · 발생 — 과정 순서대로', ''.join(a)))

    d = []
    d.append('<h4>① 탐구 3종 완벽 정리</h4><div class="two"><div>' + img('v_agar', cap='세포의 표면적과 부피 (하이탑)') + '''<ul class="pt"><li>A: 2 cm 정육면체 1개 / B: 1 cm 정육면체 8개 → <b>총부피 같음(8)</b>, 표면적 A 24, B <b>48</b></li>
<li>식용 색소에 10분 → B는 중심까지 물들고 A는 중심이 흰색</li><li>결론: 작을수록 <b>표면적/부피</b>가 커서 물질 교환에 유리 → 세포 분열로 수를 늘려 생장</li>
<li>교과서: 4×2×2 cm 직육면체(부피 16, 표면적 40) vs 2 cm 정육면체 2개(부피 16, 표면적 48)</li></ul></div><div>''' +
             img('v_onion_steps', cap='양파 뿌리 끝 체세포 분열 관찰') + '''<table class="t"><tr><th>과정</th><th>약품·조작</th><th>목적</th></tr>
<tr><td>고정</td><td class="l">에탄올:아세트산 = 3:1</td><td class="l">세포를 <b>살아 있을 때 모습</b>으로 유지</td></tr>
<tr><td>해리</td><td class="l">묽은 염산, 55~60℃ 물중탕</td><td class="l">조직을 <b>연하게</b> → 세포가 잘 분리</td></tr>
<tr><td>염색</td><td class="l">아세트산 카민 용액</td><td class="l"><b>핵과 염색체</b>를 붉게</td></tr>
<tr><td>분리</td><td class="l">해부 침으로 잘게 찢기</td><td class="l">세포를 서로 떼어 놓기</td></tr>
<tr><td>압착</td><td class="l">거름종이 위로 엄지로 누름</td><td class="l">세포를 <b>한 층으로 얇게</b> 펴기</td></tr></table>
<p class="small">관찰 결과: <b>간기 세포가 가장 많다</b> → 간기가 세포 주기에서 가장 긴 시기. 뿌리 끝 <b>생장점</b>에서 관찰.</p></div></div>''' +
             img('v_lily', '80%', cap='백합 꽃밥에서 생식세포 분열 관찰 (고정·염색 방법은 양파와 같음)'))
    d.append('<h4>② 체세포 분열 vs 생식세포 분열 한눈에</h4>' + img('v_mito_vs_meio', '82%') + '''
<table class="t"><tr><th>구분</th><th>체세포 분열</th><th>생식세포 분열</th></tr>
<tr><td>분열 횟수</td><td>1회</td><td>연속 2회</td></tr><tr><td>딸세포 수</td><td>2개</td><td>4개</td></tr>
<tr><td>2가 염색체</td><td>형성 안 됨</td><td>감수 1분열 전기에 형성</td></tr>
<tr><td>염색체 수 변화</td><td>변화 없음 (2n → 2n)</td><td>절반 (2n → n)</td></tr>
<tr><td>딸세포 유전자 구성</td><td>모세포와 같다</td><td>모세포와 다르며 다양</td></tr>
<tr><td>분열 결과</td><td>생장, 재생, 단세포 생물 번식</td><td>생식세포 형성</td></tr>
<tr><td>분열 장소</td><td>동물: 몸 전체 / 식물: 생장점, 형성층</td><td>동물: 정소, 난소 / 식물: 꽃밥, 밑씨</td></tr>
<tr><td>공통점</td><td colspan="2">분열 전 간기에 DNA 복제 · 분열기에 염색체 응축 · 염색 분체 분리가 일어남</td></tr></table>''')
    d.append('<h4>③ 난할의 특징 표</h4><table class="t"><tr><th>구분</th><th>수정란</th><th>2세포배</th><th>4세포배</th><th>8세포배</th><th>16세포배</th></tr>'
             '<tr><td>세포 수</td><td>1</td><td>2</td><td>4</td><td>8</td><td>16</td></tr><tr><td>세포 하나의 상대적 크기</td><td>1</td><td>1/2</td><td>1/4</td><td>1/8</td><td>1/16</td></tr>'
             '<tr><td>세포 하나의 염색체 수</td><td>46</td><td>46</td><td>46</td><td>46</td><td>46</td></tr><tr><td>배 전체 크기</td><td colspan="5">거의 일정 (세포 수 × 세포 크기)</td></tr></table>')
    h.append(level('d', '탐구 · 비교 · 난할 — 표로 정리', ''.join(d)))

    s = []
    s.append('<h4>① DNA 상대량 그래프</h4>' + DNA_SVG + '''<ul class="pt"><li>그래프가 <b>2 → 4로 올라가는 구간 = 간기(DNA 복제)</b></li><li>체세포: 4 → 2 한 번 · 생식세포: 4 → 2 → 1 두 번 (두 번째 감소 = 감수 2분열)</li>
<li>염색체 <b>수</b>는 감수 1분열에서만 절반. 감수 2분열은 염색체 수 그대로, DNA양만 절반.</li></ul>''')
    s.append('<h4>② 사람 세포의 수 세기 (2n = 46)</h4><table class="t"><tr><th>시기</th><th>염색체 수</th><th>염색 분체 수</th><th>DNA 상대량</th><th>상동 염색체</th></tr>'
             '<tr><td>간기 (복제 전)</td><td>46</td><td>–</td><td>2</td><td>있음</td></tr>'
             '<tr><td>체세포 분열 전기·중기</td><td>46</td><td>92</td><td>4</td><td>있음 (2가 X)</td></tr>'
             '<tr><td>감수 1분열 전기·중기</td><td>46 (2가 23개)</td><td>92</td><td>4</td><td>있음 (2가 O)</td></tr>'
             '<tr><td>감수 2분열 전기·중기</td><td>23</td><td>46</td><td>2</td><td class="red">없음</td></tr>'
             '<tr><td>정자·난자</td><td>23</td><td>–</td><td>1</td><td class="red">없음</td></tr></table>'
             '<p class="small">2n=2k인 생물의 생식세포 염색체 조합 수 = 2<sup>k</sup> (예: 2n=4 → 4가지, 2n=6 → 8가지, 사람 → 2<sup>23</sup>가지)</p>')
    s.append('<h4>③ 세포 그림 보고 시기 판단하기</h4><ol class="pt">'
             '<li><b>핵막이 있고 염색체가 안 보임</b> → 간기</li>'
             '<li>상동 염색체끼리 <b>붙어 있다(2가 염색체)</b> → 감수 1분열 (전기·중기)</li>'
             '<li>세포 안에 모양·크기가 같은 쌍이 있는데 <b>2가가 아님</b>, 한 줄로 배열 → 체세포 분열 중기</li>'
             '<li>모든 염색체의 <b>모양이 서로 다름(상동 없음)</b> + 두 가닥 → 감수 2분열</li>'
             '<li>양극으로 이동하는 것이 <b>두 가닥 염색체</b> → 감수 1분열 후기 / <b>한 가닥</b>인데 한쪽 극에 상동 쌍 있음 → 체세포 후기, 상동 쌍 없음 → 감수 2분열 후기</li></ol>')
    s.append('<h4>④ 난할의 세포 주기 (심화)</h4><div class="two">' + img('v_cycle_rings', cap='(가) 일반 체세포 (나) 난할') + img('v_cleavage_graph', cap='난할 시 DNA양·세포 수·세포 크기') + '</div>'
             '<p>세포 주기의 간기 = G<sub>1</sub>기(생장) + S기(DNA 복제) + G<sub>2</sub>기(분열 준비). 일반 체세포는 90% 이상이 간기지만, <b>난할은 G<sub>1</sub>·G<sub>2</sub>기가 거의 없어</b> 세포가 생장하지 않고 DNA 복제 후 바로 분열한다 → 분열이 빠르고, 세포 크기가 점점 작아진다. 세포 1개당 DNA양과 염색체 수는 일정하게 유지.</p>'
             '<p class="small">난자는 <b>감수 1분열까지만 마친 상태로 배란</b>되고, 정자가 들어오면 감수 2분열을 완료한다 (하이탑 최상위 4번).</p>')
    s.append(box('warn', '실수 방지 체크리스트', '''<ul class="pt">
<li>염색 분체 두 가닥 = <b>같은</b> 유전 정보 / 상동 염색체 두 개 = 부모에게서 온 <b>다를 수 있는</b> 유전 정보</li>
<li>체세포 분열에서도 <b>상동 염색체는 존재</b>하지만 접합(2가)하지 않는다</li>
<li>상동 염색체 <b>분리 = 감수 1분열</b>, 염색 분체 분리 = 체세포 분열·감수 2분열</li>
<li>감수 1분열과 2분열 사이에 <b>DNA 복제 없음</b></li>
<li>양파 뿌리 끝 = 체세포 분열 관찰 (감수 분열 X) · 꽃밥 = 생식세포 분열</li>
<li>염산 처리는 세포 분열 촉진이 아니라 <b>조직을 연하게(해리)</b> · 아세트산 카민은 방추사가 아니라 <b>핵·염색체</b> 염색</li>
<li>난할이 진행돼도 세포 하나의 <b>염색체 수는 줄지 않는다</b> · 세포질 양은 감소</li>
<li>남자의 X 염색체는 반드시 <b>어머니</b>에게서, Y는 <b>아버지</b>에게서</li>
<li>세포 주기 분열기의 구분 기준은 <b>염색체의 모양과 행동</b></li></ul>'''))
    h.append(level('s', '그래프 · 수 세기 · 시기 판단 — 고난도 대비', ''.join(s)))
    return '\n'.join(h)
