
import sys
import socket

from lights.light import Light
from lights.aitertools import aiter, anext
from lights.geometry.base import Geometry
from common.packet import LightPacket, serialize

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


class MonitorOutputDevice(OutputDevice):
    """
    Outputs packets of entire geometries for the monitoring computer.
    """
    def __init__(self, geo_id, geo):
        if not isinstance(geo_id, int):
            raise TypeError("Geometry id should be int.")
        self._geo_id = geo_id
        if not isinstance(geo, Geometry):
            raise TypeError("Geometry should be a geometry.")
        self._geo = geo
        self._s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._s.bind(("", 0))
        self._s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    async def emit(self):
        p = LightPacket(self._geo_id, self._geo.get_state())
        data = serialize(p)
        try:
            self._s.sendto(data, ("255.255.255.255", 9999))
        except OSError:
            self._s.sendto(data, ("127.255.255.255", 9999))

