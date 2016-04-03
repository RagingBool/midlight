

from aitertools import aiter, anext
from functools import wraps

class _PopIterator(object):
    """
    Helper class for _Filter.
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

class _Filter(object):
    """
    Helper class for filter_for.
    """
    def __init__(self, geo_cls, upstream, filter, *args, **kwargs):
        self._geo_cls = geo_cls
        self._upstream = upstream
        self._ait = None
        self._pop_iter = _PopIterator()
        self._filter = iter(filter(self._pop_iter, *args, **kwargs))

    async def __aiter__(self):
        self._ait = await aiter(upstream)
        return self

    async def __anext__(self):
        geo_state, input_state = await anext(self._ait))
        if not isinstance(geo_state, self._geo_cls) or \
            not isinstance(input_state, dict):
            raise ValueError("Upstream iterator yielded a bad value.")
        self._pop_iter.set_value((geo_state, input_state))
        geo_state, input_state = next(self._filter)
        if not isinstance(geo_state, self._geo_cls) or \
            not isinstance(input_state, dict):
            raise ValueError("Filter yielded a bad value.")
        return geo_state, input_state


def filter_for(geo_cls):
    """
    Decorator factory, turning decorated generator into a valid aiterator
    filter for given geometry class.
    """
    def _inner(f):
        @wraps(f)
        def _inner2(upstream, *args, **kwargs):
            return _Filter(geo_cls, upstream, f, *args, **kwargs)
        return _inner2
    return _inner


def is_filter_for(f, geo_cls):
    if not isinstance(f, _Filter):
        return False
    if f._geo_cls != geo_cls:
        return False
    return True
