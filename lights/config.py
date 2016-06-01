
import sys

from lights.filters.sample_matrix import sample_matrix_filter
from lights.filters.sample_cards import sample_cards_filter
from lights.filters.sample_cake import sample_cake_filter

def get_config(pi_id):
    if pi_id == 1:
        return {
            "FILTERS": {
                "matrix0": (sample_matrix_filter(), True),
                "cards1": (sample_cards_filter(), True),
                "cake2": (sample_cake_filter(), True),
            },
            "DEBUG": {
                #"debug1": ["l00", "l10", "l01", "l11"],
            },
            "OPC": {
                "127.0.0.1:7890": [(0, 0, i//30, i%30) for i in range(60*30)],
            }
        }

FRAME_RATE = 30
