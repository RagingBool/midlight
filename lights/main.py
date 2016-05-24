#!/usr/bin/env python3

import sys

import os
sys.path.append(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])  # FIXME

import asyncio
import itertools

from lights.config import get_config
from lights.state_gen.gen import STATE_GEN
from lights.aitertools import to_aiter, atee, azip, consume
from lights.filters.sample_matrix import sample_matrix_filter
from lights.filters.sample_cards import sample_cards_filter
from lights.util import AsyncAppliedFilter
from lights.output import DebugOutputDevice, MonitorOutputDevice
from common.config.example import GEOMETRIES


async def run(state_gen, geos_and_filters, outs):
    state_gens = list(atee(STATE_GEN, len(geos_and_filters)))
    for i, (geo, filters) in enumerate(geos_and_filters):
        upstream = azip(to_aiter(itertools.repeat(geo)), state_gens[i])
        for filter in filters:
            upstream = AsyncAppliedFilter(filter, upstream)
        state_gens[i] = upstream
    async for states in azip(*state_gens):
        for out in outs:
            await out.emit()


def main():
    conf = get_config(1)
    dl = {}
    outs = []
    geos_and_filters = []
    for geo_id, monitor in conf["MATRIX"].items():
        matrix = GEOMETRIES[geo_id]
        geos_and_filters.append((matrix, (sample_matrix_filter(),)))
        if monitor:
            outs.append(MonitorOutputDevice(matrix))
    for geo_id, monitor in conf["CARDS"].items():
        cards = GEOMETRIES[geo_id]
        geos_and_filters.append((cards, (sample_cards_filter(),)))
        if monitor:
            outs.append(MonitorOutputDevice(cards))
    for key, l in conf["DEBUG"].items():
        outs.append(DebugOutputDevice(key, l))
    el = asyncio.get_event_loop()
    el.run_until_complete(run(STATE_GEN, geos_and_filters, outs))

if __name__ == "__main__":
    main()
