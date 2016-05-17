#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.split(os.path.split(__file__)[0])[0])

import tkinter as tk
import asyncio

from monitor.input import LightStateDP
from common.lights.matrix import MatrixGeometryState

async def run_tk(root, interval=0.01):
    '''
    Run a tkinter app in an asyncio event loop.
    '''
    try:
        while True:
            root.update()
            await asyncio.sleep(interval)
    except tk.TclError as e:
        if "application has been destroyed" not in e.args[0]:
            raise


class PackCanvas(object):
    def __init__(self, canvases, ind):
        self.canvases = canvases
        self.canvas = canvases[ind]

    def __call__(self):
        for c in self.canvases:
            c.pack_forget()
        self.canvas.pack(side="bottom")


def main():
    master = tk.Tk()
    var = tk.IntVar()
    inputs_map = {k: i for (i, k) in enumerate([ \
        (0, MatrixGeometryState),
    ])}
    canvases = [tk.Canvas(master=master, height=300, width=600) for i in \
        range(len(inputs_map))]
    radio_buttons = [tk.Radiobutton(
        master=master,
        text="{}: {}".format(c.__name__, n),
        variable=var,
        value=i,
        command=PackCanvas(canvases, i)
    ) for ((n, c), i) in inputs_map.items()]
    for r in radio_buttons:
        r.pack(side="top")
    PackCanvas(canvases, 0)()
    asyncio.ensure_future(run_tk(master))
    el = asyncio.get_event_loop()
    asyncio.ensure_future(el.create_datagram_endpoint(
        lambda: LightStateDP(canvases, inputs_map),
        local_addr=("0.0.0.0", 9999),
    ))
    el.run_forever()


if __name__ == "__main__":
    main()
