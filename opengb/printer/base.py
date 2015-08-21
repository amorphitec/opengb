"""
Printer exceptions and interface.

TODO: Handle Farenheit vs Celsius
"""

import multiprocessing
import abc
import json
import time
import logging
import enum



class State(enum.Enum):
    """
    Printer state.
    """

    DISCONNECTED = 10
    READY = 20
    PRINTING = 30
    ERROR = 100


class StateEncoder(json.JSONEncoder):
    """
    JSON encoder which serializes an Enum as a string of its name.
    """
    def default(self, obj):
        if isinstance(obj, enum.Enum):
            return obj.name
        return json.JSONEncoder.default(self, obj)


class PrinterCallbacks(object):
    """
    Callbacks to be fired by :class:`IPrinter` when particular printer events
    occur. This base class implements placeholder callbacks that don't
    actually do anything.

    Inspired by _MachineComPrintCallback_ in Cura's `MachineCom
    <https://github.com/daid/Cura/blob/master/Cura/util/machineCom.py>`_
    class.
    """

    def __init__(self):
        pass

    def log(self, level, message):
        """
        Publish a log message. 
        
        This is a placeholder which does nothing.
        """
        pass

    def temp_update(self, bed, nozzle1, nozzle2):
        """
        Publish a temperate update message.
        
        This is a placeholder which does nothing.
        """
        pass

    def state_change(self, old, new):
        """
        Publish a state change message.
        
        This is a placeholder which does nothing.
        """
        pass

    def print_progress(self, current_line, total_lines):
        """
        Publish a print progress message.
        
        This is a placeholder which does nothing.
        """
        pass

    def z_change(self, new_z):
        """
        Publish a Z axis change message.
        
        This is a placeholder which does nothing.
        """ 
        pass


class QueuedPrinterCallbacks(PrinterCallbacks):
    """
    Printer callbacks that place messages on a :class:`multiprocessing.Queue`.

    Messages are serialized to JSON and are generally a :class:`dict` in the
    format:
        
        {
            'cmd':      '<COMMAND_NAME>',
            'param1':   'value1',
            'param2':   'value2',
            ...
        }

    :param from_printer: A queue upon which to place callback messages.
    :type from_printer: :class:`multiprocessing.Queue`
    """

    def __init__(self, from_printer):
        self._from_printer = from_printer

    def _publish(self, message):
        """
        Publish a message from the printer to the `_from_printer` queue.

        :param message: Message to be placed on the queue. 
        :type message: :class:`dict`
        """
        self._from_printer.put(json.dumps(message))           

    def log(self, level, message):
        """
        Publish a log message.

        :param level: Enumerated :mod:`logging` log level.
        :type level: :class:`int`
        :param message: Log message.
        :type message: :class:`str`
        """
        self._publish({
            'cmd':      'LOG',
            'level':    level,
            'msg':      message,
        })

    def state_change(self, old, new):
        """
        Publish a change of state message.

        :param old: Old state.
        :type old: :class:`opengb.printer.State`
        :param new: New state.
        :type new: :class:`opengb.printer.State`
        """
        self._publish({
            'cmd':      'STATE',
            'old':      old.value,
            'new':      new.value,
        })

    def temp_update(self, bed, nozzle1, nozzle2):
        """
        Publish a temperature update message.

        TODO: deal with units (do we set this in the fw?).

        :param bed: Bed temperature.
        :type bed: :class:`float`
        :param nozzle1: Nozzle #1 temperature.
        :type nozzle1: :class:`float`
        :param nozzle2: Nozzle #2 temperature.
        :type nozzle2: :class:`float`
        """

        self._publish({
            'cmd':      'TEMP',
            'bed':      bed,
            'nozzle1':  nozzle1,
            'nozzle2':  nozzle2,
        })

    def print_progress(self, current_line, total_lines):
        """
        Publish a print progress message.

        :param current_line: Line number currently being printed.
        :type current_line: :class:`int`
        :param total_lines: Total number of lines to be printed.
        :type total_lines: :class:`int`
        """
        self._publish({
            'cmd':      'PROGRESS',
            'current':  current_lines,
            'total':    total_lines,
        })

    def z_change(self, position):
        """
        Publish a Z axis change message.

        :param position: Current Z axis position.
        :type position: :class:`float`
        """
        self._publish({
            'cmd':  'ZCHANGE',
            'position':  new_z,
        })


class IPrinter(multiprocessing.Process):
    """
    Printer interface. Runs as a separate process to ensure uninterrupted
    operation.

    Use a concrete implementation of this class.

    :param to_printer: Queue containing messages for the printer.
    :type to_printer: :class:`multiprocessing.Queue`
    :param printer_callbacks: Callbacks to be fired on printer events.
        TODO: mention defaults.
    :type printer_callbacks: :class:`PrinterCallbacks`
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, to_printer, printer_callbacks=None):
        # TODO: make these delays configurable
        self._connect_retry_sec = 2
        self._run_loop_delay_sec = 1
        self._metric_interval_print_sec = 5
        self._metric_interval_idle_sec = 2
        self._metric_update_time = time.time() - self._metric_interval_idle_sec
        self._temp_bed = 0
        self._temp_nozzle1 = 0
        self._temp_nozzle2 = 0
        self._target_temp_bed = 0
        self._target_temp_nozzle1 = 0
        self._target_temp_nozzle2 = 0
        self._gcode = None
        self._gcode_position = 0
        self._state = State.DISCONNECTED
        self._to_printer = to_printer
        if printer_callbacks == None:
            self._callbacks = PrinterCallbacks()
        else:
            self._callbacks = printer_callbacks
        try:
            self._connect()
            self._callbacks.log(logging.INFO, 'Connected to printer.')
            self._update_state(State.READY)
        except ConnectionError as e:
            self._callbacks.log(logging.ERROR, e)
        super().__init__()

    @abc.abstractmethod
    def _connect(self):
        """
        Establish connection to printer hardware.

        :raises: :class:`ConnectionError` if connection is unsuccessful.
        """
        pass

    @abc.abstractmethod
    def _request_printer_metrics(self):
        """
        Request a temperature update from the printer.
        """
        pass

    @abc.abstractmethod
    def _print_line(self, line):
        """
        Print a line of GCode.

        :param line: Line of gcode to print.
        :type line: :class:`str`
        """
        pass

    @abc.abstractmethod
    def _get_message_from_printer(self):
        """
        Get a message from the printer

        :returns: A message or None if no messages.
        """
        pass

    @abc.abstractmethod
    def _process_message_from_printer(self):
        """
        Process a message from the printer.
        """
        pass

    def _update_state(self, new_state):
        """
        Update printer state.

        :param new_state: New printer state.
        :type new_state: :class:`State`
        """
        old_state = self._state
        self._state = new_state
        self._callbacks.state_change(old_state, new_state)

    def _process_message_to_printer(self, message):
        """
        Process a message that was sent to the printer via the
        :obj:`self._to_printer` queue.

        TODO: if printing, queue command. Otherwise call the relevant function.
        TODO: implement abstract handlers for all valid incoming messages.
        TODO: enumerate valid incoming message commands + map to abstract functions?
        """
        pass

    def _print_next_line(self):
        """
        Print the next line of the current gcode file.

        TODO:
            1. print line
            2. update self._current_line
            3. if finished, update status
        """
        pass

    def run(self):
        """
        Printer run loop.
        """
        while True:
            # Ensure printer is connected 
            if self._state == State.DISCONNECTED:
                try:
                    self._connect()
                    self._callbacks.log(logging.INFO, 'Connected to printer.')
                    self._update_state(State.READY)
                except ConnectionError as e:
                    self._callbacks.log(logging.ERROR, e)
                    time.sleep(self._connect_retry_sec)
                    continue
            # Process a message sent from the printer.
            msg_from_printer = self._get_message_from_printer()
            if msg_from_printer:
                self._process_message_from_printer(msg_from_printer)
            # Request printer metrics if interval has passed for current state.
            metric_interval = time.time() - self._metric_update_time
            if (self._state == State.PRINTING and
                metric_interval > self._metric_interval_print_sec):
                   self._request_printer_metrics()
            if (self._state == State.READY and
                metric_interval > self._metric_interval_idle_sec):
                   self._request_printer_metrics()
                   self._metric_update_time = time.time()
            # Process a message sent to the printer.
            if self._state == State.READY and not self._to_printer.empty():
                try:
                    # TODO: Consider handling json and bs messages in func to make this uniform.
                    msg_to_printer = json.loads(to_printer.get())
                    self._process_message_to_printer(msg_to_printer)
                except KeyError as e:
                    self._callbacks.log(logging.ERROR,
                        'Malformed message to printer: {0}'.format(message))
            # Print a line if printing.
            if self._state == State.PRINTING:
                self._print_next_line()
            time.sleep(self._run_loop_delay_sec)
