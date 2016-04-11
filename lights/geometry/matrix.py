
from lights.light import RGBLight
from lights.light_state import RGBColor
from lights.geometry.base import Geometry, GeometryState


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


class MatrixGeometry(Geometry):

    STATE_CLS = MatrixGeometryState
    
    def __init__(self, two_d_l):
        self._height = len(two_d_l)
        if self._height == 0:
            raise ValueError("No empty matrix.")
        self._width = len(two_d_l[0])
        for row in two_d_l:
            if self._width != len(row):
                raise ValueError("Rows are not of identical length.")
            for light in row:
                if not isinstance(light, RGBLight):
                    raise TypeError("All elements in collection should be " \
                        "Light objects")
        self._lights = two_d_l

    def _get_state(self):
        mgs = MatrixGeometryState(self._width, self._height)
        for x in range(self._width):
            for y in range(self._height):
                mgs[x, y] = self._lights[y][x].state
        return mgs

    def _set_state(self, geo_state):
        for x in range(self._width):
            for y in range(self._height):
                self._lights[y][x].state = geo_state[x, y] 
