
from functools import wraps
import mido

from control.lpd8 import MIDI_NAME, PADS, RPADS

def dispatch_callbacks(input_name, pads, knobs, ioloop, obj):
    pads_ts = [threadsafe_setattr(ioloop, obj, tup[0], tup[1]) for tup in pads if tup]
    knobs_ts = [threadsafe_setattr(ioloop, obj, tup[0], tup[1]) for tup in knobs if tup]
    def inner(message):
        if message.type in ["note_on", "note_off"]:
            i = RPADS[message.channel][message.note]
            f = pads_ts[i]
            if message.type == "note_on":
                press = True
                value = message.velocity
            else:
                press = False
                value = 0
            f(press=press, value=value, channel=message.channel)
        elif message.type == "control_change":
            i = message.control
            f = knobs_ts[i]
            value = message.value
            f(value=value, channel=message.channel)
    port = mido.open_input(name=input_name, callback=inner)
    return port


def threadsafe_setattr(ioloop, obj, attr, f):
    """
    Decorator for functions which should set an attribute threadsafely.
    """
    def do_setattr(val):
        setattr(obj, attr, val)
    @wraps(f)
    def inner(*args, **kwargs):
        val = f(*args, **kwargs)
        ioloop.call_soon_threadsafe(do_setattr, val)
    return inner
