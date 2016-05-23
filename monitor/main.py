#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.split(os.path.split(__file__)[0])[0])

import tkinter as tk
import asyncio
import time

from monitor.input import LightStateDP
from common.geometry.matrix import MatrixGeometry
from common.config.example import GEOMETRIES
from monitor.matrix import MatrixPainter

async def run_tk(root, painters, interval=0.05):
    '''
    Run a tkinter app in an asyncio event loop.
    '''
    try:
        while True:
            t = time.time()
            for painter in painters:
                painter.paint()
            root.update()
            await asyncio.sleep(t+interval-time.time())
    except tk.TclError as e:
        if "application has been destroyed" not in e.args[0]:
            raise


PAINTERS = {
    MatrixGeometry: MatrixPainter,
}


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
    geos = list(GEOMETRIES.items())
    canvases = [tk.Canvas(master=master, height=300, width=600) for i in \
        range(len(geos))]
    radio_buttons = [tk.Radiobutton(
        master=master,
        text="{}: {}".format(type(geo).__name__, name),
        variable=var,
        value=i,
        command=PackCanvas(canvases, i)
    ) for (i, (name, geo)) in enumerate(geos)]
    for r in radio_buttons:
        r.pack(side="top")
    PackCanvas(canvases, 0)()
    painters = [PAINTERS[type(geo)](canvases[i], geo) for \
        i, (name, geo) in enumerate(geos)]
    asyncio.ensure_future(run_tk(master, painters))
    el = asyncio.get_event_loop()
    asyncio.ensure_future(el.create_datagram_endpoint(
        LightStateDP,
        local_addr=("0.0.0.0", 9999),
    ))
    el.run_forever()


if __name__ == "__main__":
    main()
