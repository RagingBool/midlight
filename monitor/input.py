
import asyncio

class LightStateDP(asyncio.DatagramProtocol):
    def __init__(self, canvases):
        self.canvases = canvases

    def datagram_received(self, data, addr):
        if data[0] >= len(self.canvases):
            print("Got {}, exiting".format(data.hex()))
            return
        print("Got {}, drawing".format(data.hex()))
        self.canvases[data[0]].create_rectangle(0, 0, 100, 100, fill="#{}".format(data[1:4].hex()))
