
import time

DELTA = "DELTA"

class _StateGen(object):
    """
    This class, a singleton, is responsible for aggregating the inputs and
    creating a coherent input state to be used by light managers.
    """
    def __init__(self):
        self._init_t = time.time()
        self._accu = 0.0

    def render(self):
        """
        Create an input state frame.
        """
        rel = time.time() - self._init_t
        delta = rel - self._accu
        self.accu += delta  # This is to avoid floating error drift.
        return {
            DELTA: delta,
        }

StateGen = _StateGen()
