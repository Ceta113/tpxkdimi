"""문항 표현용 도구."""
C = '①②③④⑤'
BOGI = 'ㄱㄴㄷㄹㅁ'
COMBO = ['ㄱ', 'ㄴ', 'ㄱ, ㄴ', 'ㄴ, ㄷ', 'ㄱ, ㄴ, ㄷ']
COMBO2 = ['ㄱ, ㄴ', 'ㄱ, ㄷ', 'ㄴ, ㄷ', 'ㄴ, ㄹ', 'ㄷ, ㄹ']
COMBO3 = ['ㄱ', 'ㄷ', 'ㄱ, ㄴ', 'ㄱ, ㄷ', 'ㄴ, ㄷ']


class Stage:
    def __init__(self, key, name, title, desc):
        self.key, self.name, self.title, self.desc = key, name, title, desc
        self.items = []  # ('grp', area, header, passage) | ('q', dict)

    def grp(self, area, header, passage=''):
        self.items.append(('grp', area, header, passage))

    def _add(self, area, d):
        d['area'] = area
        self.items.append(('q', d))

    def mc(self, area, q, ch, a, e, box=None, tag=''):
        self._add(area, dict(kind='mc', q=q, ch=ch, a=a, e=e, box=box, tag=tag))

    def bg(self, area, q, items, a, e, combo=COMBO, tag=''):
        box = '<br>'.join(f'{BOGI[i]}. {t}' for i, t in enumerate(items))
        self._add(area, dict(kind='mc', q=q, ch=combo, a=a, e=e, box=box, bogi=True, tag=tag))

    def sa(self, area, q, a, e='', box=None, lines=1, tag=''):
        self._add(area, dict(kind='sa', q=q, a=a, e=e, box=box, lines=lines, tag=tag))

    def count(self):
        return sum(1 for it in self.items if it[0] == 'q')
