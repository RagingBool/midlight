
from common.color import RGBColor
from common.geometry.base import Geometry
from common.light import Lights, ID


ES = "ES" # edges
T = "T"  # triangle
T_L = "T_L"  # triangle left
T_T = "T_T"  # triangle top
T_R = "T_R"  # triangle right
L_1 = "L_1"  # left house of 1
R_1 = "R_1"  # right house of 1
L_2 = "L_2"  # left house of 2
R_2 = "R_2"  # right house of 2
L_3 = "L_3"  # left house of 3
R_3 = "R_3"  # right house of 3



ONE = [
    ES,  # edges
]

TWO = [
    ES,  # edges
    T,  # triangle
]

THREE = [
    ES,  # edges
    T_L,  # triangle left
    T_R,  # triangle right
    T_T,  # triangle top
]

HOUSES_KEYS = [
    L_1,
    L_2,
    L_3,
    R_3,
    R_2,
    R_1,
]

HOUSES = {
    L_1: ONE,
    R_1: ONE,
    L_2: TWO,
    R_2: TWO,
    L_3: THREE,
    R_3: THREE,
}

KEYS = set()
for h, c_l in HOUSES.items():
    for c in c_l:
        KEYS.add((h, c))
del h, c, c_l


class CardsGeometry(Geometry):

    def __init__(self, light_ids):
        self._lights = {}
        for h, c_l in HOUSES.items():
            s_ids = light_ids.pop(h)
            self._lights[h] = {}
            for c in c_l:
                id = ID(s_ids.pop(c))
                self._lights[h][c] = id
                Lights(id, RGBColor)
            if s_ids:
                raise ValueError("Extraneous cards in house {}.".format(h))
        if light_ids:
            raise ValueError("Extraneous houses.")

    def __getitem__(self, hc):
        h, c = hc
        return Lights[self._lights[h][c]]

    def __setitem__(self, hc, state):
        h, c = hc
        Lights[self._lights[h][c]] = state

    def items(self):
        for k in KEYS:
            yield k, self[k]

    def keys(self):
        return iter(KEYS)

    def values(self):
        for k in KEYS:
            yield self[k]

    @property
    def ids(self):
        for h, c in KEYS:
            yield self._lights[h][c]

    __iter__ = keys

    states = property(values)
