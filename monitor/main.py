#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.split(os.path.split(__file__)[0])[0])

import tkinter as tk
import asyncio
import time

from monitor.input import LightStateDP
from common.geometry.matrix import MatrixGeometry
from common.geometry.cards import CardsGeometry
from common.geometry.cake import CakeGeometry
from common.config.example import GEOMETRIES
from monitor.painter.matrix import MatrixPainter
from monitor.painter.cards import CardsPainter
from monitor.painter.cake import CakePainter


PAINTERS = {
    MatrixGeometry: MatrixPainter,
    CardsGeometry: CardsPainter,
    CakeGeometry: CakePainter,
}


async def run_tk(root, geos, radio_buttons, var, interval=0.05):
    '''
    Run a tkinter app in an asyncio event loop.
    '''
    try:
        old_val = -1
        old_w = -1
        old_h = -1
        c = tk.Canvas(root)
        painter = None
        while True:
            t = time.time()
            root.update()
            val = var.get()
            w = root.winfo_width()
            h = root.winfo_height()
            if val != old_val or w != old_w or h != old_h:
                old_val = val
                old_w = w
                old_h = h
                c.delete("all")
                c.pack_forget()
                del c
                del painter
                y = max(r.winfo_y() for r in radio_buttons)
                c = tk.Canvas(root, width=w, height=h-y, bd=-1, bg="#000000")
                c.pack(side="bottom")
                geo = geos[val]
                root.update()
                painter = PAINTERS[type(geo)](c, geo)
            painter.paint()
            root.update()
            await asyncio.sleep(t+interval-time.time())
    except tk.TclError as e:
        if "application has been destroyed" not in e.args[0]:
            raise


def main():
    master = tk.Tk()
    var = tk.IntVar()
    geos = list(GEOMETRIES.items())
    radio_buttons = [tk.Radiobutton(
        master=master,
        text="{}: {}".format(type(geo).__name__, name),
        variable=var,
        value=i,
    ) for (i, (name, geo)) in enumerate(geos)]
    for r in radio_buttons:
        r.pack(side="top")
    asyncio.ensure_future(run_tk(
        root=master,
        geos=[geo for (name, geo) in geos],
        radio_buttons=radio_buttons,
        var=var,
    ))
    el = asyncio.get_event_loop()
    asyncio.ensure_future(el.create_datagram_endpoint(
        LightStateDP,
        local_addr=("0.0.0.0", 9999),
    ))
    el.run_forever()


if __name__ == "__main__":
    main()
