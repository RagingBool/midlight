
from lights.util import filter_for
from common.geometry.base import Geometry
from lights.state_gen.consts import DELTA, STROBE
from common.color import RGBColor


@filter_for(Geometry)
def strobe_filter(upstream):
    for light_state, input_state in upstream:
        strobe = input_state.pop(STROBE, None)
        if strobe is not None:
            strobe = min(strobe, 1.0)
            for c in light_state.states:
                c.r = c.r*(1-strobe) + strobe
                c.g = c.g*(1-strobe) + strobe
                c.b = c.b*(1-strobe) + strobe
        yield light_state
