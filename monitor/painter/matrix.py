
from monitor.painter.base import Painter


class MatrixPainter(Painter):

    def paint(self):
        for (x, y), c in self._geometry.items():
            self._canvas.itemconfig(self._rects[x, y], fill=str(c))

    def update_size(self, h, w):
        self._canvas.delete("all")
        self._rects = {}
        edge = min(w/self._geometry.width, h/self._geometry.height)
        for (x, y), c in self._geometry.items():
            self._rects[x, y] = self._canvas.create_rectangle(
                int(x*edge), int(y*edge),
                int((x+1)*edge), int((y+1)*edge),
                fill=str(c),
            )
