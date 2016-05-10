
def matrix_painter(canvas, matrix_state):
    # FIXME: we assume canvas size 600x300.
    edge = min(600/matrix_state.width, 300/matrix_state.height)
    for (x,y), c in matrix_state.items():
        canvas.create_rectangle(
            int(x*edge), int(y*edge),
            int((x+1)*edge), int((y+1)*edge),
            fill=str(c),
        )
