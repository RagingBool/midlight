
from monitor.painter.base import Painter, P
from common.geometry.cards import E_L, E_R, E_B, T, T_L, T_T, T_R, L_1, R_1, \
    L_2, R_2, L_3, R_3


TRIANGLE = [P(0,0), P(0.5, (3**0.5)/2), P(1, 0), P(0,0)]
REV_TRIANGLE = [P(0,0), P(-0.5, (3**0.5)/2), P(0.5, (3**0.5)/2), P(0,0)]

EDGES = [
    E_L,  # edge left
    E_R,  # edge right
    E_B,  # edge bottom
]

ONE = dict(zip(EDGES, zip(TRIANGLE, TRIANGLE[1:])))

T2 = [p*2 for p in TRIANGLE]
TWO = dict(zip(EDGES, zip(T2, T2[1:])))
TWO[T] = [P(1,0) + p for p in REV_TRIANGLE]  # triangle

T3 = [p*3 for p in TRIANGLE]
THREE = dict(zip(EDGES, zip(T3, T3[1:])))
THREE.update(dict(zip([
    T_L,  # triangle left
    T_T,  # triangle top
    T_R,  # triangle right
], [[P(1,0)+p_1+p_2 for p_1 in REV_TRIANGLE] for p_2 in TRIANGLE[:3]])))

HOUSES = {
    L_1: {c: [p for p in ps] for (c, ps) in ONE.items()},
    L_2: {c: [P(1+1,0) + p for p in ps] for (c, ps) in TWO.items()},
    L_3: {c: [P(1+1+2+1,0) + p for p in ps] for (c, ps) in THREE.items()},
    R_3: {c: [P(1+1+2+1+3+1,0) + p for p in ps] for (c, ps) in THREE.items()},
    R_2: {c: [P(1+1+2+1+3+1+3+1,0) + p for p in ps] for (c, ps) in TWO.items()},
    R_1: {c: [P(1+1+2+1+3+1+3+1+2+1,0) + p for p in ps] for (c, ps) in ONE.items()},
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
