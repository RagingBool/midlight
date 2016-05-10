

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
