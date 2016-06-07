
import time
import asyncio

from lights.state_gen.consts import DELTA

class StateGen(object):
    """
    This class, a singleton, is an aiter responsible for aggregating the inputs
    and creating a coherent input state to be used by light managers.
    """
    def __init__(self, framerate):
        if not isinstance(framerate, int):
            raise TypeError("Framerate should be integral")
        self._init_t = time.time()
        self._accu = 0.0
        self._framecount = 0
        self._framerate = framerate

    async def __aiter__(self):
        return self

    async def __anext__(self):
        left = (self._framecount / self._framerate) + self._init_t - time.time()
        if left > 0:
            await asyncio.sleep(left)
        rel = time.time() - self._init_t
        delta = rel - self._accu
        self._accu += delta  # This is to avoid floating error drift.
        self._framecount += 1
        return {
            DELTA: delta,
        }


class StateGenDP(asyncio.DatagramProtocol):
    def __init__(self, state_gen):
        self._state_gen = state_gen

    def datagram_received(self, data, addr):
        p = parse(data, [INPUT_PACKET])
        if p is not None:
            t, priority, value = p
            self._state_gen.dispatch(t, priority, value)
