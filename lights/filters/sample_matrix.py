
from lights.util import filter_for
from lights.geometry.matrix import MatrixGeometryState
from lights.state_gen import DELTA
from lights.light_state import RGBColor

@filter_for(MatrixGeometryState)
def sample_filter(upstream):
    acc = 0
    period = 0.5
    ind = 0
    for light_state, input_state in upstream:
        w, h = light_state.size
        assert w == 2
        assert h == 2
        delta = input_state[DELTA]
        acc += delta
        if acc >= period:
            acc -= period
            ind += 1
        light_state[(ind//2)%2, ind%2].r = 0
        light_state[((ind+1)//2)%2, (ind+1)%2].r = 255
        yield light_state
