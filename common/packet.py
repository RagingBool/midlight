
from common.light import Lights, ID


def parse_light(buf):
    if not isinstance(buf, (bytes, bytearray)):
        raise TypeError("Bad type for buffer.")
    for i in range(0, len(buf), 8):
        if len(buf) < i + 8:
            raise ValueError("Buffer with bad size: {}".format(buf))
        Lights[ID(buf[i:i+4])].iparse(buf[i+4:i+8])


LIGHT_PACKET = 0

PARSERS = {
    LIGHT_PACKET: parse_light,
}


def parse(buf, packet_types=None):
    """
    Parse a general packet.
    """
    if not isinstance(buf, (bytes, bytearray)):
        raise TypeError("Bad type for buffer.")
    t = buf[0]
    parser = PARSERS[t]
    if packet_types is not None and t not in packet_types:
        return None
    return parser(buf[1:])


def serialize_light(light_ids):
    light_ids = tuple(light_ids)
    b = bytearray(1+len(light_ids)*8)
    b[0] = LIGHT_PACKET
    for i, light_id in enumerate(light_ids):
        b[1+8*i:1+8*i+4] = light_id
        b[1+8*i+4:1+8*i+8] = bytes(Lights[ID(light_id)])
    return bytes(b)
