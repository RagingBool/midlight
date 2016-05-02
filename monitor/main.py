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


def main():
    master = tk.Tk()
    var = tk.IntVar()
    r1 = tk.Radiobutton(master=master, text="abc", variable=var, value=0)
    r2 = tk.Radiobutton(master=master, text="def", variable=var, value=1)
    r1.pack(side="top")
    r2.pack(side="top")
    canvas = tk.Canvas(master=master, height=200, width=200)
    canvas.pack(side="bottom")
    canvas.create_rectangle(0, 0, 100, 100, fill="#123456")
    asyncio.ensure_future(run_tk(master))
    el = asyncio.get_event_loop()
    asyncio.ensure_future(el.create_datagram_endpoint(
        lambda: LightStateDP(canvas, var),
        local_addr=("127.0.0.1", 9999)
    ))
    el.run_forever()


if __name__ == "__main__":
    main()
