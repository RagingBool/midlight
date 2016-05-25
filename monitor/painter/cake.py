
from monitor.painter.base import Painter, P
from common.geometry.cake import TOP, BOT, N, NE, E, SE, S, SW, W, NW, NNE, \
    NEE, SEE, SSE, SSW, SWW, NWW, NNW, HOR, VER, CDL


NUM = (2**0.5)/(1+2**0.5)

OCTOGON = [
    P(1, NUM),
    P(NUM, 1),
    P(-NUM, 1),
    P(-1, NUM),
    P(-1, -NUM),
    P(-NUM, -1),
    P(NUM, -1),
    P(1, -NUM),
    P(1, NUM),
]

OCTOP1 = [P(0.05, 1) + p for p in OCTOGON[:8]]
OCTOM1 = [P(-0.05, -1) + p for p in OCTOGON[:8]]

VERTICALS_KEYS = [
    NEE,
    NNE,
    NNW,
    NWW,
    SWW,
    SSW,
    SSE,
    SEE,
]

VERTICALS = dict(zip(VERTICALS_KEYS, zip(OCTOGON, OCTOM1)))
VERTICALS2 = {k: [p*2 for p in v] for k,v in VERTICALS.items()}
CANDLES = dict(zip(VERTICALS_KEYS, zip(OCTOGON, OCTOP1)))
CANDLES2 = {k: [p*2 for p in v] for k,v in CANDLES.items()}

HORIZONTALS_KEYS = [
    NE,
    N,
    NW,
    W,
    SW,
    S,
    SE,
    E,
]

HORIZONTALS = dict(zip(HORIZONTALS_KEYS, zip(OCTOGON, OCTOGON[1:])))
HORIZONTALS2 = {k: [p*2 for p in v] for k,v in HORIZONTALS.items()}

LAYER = {
    HOR: HORIZONTALS,
    VER: VERTICALS,
    CDL: CANDLES,
}

LAYER2 = {
    HOR: HORIZONTALS2,
    VER: VERTICALS2,
    CDL: CANDLES2,
}

CAKE = {
    TOP: LAYER,
    BOT: LAYER2,
}


class CakePainter(Painter):

    def paint(self):
        for (layer, position, direction), color in self._geometry.items():
            self._canvas.itemconfig(self._stripes[layer, position, direction], fill=str(color))

    def _update_size(self, h, w):
        self._stripes = {}
        for (layer, position, direction), color in self._geometry.items():
            l = []
            for p in CAKE[layer][position][direction]:
                l.append(int(w/2 + (p.x * (w-6) / 4.2)))
                l.append(int(h/2 - (p.y * (h-6) / 8.4)))
            self._stripes[layer, position, direction] = self._canvas.create_line(
                *l,
                width=6,
                fill=str(color),
            )
