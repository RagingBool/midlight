

class Geometry(object):
    """
    Base class for geometries of light collections. A Geometry object should:
    Construct with a collection of light objects;
    Have setters and getters which alter the light-state of these lights;
    Have an iterator which yields all lights, so their state can pass through
    some geometry-agnostic filter.
    """
    pass
