"""세트형 지문 조립: 본문(private/fulltext.py)에 (가)(나)… 구분과 ㉠ 표시를 붙인다."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'private'))
try:
    import fulltext as T
except ImportError:  # 전문 파일이 없으면(저장소 공개본) 빌드 중단
    raise SystemExit('private/fulltext.py 가 필요합니다 (학습지 본문 — 저작권 때문에 저장소에 올리지 않음).')


def _mark(text, marks):
    for phrase, m in marks.items():
        assert phrase in text, phrase
        text = text.replace(phrase, f'<span class="mk">{m}</span><u>{phrase}</u>', 1)
    return text


def poem(label, lines, au, marks=None, note=''):
    marks = marks or {}
    used = set()
    out = []
    for ln in lines:
        if not ln:
            out.append('<div class="sgap"></div>'); continue
        for phrase, m in marks.items():
            if phrase in ln and phrase not in used:
                ln = ln.replace(phrase, f'<span class="mk">{m}</span><u>{phrase}</u>', 1); used.add(phrase)
        out.append(f'<div>{ln}</div>')
    missing = set(marks) - used
    assert not missing, missing
    n = f'<div class="pnote">{note}</div>' if note else ''
    return f'<div class="sec"><span class="lb">{label}</span><div class="poem">{"".join(out)}</div><div class="au2">{au}</div>{n}</div>'


def prose(label, paras, marks=None, au=''):
    marks = marks or {}
    body = ''.join(f'<p>{p}</p>' for p in paras)
    body = _mark(body, marks)
    a = f'<div class="au2">{au}</div>' if au else ''
    return f'<div class="sec"><span class="lb">{label}</span><div class="prose">{body}</div>{a}</div>'
