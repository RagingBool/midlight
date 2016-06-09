#!/usr/bin/env python3

import sys

import os
sys.path.append(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])  # FIXME
import time

from lights.e131client import E1_31DmxUniverse

def main():
    universe_id = 3
    component_identifier = "936DA01F-9ABD-4d9d-80C7-02AF85C822A8"
    e = E1_31DmxUniverse(universe_id=universe_id, component_identifier=component_identifier) 
    b = bytearray(512)
    # b[63 + 3*8] = 255
    b = bytes([255 for i in range(512)])
    e.send_frame(b)
    universe_id = 2
    component_identifier = "936DA01F-9ABD-4d9d-80C7-02AF85C822A8"
    e = E1_31DmxUniverse(universe_id=universe_id, component_identifier=component_identifier) 
    b = bytearray(512)
    # b[63 + 3*8] = 255
    b = bytes([255 for i in range(512)])
    e.send_frame(b)
    universe_id = 1
    component_identifier = "936DA01F-9ABD-4d9d-80C7-02AF85C822A8"
    e = E1_31DmxUniverse(universe_id=universe_id, component_identifier=component_identifier) 
    b = bytearray(512)
    # b[63 + 3*8] = 255
    b = bytes([255 for i in range(512)])
    e.send_frame(b)
    # while True:
        # e.send_frame(b)
        # time.sleep(0.01)

    
    # def __init__(self, universe_id, component_identifier, offset, lights):
        # lights = [ID(light) for light in lights]
        # self._lights = lights
        # self._offset = offset
        # if len(lights) + offset > 512:
            # raise ValueError("Too many lights for one universe.")

    # async def emit(self):
        # values = bytearray(512)
        # for i, c in enumerate(itertools.chain(*[Lights[l] for l in self._lights])):
            # values[i + self._offset] = f2b(c)
        # self._universe.send_frame(values)

if __name__ == "__main__":
    main()
