
import sys

from lights.filters.sample_matrix import sample_matrix_filter
from lights.filters.sample_cards import sample_cards_filter
from lights.filters.sample_cake import sample_cake_filter
from lights.filters.cake_runner import cake_runner_filter
from lights.filters.randomizer import RandomizerFilter

def get_config(pi_id):
    if pi_id == 1:
        return {
            "FILTERS": {
                "matrix0": (sample_matrix_filter(), ),
                "cards1": (sample_cards_filter(), ),
                "cake2": (RandomizerFilter(
                    sample_cake_filter(),
                    cake_runner_filter(),
                    durations=(3, 4),
                     ),)
            },
            "DEBUG": {
                #"debug1": ["l00", "l10", "l01", "l11"],
            },
            "OPC": {
                "127.0.0.1:7890": [(0, 0, i//30, i%30) for i in range(60*30)],
            },
            "DMX": {
                ("936DA01F-9ABD-4d9d-80C7-02AF85C822A8", 1, 0): [(0, 1, i//3, i%3) for i in range(18)],
            },
        }

FRAME_RATE = 30
