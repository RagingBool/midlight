#!/usr/bin/env python3

import sys
import asyncio

from lights.config import get_config
from lights.light import RGBLight
from lights.state_gen import STATE_GEN
from lights.geometry.matrix import MatrixGeometry
from lights.aitertools import to_aiter, atee, azip, consume
from lights.filters.sample_matrix import sample

def iter_state(obj):
    while True:
        yield obj.get_state()

def main():
    conf = get_config(1)
    dl = {}
    matrix_m = []
    for row in conf["MATRIX"]:
        new_row = []
        for id in row:
            l = dl.setdefault(id, RGBLight(id))
            new_row.append(l)
        matrix_m.append(new_row)
    matrix = MatrixGeometry(matrix_m)

    filter_and_geos = [
        (sample, matrix),
    ]
    state_gens = atee(STATE_GEN, len(filter_and_geos)
    outs = [f(to_aiter(iter_state(o)), state_gens[i]) for (i,(f,o)) in \
        enumerate(filter_and_geos)]
    outss = [atee(o, len(conf["DEBUG"]) for o in outs]
    debug_d = {}
    for i, (key, l) in enumerate(conf["DEBUG"].items()):
        new_l = []
        for id in l:
            l = dl.setdefault(id, RGBLight(id))
            new_l.append(l)
        debug_d[key] = DebugOutputDevice(key, new_l, [os[i] for os in outss])
    
    el = asyncio.get_event_loop()
    el.run_until_complete(asyncio.wait(tuple(
        consume(debug) for debug in debug_d.values())))

if __name__ == "__main__":
    main()
