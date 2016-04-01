
class LightManager(object):
    """
    Base class for light managers. A light manager controls a collection of
    many light which have some physical affiliation (i.e. part of the same
    large object), and therefore should be managed together. The manager is
    responsible for generating meaningful images using their lights.
    """

    def render(self, input_state):
        """
        Render light states to all lights controlled by this manager, according
        to the given input_state.
        """
        raise NotImplementedError()

