
from lights.util import filter_for
from common.lights.matrix import MatrixGeometryState
from lights.state_gen import DELTA
from common.lights.light_state import RGBColor

@filter_for(MatrixGeometryState)
def sample_filter(upstream):
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
                light_state[x, y].r = ((x / gradex) + (accx / periodx)) % 1
                light_state[x, y].b = ((y / gradey) + (accy / periody)) % 1
        yield light_state
