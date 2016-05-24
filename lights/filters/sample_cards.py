
from lights.util import filter_for
from common.geometry.cards import E_L, E_R, E_B, T, T_L, T_T, T_R, L_1, R_1, \
    L_2, R_2, L_3, R_3, CardsGeometry, HOUSES_KEYS, HOUSES
from lights.state_gen import DELTA
from common.color import RGBColor

@filter_for(CardsGeometry)
def sample_cards_filter(upstream):
    accx = 0
    accy = 0
    periodx = 0.8
    periody = 1 
    outer = [(x, h, len(HOUSES[h]), list(enumerate(HOUSES[h]))) \
        for (x, h) in enumerate(HOUSES_KEYS)]
    gradex = len(outer)
    for light_state, input_state in upstream:
        delta = input_state[DELTA]
        accx += delta
        if accx >= periodx:
            accx -= periodx
        accy += delta
        if accy >= periody:
            accy -= periody
        for x, h, gradey, inner in outer:
            for y, c in inner:
                light_state[h, c].h = ((x / gradex) + (accx / periodx)) % 1
                light_state[h, c].i = ((y / gradey) + (accy / periody)) % 1
                light_state[h, c].s = 1
        yield light_state
