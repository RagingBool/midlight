
from lights.util import filter_for
from common.geometry.base import Geometry
from lights.state_gen.consts import DELTA
from common.color import RGBColor


def gamma_correction(gamma):
    @filter_for(Geometry)
    def inner(upstream):
        for light_state, input_state in upstream:
            for c in light_state.states:
                r = c.r
                r **= gamma
                c.r = min(r,1)
                g = c.g
                g **= gamma
                c.g = min(g,1)
                r = c.r
                r **= gamma
                c.r = min(r,1)
            yield light_state
    return inner()
