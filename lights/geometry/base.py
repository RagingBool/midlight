

class Geometry(object):
    """
    Base class for geometries of light collections. A Geometry object should:
    Construct with a collection of light objects;
    Have get_state which gives a matching GeometryState object with all the
        light states;
    Have set_state which gets a matchin GeometryState object and sets all the
        lights to their states.
    """
    STATE_OBJ = GeometryState

    def get_state(self):
        raise NotImplementedError()

    def set_state(self, geo_state):
        raise NotImplementedError()


class GeometryState(object):
    """
    Base class for geometries of light states. Corresponds to a Geometry class,
    and stores the state of lights under the correct geometry.
    Should always have a __iter__ method for going of all the lights serially.
    """
    def __init__(self):
        raise NotImplementedError()

    def __iter__(self):
        raise NotImplementedError()
