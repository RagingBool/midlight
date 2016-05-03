
from common.lights.geometry import GeometryState


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
