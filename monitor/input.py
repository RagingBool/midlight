
import asyncio

from common.packet import parse, LightPacket
from common.geometry.matrix import MatrixGeometryState
from monitor.matrix import MatrixPainter


PAINTERS = {
    MatrixGeometryState: MatrixPainter,
}


class LightStateDP(asyncio.DatagramProtocol):
    def __init__(self, canvases, inputs_map):
        self.painters = {
            (struct_id, state_type): PAINTERS[state_type](canvases[i]) for \
            (struct_id, state_type), i in inputs_map.items()
        }

    def datagram_received(self, data, addr):
        p = parse(data, [LightPacket])
        if p is None:
            return
        painter = self.painters.get((p.structure_id, type(p.state)))
        if painter is None:
            return
        painter.paint(p.state)


