

class GeometryState(object):
    """
    Base class for geometries of light states. Corresponds to a Geometry class,
    and stores the state of lights under the correct geometry.
    Should always have a __iter__ method for going of all the lights serially.
    Must be (de-)serializable.
    """
    def __init__(self):
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()
    
    def __bytes__(self):
        raise NotImplementedError()

    @classmethod
    def parse(cls, buf):
        raise NotImplementedError()


class Geometry(object):
    """
    Base class for geometries of light collections. A Geometry object should:
    Construct with a collection of light objects;
    Have _get_state which gives a matching GeometryState object with all the
        light states;
    Have _set_state which gets a matchin GeometryState object and sets all the
        lights to their states.
    """
    STATE_CLS = GeometryState

    def get_state(self):
        state = self._get_state()
        if not isinstance(state, self.STATE_CLS):
            raise TypeError("_get_state returned bad type.")
        return state

    def _get_state(self):
        raise NotImplementedError()

    def set_state(self, state):
        if not isinstance(state, self.STATE_CLS):
            raise TypeError("Should only set to objects of type {}".format(
                self.STATE_CLS))
        self._set_state(state)

    def _set_state(self):
        raise NotImplementedError()
