
from lights.util import filter_for
from common.geometry.matrix import MatrixGeometry
from lights.state_gen import DELTA
from common.color import RGBColor

@filter_for(MatrixGeometry)
def sample_matrix_filter(upstream):
    accx = 0
    accy = 0
    periodx = 0.8
    periody = 1 
    gradex = 10
    gradey = 8
    for light_state, input_state in upstream:
        w, h = light_state.size
        delta = input_state[DELTA]
        accx += delta
        if accx >= periodx:
            accx -= periodx
        accy += delta
        if accy >= periody:
            accy -= periody
        for x in range(w):
            for y in range(h):
                light_state[x, y].h = ((x / gradex) + (accx / periodx)) % 1
                light_state[x, y].i = ((y / gradey) + (accy / periody)) % 1
                light_state[x, y].s = 1
        yield light_state
