
import re
import math


THIRD = 1.0 / 3.0
TWO_THIRDS = 2.0 / 3.0
PI_DIV_3 = THIRD * math.pi
TAU = math.pi * 2


def clip(x, a=0, b=1):
    return min(max(x, a), b)


def interpolate(a, b, x):
    return a + (b - a) * x


def assert_channel(c, name="", include_1=True):
    if not isinstance(c, (float, int)):
        raise TypeError("{} channel should be numeric.".format(name))
    if not (0 <= c < 1) and not (include_1 and c == 1):
        raise ValueError("{} channel should be in range [0,1{} instead of {}".format(
            name, "]" if include_1 else ")", c))
    return float(c)


class LightState(object):
    """
    Class for represnting a possible state of a light, usually a color.
    
    Must be (de-)serializable.
    """
    def __bytes__(self):
        """
        Must return a buffer 4 bytes long.
        """
        raise NotImplementedError()

    @classmethod
    def parse(cls, buf):
        o = cls()
        o.iparse(buf)
        return o

    def iparse(self, buf):
        """
        Buffer should be 4 bytes long, but cannot be counted on.
        """
        raise NotImplementedError()


class RGBColor(LightState):
    """
    Class for represnting an RGB color of a light.
    """
    def __init__(self, **kwargs):
        self._r = None
        self._g = None
        self._b = None
        self._h = None
        self._s = None
        self._i = None
        if "r" in kwargs and "g" in kwargs and "b" in kwargs:
            self._rgb = True
            for c in "rgb":
                setattr(self, c, kwargs[c])
        elif "h" in kwargs and "s" in kwargs and "i" in kwargs:
            self._rgb = False
            for c in "hsi":
                setattr(self, c, kwargs[c])
        elif "html" in kwargs:
            m = re.fullmatch(
                "#?([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})",
                kwargs["html"]
            )
            if m is None:
                raise ValueError("Invalid HTML RGB format")
            self._rgb = True
            self._r, self._g, self._b = (b2f(int(x, 16)) for x in m.groups())
        elif kwargs != {}:
            raise ValueError("Bad kwargs for function.")
        else:
            self._rgb = True
            self._r, self._g, self._b = 0.0, 0.0, 0.0

    def _assert_rgb(self):
        if not self._rgb:
            self._r, self._g, self._b = hsi_to_rgb(self._h, self._s, self._i)
            self._rgb = True

    def _assert_hsi(self):
        if self._rgb:
            self._h, self._s, self._i = rgb_to_hsi(self._r, self._g, self._b)
            self._rgb = False

    @property
    def r(self):
        self._assert_rgb()
        return self._r

    @r.setter
    def r(self, r):
        self._assert_rgb()
        self._r = assert_channel(r, name="R")

    @property
    def g(self):
        self._assert_rgb()
        return self._g

    @g.setter
    def g(self, g):
        self._assert_rgb()
        self._g = assert_channel(g, name="G")

    @property
    def b(self):
        self._assert_rgb()
        return self._b

    @b.setter
    def b(self, b):
        self._assert_rgb()
        self._b = assert_channel(b, name="B")

    @property
    def h(self):
        self._assert_hsi()
        return self._h

    @h.setter
    def h(self, h):
        self._assert_hsi()
        self._h = assert_channel(h, name="H", include_1=False)

    @property
    def s(self):
        self._assert_hsi()
        return self._s

    @s.setter
    def s(self, s):
        self._assert_hsi()
        self._s = assert_channel(s, name="S")

    @property
    def i(self):
        self._assert_hsi()
        return self._i

    @i.setter
    def i(self, i):
        self._assert_hsi()
        self._i = assert_channel(i, name="I")

    def __iter__(self):
        yield self.r
        yield self.g
        yield self.b

    def __str__(self):
        return "#{}".format(bytes(self)[:3].hex())

    def __bytes__(self):
        return bytes([f2b(self.r), f2b(self.g), f2b(self.b), 0])

    def iparse(self, buf):
        if not isinstance(buf, (bytes, bytearray)):
            raise TypeError("Bad type for buffer.")
        self.r = b2f(buf[0])
        self.g = b2f(buf[1])
        self.b = b2f(buf[2])


def b2f(b):
    """
    Convert a byte (int in [0,255]) to a float (in [0,1]).
    """
    return b / 255


def f2b(f):
    """
    Convert a float (in [0,1]) to a byte (int in [0,255]).
    """
    return min(255, int(f * 256))

# Based on a post by Brian Neltner: http://blog.saikoled.com/post/43693602826/why-every-led-light-should-be-using-hsi
def hsi_to_rgb(hue, saturation, intensity):
    nh = hue % 1
    cs = clip(saturation)
    ci = clip(intensity)

    if nh < THIRD:
        rad = TAU * nh
        r = math.cos(rad) / math.cos(PI_DIV_3 - rad)
        c1 = ci * (1 + cs * r)
        c2 = ci * (1 + cs * (1 - r))
        c3 = ci * (1 - cs)
    elif nh < TWO_THIRDS:
        rad = TAU * (nh - THIRD)
        r = math.cos(rad) / math.cos(PI_DIV_3 - rad)
        c2 = ci * (1 + cs * r)
        c3 = ci * (1 + cs * (1 - r))
        c1 = ci * (1 - cs)
    else:
        rad = TAU * (nh - TWO_THIRDS)
        r = math.cos(rad) / math.cos(PI_DIV_3 - rad)
        c3 = ci * (1 + cs * r)
        c1 = ci * (1 + cs * (1 - r))
        c2 = ci * (1 - cs)
    
    # This is to avoid clipping of colour channels with too high intensity.
    m = max(c1, c2, c3, 1)

    return c1 / m, c2 / m, c3 / m


def rgb_to_hsi(c1, c2, c3):
    cc1 = clip(c1)
    cc2 = clip(c2)
    cc3 = clip(c3)

    minc = min(cc1, cc2, cc3)
    maxc = max(cc1, cc2, cc3)

    if minc != maxc:
        nr = cc1 / maxc
        ng = cc2 / maxc
        nb = cc3 / maxc

        hue_norm_acos = math.acos(
            (0.5 * (2 * nr - ng - nb)) /
            math.sqrt((nr - ng) * (nr - ng) + (nr - nb) * (ng - nb))) / TAU

        hue = hue_norm_acos if (nb <= ng) else 1 - hue_norm_acos

        intensity = (cc1 + cc2 + cc3) / 3
        saturation = 1 - minc / intensity
    else:
        hue = 0
        saturation = 0
        intensity = minc

    return hue, saturation, intensity
