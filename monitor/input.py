
import asyncio

from common.packet import parse, LIGHT_PACKET


class LightStateDP(asyncio.DatagramProtocol):
    def datagram_received(self, data, addr):
        p = parse(data, [LIGHT_PACKET])
