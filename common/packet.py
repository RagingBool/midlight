
from common.lights.matrix import MatrixGeometryState

class LightPacket(object):
    """
    Represents a single network packet.
    """
    GEO_TO_INT = {
        MatrixGeometryState: 0,
    }

    INT_TO_GEO = {v: k for (k, v) in GEO_TO_INT.items()}

    def __init__(self, structure_id, state):
        self.structure_id = structure_id
        self.state = state

    def __bytes__(self):
        b = bytearray()
        if isinstance(self.state, MatrixGeometryState):
            b.append(self.GEO_TO_INT[MatrixGeometryState])
        else:
            raise TypeError("Bad state object")
        b.append(self.structure_id)
        b += bytes(self.state)
        return bytes(b)

    @classmethod
    def parse(cls, buf):
        if not isinstance(buf, (bytes, bytearray)):
            raise TypeError("Bad type for buffer.")
        Geo = cls.INT_TO_GEO[buf[0]]
        structure_id = buf[1]
        state = Geo.parse(buf[2:])
        return cls(structure_id=structure_id, state=state)


PACKET_TO_INT = {
    LightPacket: 0,
}

INT_TO_PACKET = {v: k for (k, v) in PACKET_TO_INT.items()}

def parse(buf):
    """
    Parse a general packet.
    """
    if not isinstance(buf, (bytes, bytearray)):
        raise TypeError("Bad type for buffer.")
    return INT_TO_PACKET[buf[0]].parse(buf[1:])

def serialize(packet):
    b = bytearray()
    if isinstance(packet, LightPacket):
        b.append(self.PACKET_TO_INT[LightPacket])
    else:
        raise TypeError("Bad packet.")
    b += bytes(packet)
    return bytes(b)
