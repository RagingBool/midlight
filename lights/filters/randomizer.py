
import itertools
import random

from lights.util import Filter
from lights.state_gen.consts import DELTA

_repeat = itertools.cycle

def _random_pick(l):
    while True:
        yield random.choice(l)

def _permutate_once(l):
    random.shuffle(l)
    return itertools.cycle(l)

def _permutate(l):
    while True:
        random.shuffle(l)
        yield from l

def _smart_permutate(l):
    small_third = len(l) // 3
    if small_third < 1:
        yield from _permutate_once(l)
    random.shuffle(l)
    spare = l[:small_third]
    yield from spare
    current = l[small_third:]
    while True:
        new_spare = current[:small_third]
        yield from new_spare
        current = current[small_third:] + spare
        random.shuffle(current)
        spare = new_spare


class RandomizerFilter(Filter):
    REPEAT = 0
    RANDOM_PICK = 1
    PERMUTATE_ONCE = 2
    PERMUTATE = 3
    SMART_PERMUTATE = 4
    _FILTER_ITERS = {
        REPEAT: _repeat,
        RANDOM_PICK: _random_pick,
        PERMUTATE_ONCE: _permutate_once,
        PERMUTATE: _permutate,
        SMART_PERMUTATE: _smart_permutate,
    }
    
    def __init__(self, *filters,
        durations,
        style=SMART_PERMUTATE
    ):
        geo_clss = set(f.GEO_CLS for f in filters)
        if len(geo_clss) > 1:
            raise TypeError("Filters for different geometries.")
        self.GEO_CLS = geo_clss.pop()
        self._filters = self._FILTER_ITERS[style](list(filters))
        if isinstance(durations, tuple):
            if len(durations) != 2:
                raise TypeError("Durations should be one or two floats.")
        elif isinstance(durations, (int, float)):
            durations = (float(durations), float(durations))
        else:
            raise TypeError("Durations should be one or two floats.")
        self._durations = durations
        self._current = next(self._filters)
        self._times = {k: 0.0 for k in filters}
        self._acc = 0.0
        self._end = self._next_time()

    def _next_time(self):
        return random.uniform(*self._durations) 

    def _step(self, light_state, input_state):
        dt = input_state[DELTA]
        self._acc += dt
        if self._acc > self._end:
            # FIXME: this only works if indeed dt << self._end.
            for k in self._times.keys():
                self._times[k] += self._acc
            self._times[self._current] = dt
            self._acc -= self._end
            self._current = next(self._filters)
            self._end =  self._next_time()
            input_state[DELTA] = self._times[self._current]
        out = self._current._step(light_state, input_state)
        input_state[DELTA] = dt
        return out
