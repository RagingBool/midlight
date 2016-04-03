
from lights.light import Light

class OutputDevice(object):
    """
    Base class for output devices. These are responsible for serializing the
    light configuration and sending it to the hardware.
    """
    
    def emit(self):
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

    def emit(self):
        print("Current state:")
        for light in self._lights:
            print("{}: {} = {}".format(self._id, light, light.state))
        print()
