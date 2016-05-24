
from monitor.painter.base import Painter


class P(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iadd__(self, o):
        self.x += o.x
        self.y += o.y
        return self

    def __add__(self, o):
        n = P(self.x, self.y)
        n += o
        return n

    def __repr__(self):
        return "P({}, {})".format(self.x, self.y)

    def __imul__(self, m):
        self.x *= m
        self.y *= m
        return self

    def __mul__(self, m):
        n = P(self.x, self.y)
        n *= m
        return n

TRIANGLE = [P(0,0), P(0.5, (3**0.5)/2), P(1, 0), P(0,0)]
REV_TRIANGLE = [P(0,0), P(-0.5, (3**0.5)/2), P(0.5, (3**0.5)/2), P(0,0)]

EDGES = [
    "e_l", # edge left
    "e_r", # edge right
    "e_b", # edge bottom
]

ONE = dict(zip(EDGES, zip(TRIANGLE, TRIANGLE[1:])))

T2 = [p*2 for p in TRIANGLE]
TWO = dict(zip(EDGES, zip(T2, T2[1:])))
TWO["t"] = [P(1,0) + p for p in REV_TRIANGLE] # triangle

T3 = [p*3 for p in TRIANGLE]
THREE = dict(zip(EDGES, zip(T3, T3[1:])))
THREE.update(dict(zip([
    "t_l", # triangle left
    "t_t", # triangle top
    "t_r", # triangle right
], [[P(1,0)+p_1+p_2 for p_1 in REV_TRIANGLE] for p_2 in TRIANGLE[:3]])))

HOUSES = {
    "1l": {c: [p for p in ps] for (c, ps) in ONE.items()},
    "2l": {c: [P(1+1,0) + p for p in ps] for (c, ps) in TWO.items()},
    "3l": {c: [P(1+1+2+1,0) + p for p in ps] for (c, ps) in THREE.items()},
    "3r": {c: [P(1+1+2+1+3+1,0) + p for p in ps] for (c, ps) in THREE.items()},
    "2r": {c: [P(1+1+2+1+3+1+3+1,0) + p for p in ps] for (c, ps) in TWO.items()},
    "1r": {c: [P(1+1+2+1+3+1+3+1+2+1,0) + p for p in ps] for (c, ps) in ONE.items()},
}


class CardsPainter(Painter):

    def paint(self):
        for (h, card), color in self._geometry.items():
            self._canvas.itemconfig(self._stripes[h, card], fill=str(color))

    def _update_size(self, h, w):
        self._stripes = {}
        for (house, card), color in self._geometry.items():
            l = []
            for p in HOUSES[house][card]:
                l.append(int(p.x * ((w/(1+1+2+1+3+1+3+1+2+1+1))-6)) + 3)
                l.append(int(h - (p.y * ((h/3)-6))) - 3)
            self._stripes[house, card] = self._canvas.create_line(
                *l,
                width=6,
                fill=str(color),
            )
