"""중3 과학 중간고사 정리노트 생성기.

실행: python3 src/build.py  →  science-midterm-note/index.html
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import concept_iv, concept_v1, concept_v2, problems_iv, problems_v1, problems_v2, problems_new, appendix  # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), 'index.html')


def cover():
    return '''<section class="cover"><div>
<div class="kicker">3학년 과학 · 중간고사 대비</div>
<h1>과학 정리노트<span>자극과 반응 · 생식과 유전</span></h1>
<div class="scope"><div class="sc-iv"><b>Ⅳ-1 감각 기관</b><small>눈 · 귀 · 코 · 혀 · 피부</small></div>
<div class="sc-v1"><b>Ⅴ-1 생장과 생식</b><small>세포 분열 · 감수 분열 · 발생</small></div>
<div class="sc-v2"><b>Ⅴ-2 유전의 원리</b><small>멘델의 유전 원리</small></div></div>
<p><b>개념 정리 4단계</b>로 기초부터 고난도까지 올라갑니다.</p>
<div class="legend"><span class="b">기본 · 용어와 구조</span><span class="a">응용 · 과정과 상황 적용</span><span class="d">발전 · 탐구 해석과 비교</span><span class="s">심화 · 그래프·계산·함정</span></div>
<p class="small">문제 구성: 하이탑(학습 Check · 탐구 확인 · 개념 확인 · 실력 강화 · 서술형 · 최상위 · 실전) + 교과서(탐구 · 해 보기 · 스스로 확인 · 스스로 정리 · 최종 점검) 전 문항, 이어서 조건을 바꾼 변형 문제 52개. 각 단원 끝에 정답과 해설.</p>
</div>
<div class="toc"><h3 style="margin-bottom:6px">목차</h3><ol>
<li>Ⅳ-1 감각 기관 — 개념 정리 <small>기본·응용·발전·심화</small></li>
<li>Ⅳ-1 감각 기관 — 문제 정리 <small>하이탑 · 교과서 · 정답</small></li>
<li>Ⅴ-1 생장과 생식 — 개념 정리</li>
<li>Ⅴ-1 생장과 생식 — 문제 정리</li>
<li>Ⅴ-2 유전의 원리 — 개념 정리</li>
<li>Ⅴ-2 유전의 원리 — 문제 정리</li>
<li>변형 문제 52 <small>응용 · 발전 · 심화</small></li>
<li>부록 <small>1장 요약 · 비교표 · 서술형 템플릿 · 공식 · 계획표</small></li></ol>
<p class="small" style="margin-top:10px">범위: 자극과 반응 중 소단원 1(감각 기관), 생식과 유전 중 소단원 1(생장과 생식)·2(유전의 원리). 사람의 유전(가계도)은 범위에서 제외했습니다.<br>그림 출처: 하이탑 중학 과학 3, 중학교 과학 3 교과서 — 개인 학습용 정리.</p></div></section>'''


def part(cls, kicker, title, desc):
    return f'<header class="part {cls}"><div class="pk">{kicker}</div><h2>{title}</h2><p>{desc}</p></header>'


def main():
    body = [cover()]
    body.append(part('iv', 'Ⅳ. 자극과 반응 · 1', '감각 기관', '자극을 받아들이는 눈·귀·코·혀·피부의 구조와 기능'))
    body.append('<h2 class="sec">개념 정리 <small>기본 → 응용 → 발전 → 심화</small></h2>' + concept_iv.build())
    body.append(part('iv', 'Ⅳ-1 감각 기관', '문제 정리', '하이탑 전 문항 + 교과서 전 문항'))
    body.append(problems_iv.build())

    body.append(part('v1', 'Ⅴ. 생식과 유전 · 1', '생장과 생식', '세포 분열 · 체세포 분열 · 생식세포 분열 · 수정과 발생'))
    body.append('<h2 class="sec">개념 정리 <small>기본 → 응용 → 발전 → 심화</small></h2>' + concept_v1.build())
    body.append(part('v1', 'Ⅴ-1 생장과 생식', '문제 정리', '하이탑 전 문항 + 교과서 전 문항'))
    body.append(problems_v1.build())

    body.append(part('v2', 'Ⅴ. 생식과 유전 · 2', '유전의 원리', '멘델의 실험 · 우열의 원리 · 분리의 법칙 · 독립의 법칙'))
    body.append('<h2 class="sec">개념 정리 <small>기본 → 응용 → 발전 → 심화</small></h2>' + concept_v2.build())
    body.append(part('v2', 'Ⅴ-2 유전의 원리', '문제 정리', '하이탑 전 문항 + 교과서 전 문항'))
    body.append(problems_v2.build())

    body.append(part('nw', 'CHALLENGE', '변형 문제 52', '하이탑·교과서 문제의 조건·자료·질문을 바꿔 만든 응용 · 발전 · 심화 문제'))
    body.append('<div class="legend"><span class="a">응용</span><span class="d">발전</span><span class="s">심화</span></div>')
    body.append(problems_new.build())

    body.append(part('ap', 'APPENDIX', '부록', '시험 직전에 필요한 것들'))
    body.append(appendix.build())

    css = open(os.path.join(HERE, 'style.css'), encoding='utf-8').read()
    html = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>중3 과학 정리노트</title>
<style>{css}</style></head>
<body><main class="page">
{''.join(body)}
</main></body></html>'''
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(html)
    n = sum(len(m.bk.answers) for m in (problems_iv, problems_v1, problems_v2, problems_new))
    print(f'wrote {OUT} ({len(html) // 1024} KB), 문항 수 {n}')


if __name__ == '__main__':
    main()
