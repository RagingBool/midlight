
from common.lights.light_state import RGBColor
from common.lights.geometry import GeometryState


class MatrixGeometryState(GeometryState):

    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._state = [[None]*width for i in range(height)]

    @property
    def size(self):
        return self.width, self.height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._width

    def __getitem__(self, xy):
        if not isinstance(xy, tuple) or not len(xy) == 2:
            raise TypeError("Can only be accessed with 2d coordinates.")
        x, y = xy
        if x >= self._width or y >= self._height:
            raise IndexError("Out of bounds")
        return self._state[y][x]

    def __setitem__(self, xy, state):
        if not isinstance(xy, tuple) or not len(xy) == 2:
            raise TypeError("Can only be accessed with 2d coordinates.")
        if not isinstance(state, RGBColor):
            raise TypeError("Can only be set to a RGBColor.")
        x, y = xy
        if x >= self._width or y >= self._height:
            raise IndexError("Out of bounds")
        self._state[y][x] = state

    def __iter__(self):
        for x in range(self.width):
            for y in range(self.height):
                yield self._state[y][x]


