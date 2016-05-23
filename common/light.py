
from common.color import LightState, RGBColor

ID_SIZE = 4


class ID(bytes):
    def __new__(cls, x):
        if isinstance(x, str):
            if len(x) > ID_SIZE*2:
                raise ValueError("Bad id.")
            return super().__new__(cls, bytes.fromhex(
                "{{:0>{size}.{size}s}}".format(size=ID_SIZE*2).format(x)))
        elif isinstance(x, int):
            if x >= (1 << (ID_SIZE*8)):
                raise ValueError("Bad id.")
            return super().__new__(cls, bytes.fromhex(
                "{{:0{size}X}}".format(size=ID_SIZE*2).format(x)))
        elif isinstance(x, (bytes, bytearray, list, tuple)):
            if len(x) != ID_SIZE:
                raise ValueError("Bad id.")
            return super().__new__(cls, x)
        elif isinstance(x, ID):
            return x
        else:
            raise TypeError("Bad id.")

    __str__ = bytes.hex


class FixedDict(dict):
    
    def __call__(self, key, type):
        if not isinstance(key, ID):
            raise TypeError("Key should be ID.")
        super().__setitem__(key, type())

    def __setitem__(self, key, value):
        if not isinstance(key, ID):
            raise TypeError("Key should be ID.")
        if key not in self:
            raise ValueError("Invalid key.")
        if not type(value) == type(self[key]):
            raise TypeError("Invalid value type.")


Lights = FixedDict()
