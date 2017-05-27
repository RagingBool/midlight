#!/usr/bin/env python3

import sys

import os
sys.path.append(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])  # FIXME
import time

from lights.e131client import E1_31DmxUniverse

def main():
    while True:
        b = bytearray(512)
        universe_id_ks = [(5, 0), (6, 0), (7, 0), (7, 31), (8, 63)]
        index = 0
        universe_id, k = universe_id_ks[index]
        b[k:k+30] = bytes([
            255, 255, 255,
            255,   0,   0,
              0, 255,   0,
              0, 0,   255,
              0, 255, 255,
            255, 0,   255,
            255, 255,   0,
            255, 128,   0,
            128, 255,   0,
            128, 0,   255,
        ])
        component_identifier = "936DA01F-9ABD-4d9d-80C7-02AF85C822A8"
        e = E1_31DmxUniverse(universe_id=universe_id, component_identifier=component_identifier) 
        e.send_frame(b)
        time.sleep(2)
        # for universe_id_main in range(5, 9):
            # for j in range(1):
                # for k in [0, 31, 63]:
                    # b = bytearray(512)
                    # b = bytes([255 if i in range(k, k+32) else 0 for i in range(512)])
                    # for universe_id in range(5, 9):
                        # component_identifier = "936DA01F-9ABD-4d9d-80C7-02AF85C822A8"
                        # e = E1_31DmxUniverse(universe_id=universe_id, component_identifier=component_identifier) 
                        # if universe_id == universe_id_main:
                            # e.send_frame(b)
                        # else:
                            # e.send_frame(blank)
                    # print(universe_id_main, k)
                    # time.sleep(2)
    # universe_id = 2
    # component_identifier = "936DA01F-9ABD-4d9d-80C7-02AF85C822A8"
    # e = E1_31DmxUniverse(universe_id=universe_id, component_identifier=component_identifier) 
    # b = bytearray(512)
    # # b[63+3*9] = 255
    # b = bytes([255 for i in range(512)])
    # e.send_frame(b)
    # universe_id = 1
    # component_identifier = "936DA01F-9ABD-4d9d-80C7-02AF85C822A8"
    # e = E1_31DmxUniverse(universe_id=universe_id, component_identifier=component_identifier) 
    # b = bytearray(512)
    # # b[63 + 3*8] = 255
    # b = bytes([255 for i in range(512)])
    # e.send_frame(b)

    
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
