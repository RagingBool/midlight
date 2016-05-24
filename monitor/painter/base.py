
class P(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iadd__(self, o):
        self.x += o.x
        self.y += o.y
        return self

    def __add__(self, o):
        n = P(self.x, self.y)
        n += o
        return n

    def __repr__(self):
        return "P({}, {})".format(self.x, self.y)

    def __imul__(self, m):
        self.x *= m
        self.y *= m
        return self

    def __mul__(self, m):
        n = P(self.x, self.y)
        n *= m
        return n


class Painter(object):
    def __init__(self, canvas, geometry):
        self._geometry = geometry
        self.update_size(canvas)

    def paint(self):
        raise NotImplementedError()

    def update_size(self, canvas):
        self._canvas = canvas
        self._update_size(canvas.winfo_height(), canvas.winfo_width())

    def _update_size(self, h, w):
        raise NotImplementedError()
