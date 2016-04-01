
class Light(object):
    """
    Base class for the representation of a single light. This is a mostly a
    container, for the high level rendering to set a color and for the low
    level output to get it and emit.
    Each instance of this class corresponds to a single physical light unit
    (LED or set of LEDs which always have the same light configuration).
    """

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
        raise NotImplementedError()

    @state.setter
    def state(self, state):
        raise NotImplementedError()
