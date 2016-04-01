
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
    
    def __init__(self, lights):
        self._lights = lights

    def emit(self):
        print("Current state:")
        for i, light in enumerate(self._lights):
            print("Light {}: {}".format(i, light.state))
        print()
