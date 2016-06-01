5
from lights.util import filter_for
from common.geometry.cake import CakeGeometry, CAKE, CAKE_LAYER_KEYS, BOT, TOP, VER, HOR
from lights.state_gen.consts import DELTA
from common.color import RGBColor
from random import random

def get_random_color():
    return (random(),random(),random())

@filter_for(CakeGeometry)
def cake_runner_filter(upstream):
    #outer = {l: [(x, p, len(layer[p]), list(enumerate(layer[p]))) \
    #    for (x, p) in enumerate(CAKE_LAYER_KEYS[l])] for l, layer in CAKE.items()}
    #gradesx = {k: len(v) for k, v in outer.items()}
    verticals = CAKE[BOT][VER]
    horizontals = CAKE[BOT][HOR]
    time=0
    speedv=4 #speed of 1 is 1hz
    speedh=3  #speed of 1 is 1hz
    hcols = [(0.5,0.5,1), (0.2,0.5,1)]
    vcolor=(0.5,0.5,1)
    color_change_countdown = col_change_speed = 3*speedh
    for light_state, input_state in upstream:
        delta = input_state[DELTA]
        time+=delta
        color_change_countdown -= delta
        if color_change_countdown <= 0:
            hcols[0] = get_random_color()
            hcols[1] = get_random_color()
            vcolor=get_random_color()
            color_change_countdown += col_change_speed
        for layer in [BOT,TOP]:
            lv,pv = (layer, CAKE_LAYER_KEYS[layer][0])
            lh,ph = (layer, CAKE_LAYER_KEYS[layer][1])
            colorlist = [vcolor for i in verticals]
            colorlist[int(time*speedv)%8]=((time%10)/10,0.5,1)  #clockwise
            colorlist[-int(time*speedv)%8]=((time%5)/5,0.5,1) #anti-clockwise
            for d,c in zip(verticals,colorlist):
                light_state[lv, pv, d].h = c[0]
                light_state[lv, pv, d].i = c[1]
                light_state[lv, pv, d].s = c[2]
            colorlist = [hcols[0] for i in verticals]
            for z in range(int(speedh*time%2),len(colorlist),2):
                colorlist[z]=hcols[1]
            for d,c in zip(horizontals,colorlist):
                light_state[lh, ph, d].h = c[0]
                light_state[lh, ph, d].i = c[1]
                light_state[lh, ph, d].s = c[2]
        yield light_state

        