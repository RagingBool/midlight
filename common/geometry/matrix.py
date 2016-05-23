
from common.color import RGBColor
from common.geometry.base import Geometry
from common.light import Lights, ID


class MatrixGeometry(Geometry):

    def __init__(self, two_d_l):
        self._height = len(two_d_l)
        if self._height == 0:
            raise ValueError("No empty matrix.")
        self._width = len(two_d_l[0])
        self._lights = [[None] * self._width for i in range(self._height)]
        for y, row in enumerate(two_d_l):
            if self._width != len(row):
                raise ValueError("Rows are not of identical length.")
            for x, light in enumerate(row):
                id = ID(light)
                self._lights[y][x] = id
                Lights(id, RGBColor)

    @property
    def size(self):
        return self.width, self.height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def __getitem__(self, xy):
        if not isinstance(xy, tuple) or not len(xy) == 2:
            raise TypeError("Can only be accessed with 2d coordinates.")
        x, y = xy
        if x >= self._width or y >= self._height:
            raise IndexError("Out of bounds")
        return Lights[self._lights[y][x]]

    def __setitem__(self, xy, state):
        if not isinstance(xy, tuple) or not len(xy) == 2:
            raise TypeError("Can only be accessed with 2d coordinates.")
        if not isinstance(state, RGBColor):
            raise TypeError("Can only be set to a RGBColor.")
        x, y = xy
        if x >= self._width or y >= self._height:
            raise IndexError("Out of bounds")
        Lights[self._lights[y][x]] = state

    def items(self):
        for x in range(self.width):
            for y in range(self.height):
                yield (x, y), self[x, y]

    def keys(self):
        for x in range(self.width):
            for y in range(self.height):
                yield (x, y)

    def values(self):
        for k, v in self.items():
            yield v

    @property
    def ids(self):
        for x in range(self._width):
            for y in range(self._height):
                yield self._lights[y][x]

    states = property(values)

    __iter__ = keys
