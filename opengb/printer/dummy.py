import random
import logging

from opengb.printer import IPrinter


class Dummy(IPrinter):
    """
    Dummy printer for testing purposes.

    Dummy printer responses are inserted into `self._dummy_respones` as tuples
    in the format (method, *args) which represent a callback to fire, e.g.:

        (self._callbacks.log, [logging.DEBUG, 'This is a debug message.'])
        (self._callbacks.temp_update, [205, 108, 109])
    """

    def __init__(self, *args, **kwargs):
        self._dummy_responses = []
        self._temp_bed = 0
        self._temp_nozzle1 = 0
        self._temp_nozzle2 = 0
        super().__init__(*args, **kwargs)

    def _connect(self):
        self._callbacks.log(logging.DEBUG, 'Connecting to printer')

    def _request_printer_metrics(self):
        """
        Simulate a printer metric request/response by immediately generating a
        set of randomized dummy metrics and placing them on the dummy response
        queue.
        """
        self._callbacks.log(logging.DEBUG, 'Requesting printer metrics')
        self._dummy_responses.insert(0, (
            self._callbacks.temp_update,
            [
                random.randrange(200, 210),
                self._temp_bed,
                random.randrange(100, 110),
                self._temp_nozzle1,
                random.randrange(100, 110),
                self._temp_nozzle2,
            ]))

    def _print_line(self, line):
        """
        Generates a log response containing the gode that would be printed.

        :param line: Line of gcode.
        :type line: :class:`str`
        """
        self._dummy_responses.insert(
            self._callbacks.log,
            logging.DEBUG,
            'Printing gcode: ' + line)

    def _get_message_from_printer(self):
        """
        Simulate Grab the next dummy response in the queue.
        """
        if len(self._dummy_responses) > 0:
            return self._dummy_responses.pop()
        return None

    def _process_message_from_printer(self, message):
        """
        Fire the callback specified in the given message using specified
        arguments.
        """
        message[0](*message[1])

    def set_temp(self, bed=None, nozzle1=None, nozzle2=None):
        if bed:
            self._temp_bed = bed
        if nozzle1:
            self._temp_nozzle1 = nozzle1
        if nozzle2:
            self._temp_nozzle2 = nozzle2

    def move_head_relative(self, x=0, y=0, z=0):
        self._callbacks.log(logging.DEBUG, 'Moving print head to relative '
                                           'coordinates: x|{0}, y|{1}, '
                                           'z|{2}'.format(x, y, z))

    def move_head_absolute(self, x=0, y=0, z=0):
        self._callbacks.log(logging.DEBUG, 'Moving print head to absolute '
                                           'coordinates: x|{0}, y|{1}, '
                                           'z|{2}'.format(x, y, z))

    def home_head(self, x=True, y=True, z=True):
        self._callbacks.log(logging.DEBUG, 'Homing print head: x|{0}, '
                                           'y|{1}, z|{2}'.format(x, y, z))
