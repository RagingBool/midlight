from lights.util import filter_for
from common.geometry.cards import E_L, E_R, E_B, T, T_L, T_T, T_R, L_1, R_1, \
    L_2, R_2, L_3, R_3, CardsGeometry, HOUSES_KEYS, HOUSES
from lights.state_gen.consts import DELTA
from common.color import RGBColor


@filter_for(CardsGeometry)
def color_the_cards_filter(upstream):
    edgeset=[[e for e in HOUSES[h] if 'E' in e] for h in HOUSES_KEYS]
    rotationset=[[t for t in HOUSES[h] if 'T' in t] for h in [L_3,R_3]]
    rotationset=[[rotationset[0][i],rotationset[1][i]] for i in range(3)]
    time=0
    for light_state, input_state in upstream:
        delta = input_state[DELTA]
        time += delta
        wavespeed = len(edgeset)
        colorlist=[(0,0,1) for z in range(1+int((time*wavespeed)%len(edgeset)))]
        for i in range(len(colorlist),len(edgeset)):
            colorlist.append((0,0,0))
        for (c,s,key) in zip(colorlist,edgeset,HOUSES_KEYS):
            for edge in s:
                light_state[key, edge].r = c[0]
                light_state[key, edge].g = c[1]
                light_state[key, edge].b = c[2]
        rotation_colors=[(1,0,0),(0,1,0),(0,0,1)]
        rotation_colors=[rotation_colors[int(3*time+i)%3] for i in range(3)]
        for (c,triangle) in zip(rotation_colors,rotationset):
            for i,house in enumerate([L_3,R_3]):
                light_state[house, triangle[i]].r = c[0]
                light_state[house, triangle[i]].g = c[1]
                light_state[house, triangle[i]].b = c[2]
        yield light_state
