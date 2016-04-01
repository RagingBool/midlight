
import re


class LightState(object):
    """
    Class for represnting a possible state of a light, usually a color.
    """
    pass


class RGBColor(LightState):
    """
    Class for represnting an RGB color of a light.
    """
    def __init__(self, **kwargs):
        if "r" in kwargs and "g" in kwargs and "b" in kwargs:
            self._r = kwargs["r"]
            self._g = kwargs["g"]
            self._b = kwargs["b"]
            for c in ["r", "g", "b"]:
                if not isinstance(kwargs[c], int):
                    raise TypeError("RGB channels should be ints")
                if not (0 <= kwargs[c] <= 255):
                    raise ValueError("RGB channels should be in range [0,255]")
        elif "html" in kwargs:
            m = re.fullmatch(
                "#?([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})",
                kwargs["html"]
            )
            if m is None:
                raise ValueError("Invalid HTML RGB format")
            self._r, self._g, self._b = (int(x, 16) for x in m.groups())

    @property
    def r(self):
        return self._r

    @property
    def g(self):
        return self._g

    @property
    def b(self):
        return self._b

    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b

    @property
    def value(self):
        return tuple(self)

    def __str__(self):
        return "#{:02X}{:02X}{:02X}".format(*self.value)
