from common.geometry.matrix import MatrixGeometry
from common.geometry.cards import CardsGeometry, HOUSES, HOUSES_KEYS
from common.geometry.cake import CakeGeometry, CAKE, CAKE_KEYS, \
    CAKE_LAYER_KEYS

GEOMETRIES = {
    "matrix0": MatrixGeometry([
        [(0, 0, x, y) for x in range(60)] \
        for y in range(30)
    ]),
    "cards1": CardsGeometry({
        h: {c: (0, 1, x, y) for y, c in enumerate(HOUSES[h]) \
        } for x, h in enumerate(HOUSES_KEYS)
    }),
    "cake2": CakeGeometry({
        l: {p: {d: (0, 2, x<<7 | y, z) for z, d in enumerate(CAKE[l][p]) \
        } for y, p in enumerate(CAKE_LAYER_KEYS[l]) \
        } for x, l in enumerate(CAKE_KEYS)
    }),
}
