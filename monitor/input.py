
import asyncio

from common.packet import parse, LightPacket
from common.lights.matrix import MatrixGeometryState
from monitor.matrix import matrix_painter


PAINTERS = {
    MatrixGeometryState: matrix_painter,
}


class LightStateDP(asyncio.DatagramProtocol):
    def __init__(self, canvases, inputs_map):
        self.canvases = canvases
        self.inputs_map = inputs_map

    def datagram_received(self, data, addr):
        p = parse(data, [LightPacket])
        if p is None:
            return
        i = self.inputs_map.get((p.structure_id, type(p.state)))
        if i is None:
            return
        canvas = self.canvases[i]
        PAINTERS[type(p.state)](canvas, p.state)


