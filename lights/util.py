

from functools import wraps

from lights.aitertools import aiter, anext
from common.geometry.base import Geometry


class Filter(object):
    """
    Baseclass for synchronous (functional) filters. Implements a single method,
    _step, which receives a light state and an input state, and outputs a
    modified state. May consume members of the input state (mutable), except
    for the DELTA member.
    """
    GEO_CLS = Geometry

    def step(self, light_state, input_state):
        if not isinstance(input_state, dict) or \
            not isinstance(light_state, self.GEO_CLS):
            raise TypeError()
        new_light_state = self._step(light_state, input_state)
        #if not isinstance(new_light_state, self.GEO_CLS):
            #raise RuntimeError()
        # FIXME
        if not new_light_state is light_state:
            raise RuntimeError("Filter should only change the geo inplace.")
        return new_light_state

    def _step(self, light_state, input_state):
        raise NotImplementedError()


class _PopIterator(object):
    """
    Helper class for _FilterFor.
    """
    def __init__(self):
        self._value = None
    
    def __iter__(self):
        return self

    def __next__(self):
        if self._value is None:
            raise StopIteration()
        tmp = self._value
        self._value = None
        return tmp

    def set_value(self, value):
        self._value = value


def filter_for(geo_cls):
    """
    Decorator factory, turning decorated generator into a filter for given
    geometry class.
    """
    def _inner(f):
        class _FilterFor(Filter):
            GEO_CLS = geo_cls
        
            def __init__(self, *args, **kwargs):
                self._pop_iter = _PopIterator()
                self._it = iter(f(self._pop_iter, *args, **kwargs))
        
            def _step(self, light_state, input_state):
                self._pop_iter.set_value((light_state, input_state))
                return next(self._it)
        
        return _FilterFor
    return _inner


def is_filter_for(f, geo_cls):
    if not isinstance(f, Filter):
        return False
    if f.geo_cls != geo_cls:
        return False
    return True


class AsyncAppliedFilter(Filter):
    """
    Class for applying a filter to an aiter, getting a new aiter.
    """
    def __init__(self, filter, upstream):
        self._filter = filter
        self._upstream = upstream
        self._ait = None

    async def __aiter__(self):
        self._ait = await aiter(self._upstream)
        return self

    async def __anext__(self):
        light_state, input_state = await anext(self._ait)
        new_light_state = self._filter.step(light_state, input_state)
        return new_light_state, input_state
