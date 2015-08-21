"""
Printer exceptions and interface.
"""

import multiprocessing
import abc
import json
from enum import Enum


class States(Enum):
    """
    Printer states.
    """

    INITIALIZING = 10
    READY = 20
    PRINTING = 30
    ERROR = 100


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

        Internal method.

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
        self._temp_bed = 0
        self._temp_nozzle1 = 0
        self._temp_nozzle2 = 0
        self._to_printer = to_printer
        # connect if not connected
        self._state = States.READY
        if printer_callbacks == None:
            self._callbacks = PrinterCallbacks()
        else:
            self._callbacks = printer_callbacks
        super().__init__()

    @abc.abstractmethod
    def run(self):
        """
        Printer run loop.
        
        0. Connect if unconnected
        1. Collect a message from the :obj:`self._to_printer` queue and
            generate a corresponding printer request.
        2. Request periodic data from the printer.
        3. Collect a message from the printer and  :obj:`self.callbacks` on printer events.
        4. Sleeps for defined interval.
        TODO: make sleep interval configurable?
        """
        if not self._to_printer.empty():
            message = json.loads(to_printer.get())


    @abc.abstractmethod
    def set_bed_target_temp(self, temp):
        """
        Set the bed target temperature.

        :param temp: Bed target temperature.
        :type temp: :class:`float`
        """
        pass

