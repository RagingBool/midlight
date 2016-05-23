
class Painter(object):
    def __init__(self, canvas, geometry, h, w):
        self._canvas = canvas
        self._geometry = geometry
        self.update_size(h, w)

    def paint(self):
        raise NotImplementedError()

    def update_size(self, h, w):
        raise NotImplementedError()
