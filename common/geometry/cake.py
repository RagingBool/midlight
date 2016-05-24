
from common.color import RGBColor
from common.geometry.base import Geometry
from common.light import Lights, ID

TOP = "TOP"  # top layer
BOT = "BOT"  # bottom layer
N = "N"
NE = "NE"
E = "E"
SE = "SE"
S = "S"
SW = "SW"
W = "W"
NW = "NW"
NNE = "NNE"
NEE = "NEE"
SEE = "SEE"
SSE = "SSE"
SSW = "SSW"
SWW = "SWW"
NWW = "NWW"
NNW = "NNW"
HOR = "HOR"  # horizontal bars
VER = "VER"  # vertical bars
CDL = "CDL"  # candles


VERTICALS = [
    NNE,
    NEE,
    SEE,
    SSE,
    SSW,
    SWW,
    NWW,
    NNW,
]

HORIZONTALS = [
    N,
    NE,
    E,
    SE,
    S,
    SW,
    W,
    NW,
]

LAYER_KEYS = [
    VER,
    HOR,
    CDL,
]

CAKE_LAYER_KEYS = {
    BOT: LAYER_KEYS,
    TOP: LAYER_KEYS,
}

LAYER = {
    VER: VERTICALS,
    HOR: HORIZONTALS,
    CDL: VERTICALS,
}

CAKE_KEYS = [
    BOT,
    TOP,
]

CAKE = {
    BOT: LAYER,
    TOP: LAYER,
}

KEYS = set()
for l, l_l in CAKE.items():
    for p, p_l in l_l.items():
        for d in p_l:
            KEYS.add((l, p, d))
del l, p, d, l_l, p_l


class CakeGeometry(Geometry):

    def __init__(self, light_ids):
        self._lights = {}
        for l, l_l in CAKE.items():
            l_ids = light_ids.pop(l)
            self._lights[l] = {}
            for p, p_l in l_l.items():
                p_ids = l_ids.pop(p)
                self._lights[l][p] = {}
                for d in p_l:
                    id = ID(p_ids.pop(d))
                    self._lights[l][p][d] = id
                    Lights(id, RGBColor)
                if p_ids:
                    raise ValueError("Extraneous direction in layer {}, part {}".format(l, p))
            if l_ids:
                raise ValueError("Extraneous part in layer {}.".format(l))
        if light_ids:
            raise ValueError("Extraneous layer.")

    def __getitem__(self, lpd):
        l, p, d = lpd
        return Lights[self._lights[l][p][d]]

    def __setitem__(self, lpd, state):
        l, p, d = lpd
        Lights[self._lights[l][p][d]] = state

    def items(self):
        for k in KEYS:
            yield k, self[k]

    def keys(self):
        return set(KEYS)

    def values(self):
        for k in KEYS:
            yield self[k]

    @property
    def ids(self):
        for h, c in KEYS:
            yield self._lights[l][p][d]

    __iter__ = keys

    states = property(values)
