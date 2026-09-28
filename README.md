# tpxkdimi
디미고 입시용 실적물

## science-midterm-note — 중3 과학 중간고사 정리노트
- `과학정리노트_중간고사.pdf` : 인쇄용 완성본 (A4, 77쪽)
- `index.html` : 브라우저로 보는 버전 (`img/` 폴더 필요)
- 범위: Ⅳ-1 감각 기관, Ⅴ-1 생장과 생식, Ⅴ-2 유전의 원리
- 구성: 개념 정리 4단계(기본·응용·발전·심화) → 하이탑·교과서 전 문항 → 변형 문제 52개 → 정답과 해설 → 부록
- 다시 만들기: `python3 science-midterm-note/src/build.py`

## korean-midterm-note — 중3 국어 정리노트 (필기 보충판)
- `국어정리노트_필기보충판.pdf` : 기존 39쪽 정리노트에 손글씨 필기 내용을 반영한 보충 페이지 10쪽을 끼워 넣은 49쪽 완성본
- 다시 만들기: `python3 korean-midterm-note/src/build.py <원본노트.pdf> <출력.pdf>`

## korean-workbook-222 — 국어 기출 222 (4단계 문제집)
- `국어기출222_문제집.pdf` : 표지 · 구성/채점표 · STEP 1~4 (222문항) · 빠른 정답 · 해설 · 뒤표지 (34쪽)
- 문항 데이터: `src/s1.py`~`s4.py` · 다시 만들기: `python3 korean-workbook-222/src/build.py`
