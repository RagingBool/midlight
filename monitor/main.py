#!/usr/bin/env python

import tkinter as tk
import asyncio

from input import LightStateDP

async def run_tk(root, interval=0.05):
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


class CanvasPacker(object):
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
    canvas0 = tk.Canvas(master=master, height=200, width=200)
    canvas1 = tk.Canvas(master=master, height=200, width=200)
    canvases = [canvas0, canvas1]
    r0 = tk.Radiobutton(master=master, text="abc", variable=var, value=0,
        command=CanvasPacker(canvases, 0))
    r1 = tk.Radiobutton(master=master, text="def", variable=var, value=1,
        command=CanvasPacker(canvases, 1))
    r0.pack(side="top")
    r1.pack(side="top")
    asyncio.ensure_future(run_tk(master))
    el = asyncio.get_event_loop()
    asyncio.ensure_future(el.create_datagram_endpoint(
        lambda: LightStateDP(canvases),
        local_addr=("127.0.0.1", 9999),
    ))
    el.run_forever()


if __name__ == "__main__":
    main()
