
from lights.light import RGBLight
from lights.geometry.base import Geometry
from common.lights.matrix import MatrixGeometryState


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
