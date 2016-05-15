
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
        return self._height

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

    def items(self):
        for x in range(self.width):
            for y in range(self.height):
                yield (x, y), self._state[y][x]

    def keys(self):
        for x in range(self.width):
            for y in range(self.height):
                yield (x, y)

    def values(self):
        for k, v in self.items():
            yield v

    __iter__ = keys

    def __bytes__(self):
        b = bytearray()
        b += bytes(self.size)
        for (x, y), v in self.items():
            b += bytes((x,y))
            b += bytes(v)
        return bytes(b)

    @classmethod
    def parse(cls, buf):
        if not isinstance(buf, (bytes, bytearray)):
            raise TypeError("Bad type for buffer.")
        size = tuple(buf[:2])
        obj = cls(*size)
        for i in range(2, len(buf), 5):
            if len(buf) < i + 5:
                raise ValueError("Buffer with bad size: {}".format(buf))
            x, y = buf[i], buf[i+1]
            if x >= size[0] or y >= size[1]:
                raise ValueError("Bad index of light: {}".format(buf))
            obj[buf[i], buf[i+1]] = RGBColor.parse(buf[i+2:i+5])
        return obj
