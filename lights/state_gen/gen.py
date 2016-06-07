
import time
import asyncio

from lights.state_gen.consts import DELTA
from common.packet import parse, INPUT_PACKET, STROBE, HUE, HUE_ALPHA

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
        self._strobe = None
        self._hue = 0.0
        self._hue_alpha = None
        self._hue_wd = 0.0

    def dispatch(self, t, priority, value):
        if t == STROBE:
            self._strobe = value
        elif t == HUE:
            self._hue = value
            self._hue_wd = self._accu
        elif t == HUE_ALPHA:
            if value == 0.0:
                self._hue_alpha = None
            else:
                self._hue_alpha = value
            self._hue_wd = self._accu
            

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
        d = {
            DELTA: delta,
        }
        if self._strobe is not None:
            d[STROBE] = self._strobe
            self._strobe = None
        if self._hue_alpha is not None and self._hue_wd > self._accu - 1.0:
            d[HUE] = self._hue
            d[HUE_ALPHA] = self._hue_alpha 
        print("{}  \r".format(d), end="")
        return d


class StateGenDP(asyncio.DatagramProtocol):
    def __init__(self, state_gen):
        self._state_gen = state_gen

    def datagram_received(self, data, addr):
        p = parse(data, [INPUT_PACKET])
        if p is not None:
            t, priority, value = p
            self._state_gen.dispatch(t, priority, value)
