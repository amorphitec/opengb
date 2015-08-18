import time
import random
import logging

from opengb.printer import IPrinter
from opengb.printer import States 


class Dummy(IPrinter):
    """
    Dummy printer for testing purposes.
    """

    def __init__(self, to_addr, from_addr):
        super().__init__(to_addr, from_addr)

    def run(self):
        # TODO: Test code only
        while True:
            old_state = self._state
            new_state = random.choice(list(States))
            self._state = new_state
            self._callbacks.state_change(old_state, new_state)
            self._callbacks.log(logging.ERROR, 'test: '+ str(random.random()))
            time.sleep(1)
