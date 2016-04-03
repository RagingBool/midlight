
import asyncio
import collections


async def aiter(aiterable):
    """
    Run __aiter__ of our aiterable.
    """
    return await ait.__aiter__()


async def anext(ait):
    """
    Get __anext of our aiterator.
    """
    return await ait.__anext__()


class _Tee(object):
    """
    Helper object for atee.
    """
    def __init__(self, aiterable, common_ait, deques, mydeque):
        self._aiterable = aiterable
        self._common_ait = common_ait
        self._ait = None
        self._deques = deques
        self._mydeque = mydeque
    
    async def __aiter__(self):
        if self._common_ait[0] is None:
            f = asyncio.Future()
            self._common_ait[0] = f
            try:
                self._ait = await aiter(self._aiterable)
            except Exception as e:
                f.set_exception(e)
                raise
            else:
                f.set_result(self._ait)
        else:
            self._ait = await self._common_ait[0]
        return self
    
    async def __anext__(self):
        if not self._mydeque:             # when the local deque is empty
            f = asyncio.Future()
            for d in self._deques:        # load it to all the deques
                if d is not self._mydeque:
                    d.append(f)
            try:
                val = await anext(self._ait)
            except Exception as e:
                f.set_exception(e)
                raise
            else:
                f.set_result(val)
                return val
        else:
            return await self._mydeque.popleft()


def atee(aiterable, n=2):
    """
    Split an aiterable into several aiterators; whenever the next value of the
    aiterable is ready, all of our aiterators will be notified.
    After this call, aiterable should not be used elsewhere.
    """
    ait = [None]
    deques = [collections.deque() for i in range(n)]
    return tuple(_Tee(aiterable, ait, deques, d) for d in deques)


class azip(object):
    """
    Zip several aiterables together.
    """
    def __init__(self, *aiterables):
        self._aiterables = aiterables
        self._aits = None

    def __aiter__(self):
        self._aits = tuple(await aiter(aiterable) for aiterable in aiterables)
        return self

    def __anext__(self):
        yield tuple(await anext(ait) for ait in self._aits)


class to_aiter(object):
    """
    Convert a given aiterable to aiter.
    """
    def __init__(self, iterable):
        self._it = iter(iterable)

    async def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            next(self._it)
        except StopIteration:
            raise StopAsyncIteration()


async def consume(aiter):
    """
    Consume an aiter.
    """
    async for i in aiter:
        pass
