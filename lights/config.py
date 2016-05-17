
import sys

def get_config(pi_id):
    if pi_id == 1:
        return {
            "MATRIX": {
                0: ([
                    ["l{:02d}{:02d}".format(x, y) for x in range(60)] \
                    for y in range(30)
                ], True)
            },
            "DEBUG": {
                #"debug1": ["l00", "l10", "l01", "l11"]
            },
        }

FRAME_RATE = 30
