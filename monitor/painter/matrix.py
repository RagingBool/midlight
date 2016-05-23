
from monitor.painter.base import Painter


class MatrixPainter(Painter):
    def __init__(self, canvas, geometry):
        self._canvas = canvas
        self._matrix = geometry
        self._rects = {}
        edge = min(600/self._matrix.width, 300/self._matrix.height)
        for x, y in self._matrix.keys():
            self._rects[x, y] = self._canvas.create_rectangle(
                int(x*edge), int(y*edge),
                int((x+1)*edge), int((y+1)*edge),
            )

    def paint(self):
        for (x, y), c in self._matrix.items():
            self._canvas.itemconfig(self._rects[x, y], fill=str(c))

