"""노트 생성용 공통 도구: 문제 카드 렌더링, 정답 수집, 섹션 머리글."""
import html as _h

CIRC = '①②③④⑤⑥⑦⑧'
BOGI = 'ㄱㄴㄷㄹㅁㅂ'


class Book:
    """한 단원의 문제와 정답을 모아 두는 상자."""

    def __init__(self, key):
        self.key = key
        self.answers = []  # (group, label, answer, explanation)
        self.group = ''

    def set_group(self, g):
        self.group = g

    def add(self, label, ans, exp):
        self.answers.append((self.group, label, ans, exp))


def img(name, w=None, cap=None, cls='fig'):
    style = f' style="width:{w}"' if w else ''
    c = f'<figcaption>{cap}</figcaption>' if cap else ''
    return f'<figure class="{cls}"><img src="img/{name}.jpg"{style} alt="{cap or name}">{c}</figure>'


def P(book, label, q, fig=None, box=None, ch=None, ans='', exp='', tag='', lines=0,
      figw=None, extra='', cols=None):
    """문제 카드 한 개를 HTML로 만들고 정답을 book에 등록한다."""
    out = ['<div class="prob">']
    t = f'<span class="tag">{tag}</span>' if tag else ''
    out.append(f'<div class="q"><span class="num">{label}</span>{t}{q}</div>')
    if fig:
        figs = fig if isinstance(fig, list) else [fig]
        inner = ''.join(f if f.lstrip().startswith('<') else
                        f'<img src="img/{f}.jpg" alt="{f}"' + (f' style="width:{figw}"' if figw else '') + '>'
                        for f in figs)
        out.append(f'<div class="pfig">{inner}</div>')
    if extra:
        out.append(extra)
    if box:
        items = ''.join(f'<li><b>{BOGI[i]}.</b> {b}</li>' for i, b in enumerate(box))
        out.append(f'<div class="bogi"><span class="bogi-t">보기</span><ul>{items}</ul></div>')
    if ch:
        n = cols or (5 if max(len(_strip(c)) for c in ch) <= 9 else
                     (3 if max(len(_strip(c)) for c in ch) <= 16 else 1))
        items = ''.join(f'<li>{CIRC[i]} {c}</li>' for i, c in enumerate(ch))
        out.append(f'<ol class="ch c{n}">{items}</ol>')
    if lines:
        out.append('<div class="lines">' + '<div></div>' * lines + '</div>')
    out.append('</div>')
    book.add(label, ans, exp)
    return '\n'.join(out)


def _strip(s):
    import re
    return re.sub('<[^>]+>', '', s)


def fill(book, label, text, ans):
    """빈칸 문제: text 안의 ___ 를 밑줄 칸으로 바꾼다."""
    t = text.replace('___', '<span class="blank"></span>')
    book.add(label, ans, '')
    return f'<li><span class="num s">{label}</span> {t}</li>'


def answer_key(book, title='정답과 해설'):
    rows = []
    cur = None
    for g, label, a, e in book.answers:
        if g != cur:
            rows.append(f'<tr class="grp"><td colspan="3">{g}</td></tr>')
            cur = g
        rows.append(f'<tr><td class="al">{label}</td><td class="aa">{a}</td><td class="ae">{e}</td></tr>')
    return (f'<section class="akey"><h3 class="akey-h">{title}</h3>'
            f'<table class="ak"><thead><tr><th>번호</th><th>정답</th><th>해설 · 포인트</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></section>')


def level(kind, title, body):
    names = {'b': ('기본', 'lv-b'), 'a': ('응용', 'lv-a'), 'd': ('발전', 'lv-d'), 's': ('심화', 'lv-s')}
    n, c = names[kind]
    return (f'<section class="level {c}"><div class="lv-head"><span class="lv-badge">{n}</span>'
            f'<h3>{title}</h3></div><div class="lv-body">{body}</div></section>')


def box(kind, title, body):
    return f'<div class="box {kind}"><div class="box-t">{title}</div><div class="box-b">{body}</div></div>'


def esc(s):
    return _h.escape(s)
