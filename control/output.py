
import time
import asyncio

from common.packet import serialize_input, STROBE, HUE, HUE_ALPHA

class Outputer(object):
    """
    This class, a singleton, is an aiter responsible for aggregating the inputs
    and creating a coherent input state to be used by light managers.
    Keepalive is in frames.
    """
    def __init__(self, framerate, keepalive, priority):
        if not isinstance(framerate, int):
            raise TypeError("Framerate should be integral")
        self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._s.bind(("", 0))
        self._s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._init_t = time.time()
        self._accu = 0.0
        self._framecount = 0
        self._framerate = framerate
        self._priority = priority
        self._hue = 0.0
        self._hue_alpha = 0.0
        self._strobe = 0.0
        self._keepalive = keepalive

    @property
    def hue(self):
        return self._hue

    @hue.setter
    def hue(self, hue):
        self._hue = hue
        self._send_packet(HUE, hue)

    @property
    def hue_alpha(self):
        return self._hue_alpha

    @hue_alpha.setter
    def hue_alpha(self, hue_alpha):
        self._hue_alpha = hue_alpha
        self._send_packet(HUE_ALPHA, hue_alpha)

    @property
    def strobe(self):
        return self._strobe

    @strobe.setter
    def strobe(self, strobe):
        self._strobe = strobe
        self._send_packet(STROBE, strobe)

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
        
        if self._framecount % self._keepalive == 0:
            self._send_packet(STROBE, self._strobe)
            if self._hue_alpha > 0.0:
                self._send_packet(HUE, self._hue)
                self._send_packet(HUE_ALPHA, self._hue_alpha)
        
        if self._strobe > 0.0:
            self._strobe -= delta
        if self._strobe > 0.0:
            self._send_packet(STROBE, self._strobe)

    def _send_packet(self, t, value):
        data = serialize_input(t, self._priority, value)
        try:
            self._s.sendto(data, ("255.255.255.255", 9999))
        except OSError:
            self._s.sendto(data, ("127.255.255.255", 9999))
