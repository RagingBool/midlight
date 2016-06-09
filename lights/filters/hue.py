
from lights.util import filter_for
from common.geometry.base import Geometry
from lights.state_gen.consts import DELTA, HUE, HUE_ALPHA, SATURATION, INTENSITY
from common.color import RGBColor


@filter_for(Geometry)
def hue_filter(upstream):
    for light_state, input_state in upstream:
        hue_alpha = input_state.pop(HUE_ALPHA, None)
        if hue_alpha is not None:
            hue = input_state.pop(HUE)
            for c in light_state.states:
                h = c.h
                h = h*(1-hue_alpha) + hue*hue_alpha
                c.h = h
        saturation = input_state.pop(SATURATION, None)
        if saturation is not None:
            for c in light_state.states:
                c.s *= saturation
        intensity = input_state.pop(INTENSITY, None)
        if intensity is not None:
            for c in light_state.states:
                c.i *= intensity
        yield light_state
