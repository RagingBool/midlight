
from lights.light_state import LightState, RGBColor


class Light(object):
    """
    Base class for the representation of a single light. This is a mostly a
    container, for the high level rendering to set a color and for the low
    level output to get it and emit.
    Each instance of this class corresponds to a single physical light unit
    (LED or set of LEDs which always have the same light configuration).
    """
    STATE_TYPE = LightState

    def __init__(self, id):
        self._id = id

    def __str__(self):
        return "Light #{}".format(self._id)

    @property
    def id(self):
        return self._id

    @property
    def state(self):
        """
        The state of the physical light unit.
        """
        return self._state

    @state.setter
    def state(self, state):
        if not isinstance(state, self.STATE_TYPE):
            raise TypeError("This light's state should be a {}". \
                format(self.STATE_TYPE))
        self._state = state


class RGBLight(Light):
    STATE_TYPE = RGBColor
