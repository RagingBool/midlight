
import itertools

from lights.util import filter_for
from common.geometry.cake import CakeGeometry, CAKE, CAKE_LAYER_KEYS, CAKE_KEYS
from lights.state_gen.consts import DELTA
from common.color import RGBColor


def keys():
    ck = list(CAKE_KEYS)
    # ck.reverse()
    for l in ck:
        for p in CAKE_LAYER_KEYS[l]:
            for d in CAKE[l][p]:
                yield (l, p, d)


def test_cake_filter(period, color=False):
    @filter_for(CakeGeometry)
    def inner(upstream):
        acc = 0.0
        it = itertools.cycle(keys())
        cur = next(it)
        cur = next(it)
        cur = next(it)
        for light_state, input_state in upstream:
            delta = input_state[DELTA]
            acc += delta
            if acc >= period:
                acc -= period
                cur = next(it)
            for k in keys():
                light_state[k] = RGBColor(r=0, g=0, b=0)
            if color:
                light_state[cur] = RGBColor(h=acc/period, s=1, i=1)
            else:
                light_state[cur] = RGBColor(r=1, g=1, b=1)
            yield light_state
    return inner()
