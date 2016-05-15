
import re


class LightState(object):
    """
    Class for represnting a possible state of a light, usually a color.
    
    Must be (de-)serializable.
    """
    def __bytes__(self):
        raise NotImplementedError()

    @classmethod
    def parse(cls, buf):
        raise NotImplementedError()


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
                if not isinstance(kwargs[c], float):
                    raise TypeError("RGB channels should be ints")
                if not (0 <= kwargs[c] <= 1):
                    raise ValueError("RGB channels should be in range [0,1]")
        elif "html" in kwargs:
            m = re.fullmatch(
                "#?([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})",
                kwargs["html"]
            )
            if m is None:
                raise ValueError("Invalid HTML RGB format")
            self._r, self._g, self._b = (b2f(int(x, 16)) for x in m.groups())
        else:
            self._r, self._g, self._b = 0, 0, 0

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, r):
        self._r = r

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, g):
        self._g = g

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, b):
        self._b = b

    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b

    @property
    def value(self):
        return tuple(self)

    def __str__(self):
        return "#{}".format(bytes(self).hex())

    def __bytes__(self):
        return bytes([f2b(self.r), f2b(self.g), f2b(self.b)])

    @classmethod
    def parse(cls, buf):
        if not isinstance(buf, (bytes, bytearray)):
            raise TypeError("Bad type for buffer.")
        return cls(r=buf[0], g=buf[1], b=buf[2])


def b2f(b):
    """
    Convert a byte (int in [0,255]) to a float (in [0,1]).
    """
    return b / 255


def f2b(b):
    """
    Convert a float (in [0,1]) to a byte (int in [0,255]).
    """
    return min(255, int(f * 256))
