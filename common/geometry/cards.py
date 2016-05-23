
from common.color import RGBColor
from common.geometry.base import Geometry
from common.light import Lights, ID


EDGES = [
    "e_l", # edge left
    "e_r", # edge right
    "e_b", # edge bottom
]

ONE = EDGES

TWO = EDGES + [
    "t", # triangle
]

THREE = EDGES + [
    "t_l", # triangle left
    "t_r", # triangle right
    "t_b", # triangle bottom
]

HOUSES = {
    "1l": ONE,
    "1r": ONE,
    "2l": TWO,
    "2r": TWO,
    "3l": THREE,
    "3r": THREE,
}

HOUSES_KEYS = [
    "1l",
    "1r",
    "2l",
    "2r",
    "3l",
    "3r",
]

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
        return set(KEYS)

    def values(self):
        for k in KEYS:
            yield self[k]

    @property
    def ids(self):
        for h, c in KEYS:
            return self._lights[h][c]

    __iter__ = keys

    states = property(values)
