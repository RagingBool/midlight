
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
