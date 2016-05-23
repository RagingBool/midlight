

class Geometry(object):
    """
    Base class for geometries of lights.
    Stores the ids of lights, and gives API to get and set their light_states.
    Should give an iterable both of light ids (under ids) and of light states
    (under states).
    """
    @property
    def ids(self):
        raise NotImplementedError()

    @property
    def states(self):
        raise NotImplementedError()
