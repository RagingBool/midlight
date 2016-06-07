
import sys

from lights.filters.sample_matrix import sample_matrix_filter
from lights.filters.sample_cards import sample_cards_filter
from lights.filters.sample_cake import sample_cake_filter
from lights.filters.test_cake import test_cake_filter
from lights.filters.cake_runner import cake_runner_filter
from lights.filters.randomizer import RandomizerFilter
from lights.filters.gamma import gamma_correction

def get_config(pi_id):
    if pi_id == 1:
        return {
            "FILTERS": {
                "matrix0": (sample_matrix_filter(), ),
                "cards1": (sample_cards_filter(), ),
                "cake2": (sample_cake_filter(), gamma_correction(1.1)),
                # "cake2": (test_cake_filter(5, color=True), ),
                # "cake2": (RandomizerFilter(
                    # sample_cake_filter(),
                    # cake_runner_filter(),
                    # durations=(3, 4),
                     # ),)
            },
            "DEBUG": {
                #"debug1": ["l00", "l10", "l01", "l11"],
            },
            "OPC": {
                "127.0.0.1:7890": [(0, 0, i//30, i%30) for i in range(60*30)],
            },
            "DMX": {
                ("936DA01F-9ABD-4d9d-80C7-02AF85C822A8", 1): {
                    0: [(0, 2, i//4, i%4) for i in range(8)] + [(0, 2, 2, 0), (0, 2, 2, 2)],
                    31: [(0, 2, i//4, 4 + i%4) for i in range(4)],
                    31+5*3: [(0, 2, i//4, 4 + i%4) for i in range(5, 8)] + [(0, 2, 2, 4), (0, 2, 2, 6)],
                    63: [(0, 2, 128 | (i//2), 2+(i%2)) for i in range(5)],
                    63+6*3: [
                        (0, 2, 2, 3),
                    ],
                    63+8*3: [
                        (0, 2, 128 | 2, 3),
                    ],
                },
                ("936DA01F-9ABD-4d9d-80C7-02AF85C822A8", 2): {
                    0: [(0, 2, 128 | (i//2), 4+(i%2)) for i in range(6)] + [
                        (0, 2, 2, 5),
                        (0, 2, 1, 4),
                    ],
                },
                ("936DA01F-9ABD-4d9d-80C7-02AF85C822A8", 3): {
                    0: [(0, 2, 128 | (i//2), (i%2)) for i in range(6)] + [
                        (0, 2, 2, 1),
                    ],
                    31: [(0, 2, 128 | (i//2), 6+(i%2)) for i in range(6)] + [
                        (0, 2, 2, 7),
                    ],
                },
            },
        }

FRAME_RATE = 5
