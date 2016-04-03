
from lights.util import filter_for
from lights.geometry.matrix import MatrixGeometryState

@filter_for(MatrixGeometryState)
def sample_filter(upstream):
    for light_state, input_state in upstream:
        w, h = light_state.size
        assert w == 2
        assert h == 2
        yield light_state, input_state
