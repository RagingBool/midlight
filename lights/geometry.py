
from lights.light import RGBLight

class Geometry(object):
    """
    Base class for geometries of light collections. A Geometry object should:
    Construct with a collection of light objects;
    Have setters and getters which alter the light-state of these lights;
    Have an iterator which yields all lights, so their state can pass through
    some geometry-agnostic filter.
    """
    pass


class MatrixGeometry(Geometry):
    
    def __init__(self, two_d_l):
        self._height = len(two_d_l)
        if self.__height == 0:
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

    def __getitem__(self, xy):
        if not isinstance(xy, tuple) or not len(xy) == 2:
            raise TypeError("Can only be accessed with 2d coordinates.")
        x, y = xy
        if x >= self._width or y >= self._heigth:
            raise IndexError("Out of bounds")
        return self._lights[x][y].state

    def __setitem__(self, xy, state):
        if not isinstance(xy, tuple) or not len(xy) == 2:
            raise TypeError("Can only be accessed with 2d coordinates.")
        x, y = xy
        if x >= self._width or y >= self._heigth:
            raise IndexError("Out of bounds")
        self._lights[x][y].state = state

    @property
    def size(self):
        return self.width, self.height

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._width

    def __iter__(self):
        for x in range(self.width):
            for y in range(self.height)
                yield self._lights[x][y]
