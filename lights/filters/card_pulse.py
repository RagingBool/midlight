from lights.util import filter_for
from common.geometry.cards import CardsGeometry, EDGES, KEYS
from lights.state_gen.consts import DELTA
from common.color import RGBColor, rgb_to_hsi

@filter_for(CardsGeometry)
def card_pulse_filter(upstream):
    EDGES_SET = set(EDGES)
    edges = [x for x in KEYS if x[1] in EDGES_SET]
    triangles = [x for x in KEYS if not x[1] in EDGES_SET]
    bcolor = (1, 0, 0)
    fcolor = rgb_to_hsi(1, 0, 0)
    beat = 0.8
    current_beat = 0 
    direction = 1
    for light_state, input_state in upstream:
        delta = input_state[DELTA]
        hue = 0 #TODO: get hue from input state
        current_beat += delta*direction
        if current_beat > beat or current_beat < 0:
            current_beat = max(min(current_beat, beat), 0)
            direction *= -1
        fcolor =  (hue, fcolor[1], current_beat / beat)

        for x in edges:
            light_state[x[0], x[1]].r = bcolor[0]
            light_state[x[0], x[1]].g = bcolor[1]
            light_state[x[0], x[1]].b = bcolor[2]
        for x in triangles:
            light_state[x[0], x[1]].h = fcolor[0]
            light_state[x[0], x[1]].s = fcolor[1]
            light_state[x[0], x[1]].i = fcolor[2]
        yield light_state