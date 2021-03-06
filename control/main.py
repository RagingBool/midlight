#!/usr/bin/env python3

import sys

import os
sys.path.append(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])  # FIXME

import asyncio
import itertools

from control.output import Outputer
from control.config import FRAME_RATE, KEEP_ALIVE, PRIORITY, MAX_STROBE, \
    INPUT_NAME
from control.midi import dispatch_callbacks

async def run(out):
    async for a in out:
        pass


def main():
    el = asyncio.get_event_loop()
    out = Outputer(FRAME_RATE, KEEP_ALIVE, PRIORITY)
    dispatch_callbacks(pads=[
        ("strobe", conv_strobe(MAX_STROBE)),
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ], knobs = [
        ("hue", conv_hue),
        ("hue_alpha", conv_alpha),
        ("saturation", conv_saturation),
        ("intensity", conv_intensity),
        None,
        None,
        None,
        None,
    ], ioloop=el, obj=out, input_name=INPUT_NAME)
    el.run_until_complete(run(out))


def conv_strobe(max_strobe):
    def inner(value, channel, press):
        return max_strobe * value / 127
    return inner

def conv_hue(value, channel):
    return value / 128

def conv_alpha(value, channel):
    return value / 127

def conv_saturation(value, channel):
    return value / 127

def conv_intensity(value, channel):
    return value / 127

if __name__ == "__main__":
    main()
