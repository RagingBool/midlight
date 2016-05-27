
import mido

from control.lpd8 import MIDI_NAME, PADS, RPADS

def dispatch_callbacks(pads, knobs):
    def inner(message):
        if message.type in ["note_on", "note_off"]:
            i = RPADS[message.channel][message.note]
            f = pads[i]
            if message.type == "note_on":
                press = True
                value = message.velocity
            else:
                press = False
                value = 0
            f(press=press, value=value, channel=message.channel)
        elif message.type == "control_change":
            i = message.control
            f = knobs[i]
            value = message.value
            f(value=value, channel=message.channel)
    port = mido.open_input(callback=inner)
    return port
