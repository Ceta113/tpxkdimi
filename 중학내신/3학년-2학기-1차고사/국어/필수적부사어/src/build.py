"""필수적 부사어 집중 노트.  실행: python3 src/build.py"""
import os, json, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), '필수적부사어_노트.pdf')

CSS = """
@page{size:A4;margin:14mm 13mm 15mm}
*{box-sizing:border-box}html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;font-family:'Noto Sans KR';font-size:9.8pt;line-height:1.62;color:#1b1d22;word-break:keep-all}
.head{background:#14213d;color:#fff;border-radius:8px;padding:14px 18px 12px;margin-bottom:12px}
.head .k{font-size:8.5pt;letter-spacing:.25em;color:#aab3c5}
.head h1{margin:2px 0 3px;font-family:'Noto Serif KR';font-weight:900;font-size:24pt}
.head p{margin:0;color:#d8dde8;font-size:9pt}
.lv{border:1.5px solid var(--c);border-radius:9px;margin:0 0 12px;overflow:hidden}
.lv>h2{margin:0;padding:6px 12px;background:var(--l);font-size:12pt;display:flex;align-items:center;gap:8px;break-after:avoid}
.lv>h2 span{background:var(--c);color:#fff;border-radius:5px;padding:1px 9px;font-size:9pt}
.lv .in{padding:6px 13px 10px}
.b{--c:#1f9d62;--l:#e8f6ee}.a{--c:#2f6fd6;--l:#eaf2fd}.d{--c:#7e57c2;--l:#f1ebfd}.s{--c:#d6334a;--l:#fde8ec}
h3{font-size:10.5pt;margin:10px 0 5px;break-after:avoid}
table{width:100%;border-collapse:collapse;margin:6px 0;font-size:9pt}
th,td{border:1px solid #cfd5dd;padding:4px 7px;vertical-align:top}th{background:#eef1f6}
tr{break-inside:avoid}td.c,th.c{text-align:center}
.ok{color:#1f9d62;font-weight:700}.no{color:#d6334a;font-weight:700}
u.m{text-decoration:none;background:linear-gradient(transparent 55%,#ffe58a 55%);font-weight:700}
.box{border-radius:7px;padding:7px 11px;margin:8px 0;break-inside:avoid}
.key{background:#eaf2fd;border:1px solid #9cc3ff}.tip{background:#fff8e6;border:1px solid #f0dca6}.warn{background:#fdecee;border:1px solid #f1a9b3}
.box b.t{display:block;margin-bottom:2px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:10px}
svg{width:100%;height:auto}
.q{break-inside:avoid;margin:0 0 11px}.q .n{font-weight:900;color:#14213d;margin-right:5px}
.q ul{list-style:none;padding:0;margin:3px 0 0 18px}.q .bx{border:1px solid #9aa1ad;border-radius:4px;padding:4px 8px;margin:4px 0 0 18px;font-size:9pt}
.cols{columns:2;column-gap:8mm;column-rule:1px solid #dde1e7}
.ln{border-bottom:1px dashed #aab;height:20px;margin-left:18px}
.pb{break-before:page}
.ans td:first-child{width:34px;text-align:center;font-weight:700}.ans td:nth-child(2){width:18%;color:#d6334a;font-weight:700}
"""

def slots(verb, items):
    """서술어가 요구하는 자리 도식. items: (라벨, 예, 종류)  종류: s=주어 o=목적어 m=필수 부사어"""
    col = {'s': ('#eef1f6', '#5b6272'), 'o': ('#eef1f6', '#5b6272'), 'm': ('#fff3c4', '#b77a00'), 'v': ('#14213d', '#14213d')}
    x, parts = 4, []
    for lab, ex, k in items + [(verb, '서술어', 'v')]:
        w = 30 + 12 * max(len(ex), len(lab))
        fill, st = col[k]
        tc = '#fff' if k == 'v' else '#1b1d22'
        parts.append(f'<rect x="{x}" y="6" width="{w}" height="44" rx="7" fill="{fill}" stroke="{st}" stroke-width="{2 if k=="m" else 1}"/>'
                     f'<text x="{x+w/2}" y="25" text-anchor="middle" font-size="13" font-weight="700" fill="{tc}">{lab}</text>'
                     f'<text x="{x+w/2}" y="42" text-anchor="middle" font-size="10.5" fill="{"#cfd6e4" if k=="v" else "#5b6272"}">{ex}</text>')
        x += w + 8
    return f'<svg viewBox="0 0 {x} 56" style="max-width:{x*1.1:.0f}px">{"".join(parts)}</svg>'


def body():
    h = ['<div class="head"><div class="k">중학 국어 3-2 · 문장 성분 집중</div><h1>필수적 부사어</h1><p>부속 성분인데도 빠지면 문장이 무너지는 부사어 — 개념 4단계 · 확인 문제 20 · 정답과 해설</p></div>']

    # 기본
    h.append('''<section class="lv b"><h2><span>기본</span>부사어부터 다시 — 필수적 부사어의 정의</h2><div class="in">
<p><b>부사어</b>는 주로 용언(서술어)을 꾸며 주는 <b>부속 성분</b>이다. 부속 성분은 보통 빼도 문장이 성립한다.</p>
<table><tr><th style="width:22%">부사어의 형식</th><th>예</th></tr>
<tr><td>① 부사 그 자체</td><td>비행기가 <u class="m">매우</u> 빠르다.</td></tr>
<tr><td>② 체언 + 부사격 조사</td><td>책을 <u class="m">가방에</u> 넣었다. / 나는 <u class="m">너와</u> 다르다. / 그를 <u class="m">제자로</u> 삼았다.</td></tr>
<tr><td>③ 용언 어간 + -게</td><td>강아지가 <u class="m">귀엽게</u> 생겼다.</td></tr></table>
<div class="box key"><b class="t">필수적 부사어란?</b>서술어가 <b>반드시 필요로 하는</b> 부사어. 빼면 문장이 <b>불완전</b>해지거나 <b>뜻이 달라진다</b>.<br>→ 성분 종류는 여전히 <b>부속 성분(부사어)</b>이지만, 문장 구성에는 <b>필수</b>다.</div>
<div class="two"><div><h3>수의적 부사어 (빼도 됨)</h3>그는 <u class="m">빨리</u> 달렸다. → 그는 달렸다. <span class="ok">(자연스러움)</span><br>어제 <u class="m">학교에서</u> 공부했다. → 어제 공부했다. <span class="ok">(자연스러움)</span></div>
<div><h3>필수적 부사어 (빼면 안 됨)</h3>나는 <u class="m">너와</u> 다르다. → 나는 다르다. <span class="no">(무엇과?)</span><br>그를 <u class="m">제자로</u> 삼았다. → 그를 삼았다. <span class="no">(어색)</span></div></div>
<div class="box tip"><b class="t">판별법 — "빼 보기"</b>밑줄 친 부사어를 지우고 읽어 본다. ① 문장이 어색하다 / ② "무엇과? 누구에게? 어디에? 무엇으로?"라는 질문이 저절로 생긴다 / ③ 뜻이 달라진다 → <b>필수적 부사어</b>.</div>
</div></section>''')

    # 응용
    rows = [
        ('비교·같음·다름', '같다, 다르다, 비슷하다, 닮다', '~와/과', '이것은 <u class="m">저것과</u> 같다. / 형은 <u class="m">아빠와</u> 닮았다.', '이것은 같다. (무엇과?)'),
        ('주고받기', '주다, 드리다, 보내다, 건네다', '~에게/께', '그는 <u class="m">친구에게</u> 선물을 주었다. / <u class="m">할머니께</u> 편지를 드렸다.', '그는 선물을 주었다. (누구에게?)'),
        ('자격·지위 부여', '삼다, 여기다, 뽑다', '~(으)로', '그를 <u class="m">제자로</u> 삼았다. / 그를 <u class="m">친구로</u> 여겼다.', '그를 삼았다. (어색)'),
        ('위치에 두기', '넣다, 두다, 놓다, 얹다', '~에', '책을 <u class="m">가방에</u> 넣었다. / 컵을 <u class="m">식탁에</u> 놓았다.', '책을 넣었다. (어디에?)'),
        ('변화의 결과', '되다, 변하다, 바뀌다', '~(으)로', '물이 <u class="m">얼음으로</u> 되었다. / 신호가 <u class="m">초록불로</u> 바뀌었다.', '물이 되었다. (무엇으로?)'),
        ('모양·생김새', '생기다(모양)', '~게', '강아지가 <u class="m">귀엽게</u> 생겼다.', '강아지가 생겼다. (뜻이 달라짐)'),
    ]
    tr = ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td class="c">{c}</td><td>{d}</td><td class="no" style="font-weight:500">{e}</td></tr>' for a, b, c, d, e in rows)
    h.append(f'''<section class="lv a"><h2><span>응용</span>필수적 부사어를 부르는 서술어 6유형</h2><div class="in">
<p>필수적 부사어는 <b>서술어가 무엇이냐</b>로 결정된다. 아래 서술어가 보이면 먼저 의심하자.</p>
<table><tr><th style="width:14%">유형</th><th style="width:20%">대표 서술어</th><th style="width:9%">모양</th><th>예문</th><th style="width:19%">빼 보면</th></tr>{tr}</table>
<h3>서술어가 요구하는 자리로 보기</h3>
{slots('주었다', [('누가', '그는', 's'), ('누구에게', '친구에게', 'm'), ('무엇을', '선물을', 'o')])}
{slots('다르다', [('누가', '나는', 's'), ('무엇과', '너와', 'm')])}
{slots('삼았다', [('누가', '스승은', 's'), ('누구를', '그를', 'o'), ('무엇으로', '제자로', 'm')])}
<p style="font-size:8.8pt;color:#555">노란 칸이 필수적 부사어. 서술어마다 꼭 채워야 하는 <b>자리 수</b>가 정해져 있다 — '주다'는 주어·목적어·부사어 3자리, '다르다'는 주어·부사어 2자리.</p>
</div></section>''')

    # 발전
    h.append('''<section class="lv d"><h2><span>발전</span>헷갈리는 짝 구별하기</h2><div class="in">
<h3>① 같은 서술어라도 뜻에 따라 달라진다</h3>
<table><tr><th>서술어</th><th>필수적 부사어 필요 <span class="ok">O</span></th><th>필요 <span class="no">X</span></th></tr>
<tr><td class="c">생기다</td><td>강아지가 <u class="m">귀엽게</u> 생겼다. (생김새)</td><td>문제가 생겼다. (발생하다)</td></tr>
<tr><td class="c">두다</td><td>책을 <u class="m">책상에</u> 두었다. (놓다)</td><td>할아버지와 바둑을 두었다. (놀이를 하다)</td></tr>
<tr><td class="c">되다</td><td>물이 <u class="m">얼음으로</u> 되었다. (변하다)</td><td>그는 의사가 되었다. → '의사가'는 <b>보어</b></td></tr></table>
<h3>② 필수적 부사어 vs 보어 — "되다" 앞 조사를 보라</h3>
<table><tr><th></th><th>보어</th><th>필수적 부사어</th></tr>
<tr><td class="c">조건</td><td>'되다/아니다' 앞 + 보격 조사 <b>이/가</b></td><td>서술어가 요구 + <b>부사격 조사</b>(에게, 와, (으)로, 에) 또는 -게</td></tr>
<tr><td class="c">예</td><td>물이 <b>얼음이</b> 되었다.</td><td>물이 <b>얼음으로</b> 되었다.</td></tr>
<tr><td class="c">성분 종류</td><td><b>주성분</b></td><td><b>부속 성분</b> (필수이긴 하지만!)</td></tr></table>
<h3>③ 필수적 부사어 vs 위치 이동이 불가능한 부사어 — 포함 관계 X (필기)</h3>
<table><tr><th></th><th>필수적 부사어</th><th>이동 불가 부사어</th></tr>
<tr><td class="c">따지는 것</td><td><b>빼면</b> 문장이 무너지나?</td><td><b>자리를 옮기면</b> 어색한가?</td></tr>
<tr><td class="c">예</td><td>강아지가 <u class="m">귀엽게</u> 생겼다.</td><td>애가 아직 잠에 <u class="m">안</u> 들었다. (안 → 서술어 바로 앞만)</td></tr>
<tr><td class="c">빼 보면</td><td class="no">어색 → 필수</td><td class="ok">애가 아직 잠에 들었다 → 성립 (필수 아님)</td></tr></table>
<h3>④ '와/과' — 접속 조사일 때는 필수적 부사어가 아니다</h3>
<table><tr><th>문장</th><th>'와'의 정체</th><th>성분</th></tr>
<tr><td>형은 <b>아빠와</b> 닮았다.</td><td>부사격 조사 (비교 대상)</td><td>'아빠와' = 필수적 부사어</td></tr>
<tr><td><b>철수와 영희는</b> 닮았다.</td><td>접속 조사 (두 사람을 같은 자격으로 연결)</td><td>'철수와 영희는' 전체가 주어</td></tr></table>
<div class="box tip"><b class="t">구별 요령</b>'와/과' 앞뒤를 바꿔도(영희와 철수는) 뜻이 같고, 둘이 함께 주어가 되면 → 접속 조사. 비교·동반의 상대를 나타내면 → 부사격 조사.</div>
</div></section>''')

    # 심화
    h.append('''<section class="lv s"><h2><span>심화</span>시험 함정 체크리스트</h2><div class="in">
<table><tr><th style="width:48%">틀린 선지 (함정)</th><th>바로잡기</th></tr>
<tr><td>필수적 부사어는 문장에 꼭 필요하므로 <b>주성분</b>이다.</td><td>필수여도 성분 종류는 <b>부속 성분(부사어)</b>. 주성분은 주어·서술어·목적어·보어뿐.</td></tr>
<tr><td>'물이 얼음으로 되었다'의 '얼음으로'는 보어이다.</td><td>'으로'는 부사격 조사 → <b>필수적 부사어</b>. 보어는 '얼음<b>이</b> 되었다'.</td></tr>
<tr><td>위치를 옮길 수 없는 부사어는 모두 필수적 부사어이다.</td><td>기준이 다른 별개 개념 → <b>포함 관계 X</b>.</td></tr>
<tr><td>'그는 빨리 달렸다'의 '빨리'는 필수적 부사어이다.</td><td>빼도 '그는 달렸다' 성립 → <b>수의적</b> 부사어.</td></tr>
<tr><td>'문제가 생겼다'에는 필수적 부사어가 빠져 있다.</td><td>'생기다'가 <b>발생</b>의 뜻이면 부사어가 필요 없다.</td></tr>
<tr><td>필수적 부사어는 반드시 체언 + 부사격 조사 형태이다.</td><td>'용언 어간 + -게'도 가능 (귀엽게 생겼다).</td></tr>
<tr><td>'철수와 영희는 닮았다'의 '철수와'는 필수적 부사어이다.</td><td>'와'가 접속 조사 → '철수와 영희는'이 주어.</td></tr></table>
<div class="box warn"><b class="t">한 줄 요약</b>필수적 부사어 = <b>서술어가 요구해서 빼면 안 되는 부사어</b>. 같다·다르다·닮다(와) / 주다·드리다·보내다(에게) / 삼다·여기다(로) / 넣다·두다·놓다(에) / 되다·변하다(로) / 생기다(게).</div>
</div></section>''')

    # 문제
    Q = [
        ('밑줄 친 부사어를 빼면 문장이 불완전해지는 것은?', None, ['그는 <u>빨리</u> 달렸다.', '<u>어제</u> 비가 왔다.', '나는 <u>너와</u> 다르다.', '이 빵은 <u>정말</u> 맛있다.', '그는 <u>조용히</u> 앉았다.'], '③', "'다르다'는 비교 대상이 꼭 필요."),
        ('필수적 부사어가 쓰인 문장을 모두 고른 것은?', 'ㄱ. 그는 친구에게 선물을 주었다.　ㄴ. 동생이 학교에서 공부한다.<br>ㄷ. 그를 제자로 삼았다.　ㄹ. 새가 하늘을 높이 난다.', ['ㄱ, ㄴ', 'ㄱ, ㄷ', 'ㄴ, ㄷ', 'ㄴ, ㄹ', 'ㄷ, ㄹ'], '②', 'ㄴ·ㄹ은 빼도 성립하는 수의적 부사어.'),
        ('필수적 부사어에 대한 설명으로 옳은 것은?', None, ['문장의 주성분이다.', '서술어가 반드시 요구하는 부사어이다.', '항상 문장 맨 앞에 온다.', '부사만 필수적 부사어가 될 수 있다.', '빼도 문장의 뜻이 달라지지 않는다.'], '②', '성분 종류는 부속 성분.'),
        ('필수적 부사어를 요구하는 서술어가 <u>아닌</u> 것은?', None, ['같다', '주다', '삼다', '넣다', '달리다'], '⑤', "'달리다'는 주어만으로 성립."),
        ('밑줄 친 부분이 필수적 부사어인 것은?', None, ['<u>학교에서</u> 친구를 만났다.', '책을 <u>가방에</u> 넣었다.', '<u>아침에</u> 운동을 했다.', '<u>천천히</u> 걸어라.', '<u>매우</u> 춥다.'], '②', "'넣다'는 넣을 장소가 필요."),
        ('다음 문장의 문장 성분을 차례대로 쓰시오.', '형은 / 아빠와 / 닮았다.', None, '주어 - 부사어(필수적) - 서술어', ''),
        ('보어가 쓰인 문장과 필수적 부사어가 쓰인 문장을 각각 고르시오.', '(가) 물이 얼음이 되었다.　(나) 물이 얼음으로 되었다.', None, '보어: (가) / 필수적 부사어: (나)', "'이'는 보격 조사, '으로'는 부사격 조사."),
        ("밑줄 친 '생겼다'가 필수적 부사어를 요구하는 것은?", None, ['갑자기 문제가 <u>생겼다</u>.', '동네에 빵집이 <u>생겼다</u>.', '강아지가 귀엽게 <u>생겼다</u>.', '용돈이 <u>생겼다</u>.', '친구가 <u>생겼다</u>.'], '③', '생김새의 뜻일 때만.'),
        ("밑줄 친 '와/과'가 필수적 부사어를 만드는 것은?", None, ['<u>철수와</u> 영희는 학생이다.', '<u>사과와</u> 배를 샀다.', '이것은 <u>저것과</u> 같다.', '<u>빵과</u> 우유를 먹었다.', '<u>산과</u> 바다가 아름답다.'], '③', '나머지는 접속 조사.'),
        ('필수적 부사어와 위치 이동이 불가능한 부사어에 대한 설명으로 옳은 것은?', None, ['이동 불가 부사어는 모두 필수적 부사어이다.', '필수적 부사어는 모두 위치를 옮길 수 없다.', '두 개념은 서로 다른 기준으로 나눈 것이다.', "'안 들었다'의 '안'은 필수적 부사어이다.", '둘 다 주성분이다.'], '③', '필기: 포함 관계 X.'),
        ('필수적 부사어의 형식이 나머지와 <u>다른</u> 것은?', None, ['나는 <u>너와</u> 다르다.', '강아지가 <u>귀엽게</u> 생겼다.', '그를 <u>친구로</u> 여겼다.', '<u>동생에게</u> 책을 주었다.', '컵을 <u>식탁에</u> 놓았다.'], '②', '②는 용언 어간 + -게, 나머지는 체언 + 부사격 조사.'),
        ("'주다'가 요구하는 문장 성분을 모두 쓰시오.", None, None, '주어, 목적어, (필수적) 부사어', '누가 / 누구에게 / 무엇을 주다.'),
        ('필수적 부사어를 빠뜨려 어색해진 문장을 고르고 바르게 고치시오.', '(가) 나는 그를 스승으로 여긴다.　(나) 엄마가 용돈을 주셨다.<br>(다) 그 영화는 원작과 많이 다르다.　(라) 이 가방은 비슷하다.', None, '(라) → 이 가방은 내 가방과 비슷하다.', "'비슷하다'는 비교 대상(~와)이 필요. (나)는 문맥상 '나에게'가 생략된 자연스러운 문장으로 볼 수 있음."),
        ("'되다'가 쓰인 두 문장 '그는 의사가 되었다', '물이 얼음으로 되었다'에서 '의사가'와 '얼음으로'의 문장 성분을 각각 쓰고, 그렇게 판단한 근거를 쓰시오.", None, None, '의사가 = 보어 / 얼음으로 = 필수적 부사어', "'되다' 앞에 보격 조사 '가'가 붙으면 보어, 부사격 조사 '으로'가 붙으면 부사어. '얼음으로'는 빼면 '물이 되었다'로 어색하므로 필수적."),
        ("'두다'가 필수적 부사어를 요구하는 문장과 요구하지 않는 문장을 하나씩 만들어 쓰시오.", None, None, '예) 요구 O: 책을 책상에 두었다. / 요구 X: 친구와 바둑을 두었다.', "'놓다'의 뜻일 때만 장소 부사어가 필수."),
        ('다음 문장에서 필수적 부사어를 찾아 쓰시오.', '와, 할머니께서 손녀에게 예쁜 인형을 선물로 주셨다.', None, '손녀에게', "'선물로'는 빼도 '할머니께서 손녀에게 예쁜 인형을 주셨다'로 성립 → 수의적."),
        ("'철수와 영희는 닮았다'와 '철수는 영희와 닮았다'에서 '와'의 차이를 설명하시오.", None, None, '앞: 접속 조사(두 사람이 함께 주어) / 뒤: 부사격 조사(비교 대상 → 필수적 부사어)', ''),
        ('필수적 부사어가 쓰인 겹문장은?', None, ['비가 와서 길이 미끄럽다.', '내가 산 책은 이것과 같다.', '그는 키가 크다.', '하늘은 높고 바다는 넓다.', '나는 그가 온 것을 알았다.'], '②', "'이것과'가 '같다'의 필수적 부사어 + [내가 산] 관형절."),
        ('필수적 부사어에 대한 설명으로 적절하지 <u>않은</u> 것은?', None, ["'같다, 다르다'는 비교 대상을 부사어로 요구한다.", "'삼다, 여기다'는 '~(으)로'의 부사어를 요구한다.", '필수적 부사어가 빠지면 문장이 불완전해진다.', '필수적 부사어는 문장 성분 중 주성분에 속한다.', "'용언 어간 + -게' 형태로도 나타날 수 있다."], '④', '부속 성분.'),
        ('<보기>의 조건에 맞는 문장을 쓰시오.', '&lt;조건&gt; ① \'보내다\'를 서술어로 쓸 것 ② 필수적 부사어를 포함할 것 ③ 관형어를 한 개 이상 넣을 것', None, '예) 나는 멀리 사는 친구에게 긴 편지를 보냈다.', "필수적 부사어 '친구에게', 관형어 '멀리 사는', '긴'."),
    ]
    qs = []
    for i, (q, bx, ch, a, e) in enumerate(Q, 1):
        s = f'<div class="q"><span class="n">{i:02d}</span>{q}'
        if bx: s += f'<div class="bx">{bx}</div>'
        if ch: s += '<ul>' + ''.join(f'<li>{"①②③④⑤"[k]} {c}</li>' for k, c in enumerate(ch)) + '</ul>'
        else: s += '<div class="ln"></div><div class="ln"></div>'
        qs.append(s + '</div>')
    h.append('<section class="pb"><div class="head" style="padding:10px 16px"><div class="k">CHECK</div><h1 style="font-size:18pt">확인 문제 20</h1><p>01~05 기본 · 06~10 응용 · 11~15 발전 · 16~20 심화</p></div><div class="cols">' + ''.join(qs) + '</div></section>')
    h.append('<section class="pb"><div class="head" style="padding:10px 16px"><div class="k">ANSWER</div><h1 style="font-size:18pt">정답과 해설</h1></div><table class="ans"><tr><th>번호</th><th>정답</th><th>해설</th></tr>'
             + ''.join(f'<tr><td>{i:02d}</td><td>{a}</td><td>{e}</td></tr>' for i, (_, _, _, a, e) in enumerate(Q, 1)) + '</table></section>')
    return ''.join(h)


JS = """const { chromium } = require('playwright');
(async () => { const [h, o] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage();
 await p.goto('file://' + h, { waitUntil: 'load' }); await p.evaluate(() => document.fonts.ready);
 await p.pdf({ path: o, format: 'A4', printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true, headerTemplate: '<span></span>',
  footerTemplate: '<div style="width:100%;font-size:7.5px;color:#888;text-align:center">필수적 부사어 집중 노트 · <span class="pageNumber"></span></div>' });
 await b.close(); })();"""


def main():
    t = tempfile.mkdtemp()
    h = os.path.join(t, 'n.html'); open(h, 'w', encoding='utf-8').write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body()}</body></html>')
    js = os.path.join(t, 'r.js'); open(js, 'w').write(JS)
    root = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
    subprocess.run(['node', js, h, OUT], check=True, env={**os.environ, 'NODE_PATH': root})
    print(OUT)


if __name__ == '__main__':
    main()
