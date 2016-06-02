
import sys
import socket
import itertools

from lights.aitertools import aiter, anext
from common.geometry.base import Geometry
from common.packet import serialize_light
from common.light import Lights, ID
from common.color import f2b
from lights.opc import Client
from lights.e131client import E1_31DmxUniverse

class OutputDevice(object):
    """
    Base class for output devices. These are responsible for serializing the
    light configuration and sending it to the hardware.
    """
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
    def __init__(self, id, lights):
        lights = [ID(light) for light in lights]
        self._lights = lights
        self._id = id

    async def emit(self):
        s = " | ".join("{}: {} = {}".format(self._id, light, Lights[ID(light)]) \
            for light in self._lights)
        sys.stdout.write("\r  "+s+"    ")


class MonitorOutputDevice(OutputDevice):
    """
    Outputs packets of lights for the monitoring computer.
    """
    def __init__(self, lights):
        self._lights = lights
        self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._s.bind(("", 0))
        self._s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    async def emit(self):
        data = serialize_light(self._lights)
        try:
            self._s.sendto(data, ("255.255.255.255", 9999))
        except OSError:
            self._s.sendto(data, ("127.255.255.255", 9999))


class OPCOutputDevice(OutputDevice):
    """
    Send packets to OPC server. Input lights should be in the same order as
    they appear in the configuration of the fadecandy-server.
    """
    def __init__(self, addr, lights):
        lights = [ID(light) for light in lights]
        self._lights = lights
        self._client = Client(addr)
     
    async def emit(self):
        pixels = [tuple(f2b(c) for c in Lights[l]) for l in self._lights]
        self._client.put_pixels(pixels)


class DMXOutputDevice(OutputDevice):
    """
    Send packets to DMX via e1.31. Input lights should be in the same order as
    they are connected to the box.
    """
    def __init__(self, universe_id, component_identifier, offset, lights):
        lights = [ID(light) for light in lights]
        self._lights = lights
        self._universe = E1_31DmxUniverse(universe_id=universe_id, 
            component_identifier=component_identifier) 
        self._offset = offset
        if len(lights) + offset > 512:
            raise ValueError("Too many lights for one universe.")

    async def emit(self):
        values = bytearray(512)
        for i, c in enumerate(itertools.chain(*[Lights[l] for l in self._lights])):
            values[i + self._offset] = f2b(c)
        self._universe.send_frame(values)
