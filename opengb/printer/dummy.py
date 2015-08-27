import time
import random
import logging
import multiprocessing

from opengb.printer import IPrinter
from opengb.printer import State 


class Dummy(IPrinter):
    """
    Dummy printer for testing purposes.
    """

    def __init__(self, to_addr, from_addr):
        super().__init__(to_addr, from_addr)

    def _connect(self):
        self._callbacks.log(logging.DEBUG, 'Connecting to printer.')

    def _request_printer_metrics(self):
        self._callbacks.log(logging.DEBUG, 'Requesting printer metrics.')
        # For now we just generate a random bed temperature.
        self._temp_bed = random.randrange(20, 30)
        # For now we cut out the middle man and initate the callback directly. 
        self._callbacks.temp_update(self._temp_bed, self._temp_nozzle1,
                                    self._temp_nozzle2)

    def _print_line(self, line):
        self._callbacks.log(logging.DEBUG, 'Printing gcode: ' + line)

    def _get_message_from_printer(self):
        pass

    def _process_message_from_printer(self):
        pass
