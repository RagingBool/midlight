from common.geometry.matrix import MatrixGeometry

GEOMETRIES = {
    "matrix0": MatrixGeometry([
        [(0, 0, x, y) for x in range(60)] \
        for y in range(30)
    ]),
}
