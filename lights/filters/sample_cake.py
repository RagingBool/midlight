
from lights.util import filter_for
from common.geometry.cake import CakeGeometry, CAKE, CAKE_LAYER_KEYS
from lights.state_gen.consts import DELTA
from common.color import RGBColor

@filter_for(CakeGeometry)
def sample_cake_filter(upstream):
    accx = 0
    accy = 0
    periodx = 0.8
    periody = 1 
    outer = {l: [(x, p, len(layer[p]), list(enumerate(layer[p]))) \
        for (x, p) in enumerate(CAKE_LAYER_KEYS[l])] for l, layer in CAKE.items()}
    gradesx = {k: len(v) for k, v in outer.items()}
    for light_state, input_state in upstream:
        delta = input_state[DELTA]
        accx += delta
        if accx >= periodx:
            accx -= periodx
        accy += delta
        if accy >= periody:
            accy -= periody
        for l, gradex in gradesx.items():
            for x, p, gradey, inner in outer[l]:
                for y, d in inner:
                    light_state[l, p, d].h = ((x / gradex) + (accx / periodx)) % 1
                    light_state[l, p, d].i = ((y / gradey) + (accy / periody)) % 1
                    light_state[l, p, d].s = 1
        yield light_state
