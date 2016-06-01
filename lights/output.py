
import sys
import socket

from lights.aitertools import aiter, anext
from common.geometry.base import Geometry
from common.packet import serialize_light
from common.light import Lights, ID

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
    Outputs packets of entire geometries for the monitoring computer.
    """
    def __init__(self, geo):
        if not isinstance(geo, Geometry):
            raise TypeError("Geometry should be a geometry.")
        self._geo = geo
        self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._s.bind(("", 0))
        self._s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    async def emit(self):
        data = serialize_light(self._geo)
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
