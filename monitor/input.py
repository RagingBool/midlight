
import asyncio

class LightStateDP(asyncio.DatagramProtocol):
    def __init__(self, canvas, var):
        self.canvas = canvas
        self.var = var

    def datagram_received(self, data, addr):
        if self.var.get() != data[0]:
            print("Got {}, exiting".format(data.hex()))
            return
        print("Got {}, drawing".format(data.hex()))
        self.canvas.create_rectangle(0, 0, 100, 100, fill="#{}".format(data[1:4].hex()))
