from common.geometry.matrix import MatrixGeometry
from common.geometry.cards import CardsGeometry, HOUSES, HOUSES_KEYS

GEOMETRIES = {
    "matrix0": MatrixGeometry([
        [(0, 0, x, y) for x in range(60)] \
        for y in range(30)
    ]),
    "cards0": CardsGeometry({
        h: {c: (0, 0, x, y) for x, c in enumerate(HOUSES[h])} \
        for y, h in enumerate(HOUSES_KEYS)
    }),
}