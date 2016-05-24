from common.geometry.matrix import MatrixGeometry
from common.geometry.cards import CardsGeometry, HOUSES, HOUSES_KEYS

GEOMETRIES = {
    "matrix0": MatrixGeometry([
        [(0, 0, x, y) for x in range(60)] \
        for y in range(30)
    ]),
    "cards1": CardsGeometry({
        h: {c: (0, 1, x, y) for y, c in enumerate(HOUSES[h]) \
        } for x, h in enumerate(HOUSES_KEYS)
    }),
}
