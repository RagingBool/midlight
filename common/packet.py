
import struct

from common.light import Lights, ID


def parse_light(buf):
    if not isinstance(buf, (bytes, bytearray)):
        raise TypeError("Bad type for buffer.")
    for i in range(0, len(buf), 8):
        if len(buf) < i + 8:
            raise ValueError("Buffer with bad size: {}".format(buf))
        Lights[ID(buf[i:i+4])].iparse(buf[i+4:i+8])


def parse_input(buf):
    if not isinstance(buf, (bytes, bytearray)):
        raise TypeError("Bad type for buffer.")
    if len(buf) < 6:
        raise ValueError("Buffer with bad size: {}".format(buf))
    t = INPUTS[buf[0]]
    dtype = INPUT_DTYPES[t]
    priority = buf[1]
    if dtype == bool:
        value = bool(struct.unpack(">I", buf[2:6]))
    elif dtype == int:
        value = struct.unpack(">I", buf[2:6])
    elif dtype == float:
        value = struct.unpack(">f", buf[2:6])
    else:
        raise RuntimeError("Bad dtype in config?")
    return t, priority, value


LIGHT_PACKET = "LIGHT"
INPUT_PACKET = "INPUT"

PACKETS = [
    LIGHT_PACKET,
    INPUT_PACKET,
]

RPACKETS = {v: i for i, v in enumerate(PACKETS)}

PARSERS = {
    LIGHT_PACKET: parse_light,
    INPUT_PACKET: parse_input,
}


def parse(buf, packet_types=None):
    """
    Parse a general packet.
    """
    if not isinstance(buf, (bytes, bytearray)):
        raise TypeError("Bad type for buffer.")
    t = PACKETS[buf[0]]
    parser = PARSERS[t]
    if packet_types is not None and t not in packet_types:
        return None
    return parser(buf[1:])


def serialize_light(light_ids):
    b = bytearray(1+len(light_ids)*8)
    b[0] = RPACKETS[LIGHT_PACKET]
    for i, light_id in enumerate(light_ids):
        b[1+8*i:1+8*i+4] = light_id
        b[1+8*i+4:1+8*i+8] = bytes(Lights[ID(light_id)])
    return bytes(b)


def serialize_input(t, priority, value):
    dtype = INPUT_DTYPES[t]
    if dtype == float:
        bvalue = struct.pack(">f", value)
    elif dtype == bool:
        bvalue = bool(struct.pack(">I", value))
    elif dtype == int:
        bvalue = struct.pack(">I", value)
    else:
        raise RuntimeError("Bad dtype in config?")
    return bytes([RPACKETS[INPUT_PACKET], RINPUTS[t], priority]) + bvalue


STROBE = "STROBE"
HUE = "HUE"
HUE_ALPHA = "HUE_ALPHA"

INPUTS = [
    STROBE,
    HUE,
    HUE_ALPHA,
]

RINPUTS = {v: i for i, v in enumerate(INPUTS)}

INPUT_DTYPES = {
    STROBE: float,
    HUE: float,
    HUE_ALPHA: float,
}
