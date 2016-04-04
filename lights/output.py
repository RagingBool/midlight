
import sys

from lights.light import Light
from lights.aitertools import aiter, anext

class OutputDevice(object):
    """
    Base class for output devices. These are responsible for serializing the
    light configuration and sending it to the hardware.
    Should be aiters, which send to hardware on __anext__.
    """
    def __init__(self, upstreams):
        self._upstreams = upstreams
        self._aits = None

    async def __aiter__(self):
        self._aits = []
        for aiterable in self._upstreams:
            self._aits.append(await aiter(aiterable))
        return self

    async def __anext__(self):
        for ait in self._aits:
            await anext(ait)
        await self.emit()
        
    async def emit(self):
        """
        Serialize and emit via the proper protocol a message for all the lights
        under this output device to change to their new color (or
        configuration).
        """
        raise NotImplementedError()


class DebugOutputDevice(OutputDevice):
    """
    Output device for debug purposes - prints the current state of the lights.
    """
    
    def __init__(self, id, lights, upstreams):
        super().__init__(upstreams)
        lights = list(lights)
        for light in lights:
            if not isinstance(light, Light):
                raise TypeError("All elements in collection should be Light " \
                    "objects")
        self._lights = lights
        self._id = id

    async def emit(self):
        s = " | ".join("{}: {} = {}".format(self._id, light, light.state) \
            for light in self._lights)
        sys.stdout.write("\r  "+s+"    ")
