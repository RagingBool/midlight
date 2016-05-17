
class MatrixPainter(object):
    def __init__(self, canvas):
        self._canvas = canvas
        self._w = None
        self._h = None
        self._rects = None

    def paint(self, matrix_state):
        if self._w != matrix_state.width or self._h != matrix_state.height:
            self._w = matrix_state.width
            self._h = matrix_state.height
            self._rects = {}
            # FIXME: we assume canvas size 600x300.
            edge = min(600/matrix_state.width, 300/matrix_state.height)
            self._canvas.delete("all")
            for (x,y), c in matrix_state.items():
                self._rects[x, y] = self._canvas.create_rectangle(
                    int(x*edge), int(y*edge),
                    int((x+1)*edge), int((y+1)*edge),
                    fill=str(c),
                )
        else:
            for (x,y), c in matrix_state.items():
                self._canvas.itemconfig(self._rects[x, y], fill=str(c))
