
from lights.light import RGBLight

class LightManager(object):
    """
    Base class for light managers. A light manager controls a collection of
    many light which have some physical affiliation (i.e. part of the same
    large object), and therefore should be managed together. The manager is
    responsible for generating meaningful images using their lights.
    """

    def render(self, input_state):
        """
        Render light states to all lights controlled by this manager, according
        to the given input_state.
        """
        raise NotImplementedError()


def rot_col(rgb, add):
    d = {c: getattr(rgb, c) for c in ("r", "g", "b")}
    while add > 0:
        for cs in [
                ("r", "b", "g"),
                ("g", "r", "b"),
                ("b", "g", "r"),
            ]:
            vs = list(d[c] for c in cs)
            if vs[0] == 0 and vs[1] == 255 and vs[2] != 255:
                sadd = min(add, 255 - vs[2])
                add -= sadd
                vs[2] += sadd
                break
            elif vs[0] == 0 and vs[2] == 255 and vs[1] != 0:
                sadd = min(add, vs[1])
                add -= sadd
                vs[1] -= add
                break
        d = dict(zip(cs, vs))
    return RGBLight(**d)


class BasicRainbowManager(LightManager):
    """
    A light manager which rotates all of its RGB-lights around the fully
    saturated color space.
    """
    def __init__(self, freq, lights):
        if not isinstance(freq, (int, float)):
            raise TypeError("Freq should be numeric.")
        lights = list(lights)
        for light in lights:
            if not isinstance(light, RGBLight):
                raise TypeError("All elements in collection should be Light " \
                    "objects")
        self._freq = freq
        self._lights = lights
        for i, light in enumerate(self._lights):
            light.state = rot_col(RGBColor(html="ff0000"), i*23)
        self._offset = 0.0

    def render(self, input_state):
        add = (6*255)*input_state[DELTA]*self._freq + self._offset
        self._offset = add % 1
        add = int(add)
        for light in self._lights:
            light.state = rot_col(light.state, add)
