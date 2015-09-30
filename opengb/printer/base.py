"""
Printer exceptions and interface.

TODO: Handle Farenheit vs Celsius
"""

import multiprocessing
import threading
import abc
import json
import time
import logging
import enum

from jsonrpc import JSONRPCResponseManager, dispatcher 


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
    Callbacks to be fired by :class:`IPrinter` when particular pr    occur.
    
    This base class implements placeholder callbacks that don't
    actually do anything. You probably want to sub-class this to send events
    to some kind of message queue.

    Inspired by _MachineComPrintCallback_ in Cura's `MachineCom
    <https://github.com/daid/Cura/blob/master/Cura/util/machineCom.py>`_
    class.
    """

    def __init__(self):
        pass

    def log(self, level, message):
        """
        Publish a log event. 

        :param level: Enumerated :mod:`logging` log level.
        :type level: :class:`int`
        :param message: Log message.
        :type message: :class:`str`
         """
        pass

    def state_change(self, old, new):
        """
        Publish a state change event.

        :param old: Old state.
        :type old: :class:`opengb.printer.State`
        :param new: New state.
        :type new: :class:`opengb.printer.State`
        """
        pass

    def temp_update(self, bed_current, bed_target, nozzle1_current,
                    nozzle1_target, nozzle2_current, nozzle2_target):
        """
        Publish a temperate update event.

        :param bed_current: Current bed temperature.
        :type bed_current: :class:`float`
        :param bed_target: Target bed temperature.
        :type bed_target: :class:`float`
        :param nozzle1_current: Current nozzle #1 temperature.
        :type nozzle1_current: :class:`float`
        :param nozzle1_target: Target nozzle #1 temperature.
        :type nozzle1_target: :class:`float`
        :param nozzle2_current: Current nozzle #2 temperature.
        :type nozzle2_current: :class:`float`
        :param nozzle2_target: Target nozzle #2 temperature.
        :type nozzle2_target: :class:`float`
        """
        pass

    def print_progress(self, current_file, current_line, total_lines):
        """
        Publish a print progress event.

        :param current_file: File currently being printed.
        :type current_file: :class:`str`
        :param current_line: Line number currently being printed.
        :type current_line: :class:`int`
        :param total_lines: Total number of lines to be printed.
        :type total_lines: :class:`int`
        """
        pass

    def z_change(self, new_z):
        """
        Publish a Z axis change event.

        :param position: Current Z axis position.
        :type position: :class:`float`
        """ 
        pass


class QueuedPrinterCallbacks(PrinterCallbacks):
    """
    Printer callbacks that place `JSON-RPC 2.0 <http://www.jsonrpc.org/specification>`_ event objects on a :class:`multiprocessing.Queue`. E.g.
        
        {
            'jsonrpc':  '2.0',
            'event':   '<event_nanme>',
            'params':   {
                'param1':   '<value_1>',
                'param2':   '<value_2>',
            }
        }

    :param from_printer: A queue upon which to place callback messages.
    :type from_printer: :class:`multiprocessing.Queue`
    """

    def __init__(self, from_printer):
        self._from_printer = from_printer

    def _publish(self, event):
        """
        Publish an event from the printer to the `_from_printer` queue.

        Adds the `'jsonrpc': '2.0'` key/value to maintain compatibility with
        the JSON-RPC 2.0 spec.

        :param event: Event to be placed on the queue. 
        :type event: :class:`dict`
        """
        event['jsonrpc'] = '2.0'
        self._from_printer.put(json.dumps(event))           

    def log(self, level, message):
        self._publish({
            'event':   'log',
            'params':   {
                'level':    level,
                'msg':      message,
            }
        })

    def state_change(self, old, new):
        self._publish({
            'event':   'state',
            'params':   {
                'old':      old.value,
                'new':      new.value,
            }
        })

    def temp_update(self, bed_current, bed_target, nozzle1_current,
                    nozzle1_target, nozzle2_current, nozzle2_target):
        self._publish({
            'event':   'temp',
            'params':   {
                'bed_current':      bed_current,
                'bed_target':       bed_target,
                'nozzle1_current':  nozzle1_current,
                'nozzle1_target':   nozzle1_target,
                'nozzle2_current':  nozzle2_current,
                'nozzle2_target':   nozzle2_target,
            }
        })

    def print_progress(self, current_file, current_line, total_lines):
        self._publish({
            'event':   'progress',
            'params':   {
                'current_file': current_file,
                'current_line': current_line,
                'total_lines':  total_lines,
            }
        })

    def z_change(self, position):
        self._publish({
            'event':  'ZCHANGE',
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

    def __init__(self, to_printer, printer_callbacks=None, baud_rate=115200,
                 port='/dev/ttyACM0'):
        # Configuration.
        # TODO: make these configurable in config file?
        self._connect_retry_sec = 2
        self._run_loop_delay_sec = 0.1
        self._print_loop_delay_sec = 0.001
        self._metric_interval_print_sec = 5 
        self._metric_interval_idle_sec = 1  
        self._metric_update_time = time.time() - self._metric_interval_idle_sec
        # State.
        self._temp_bed = 0
        self._temp_nozzle1 = 0
        self._temp_nozzle2 = 0
        self._target_temp_bed = 0
        self._target_temp_nozzle1 = 0
        self._target_temp_nozzle2 = 0
        self._gcode = [] 
        self._gcode_file = None
        self._gcode_position = 0
        self._state = State.DISCONNECTED
        self._to_printer = to_printer
        # Callbacks.
        if printer_callbacks == None:
            self._callbacks = PrinterCallbacks()
        else:
            self._callbacks = printer_callbacks
        # Connect.
        self._baud_rate = baud_rate
        self._port = port
        self._timeout = 0.01
        try:
            self._callbacks.log(logging.INFO, 'Connecting to printer.')
            self._connect()
            self._callbacks.log(logging.INFO, 'Connected to printer.')
            self._update_state(State.READY)
        except ConnectionError as e:
            self._callbacks.log(logging.ERROR, 'Connection error: ' + str(e))
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
    def _process_message_from_printer(self, message):
        """
        Process a message from the printer.

        If the message contains relevant data, extract this data and pass
        it to the most appropriate of the `self._callbacks`.

        :param message: Message from the printer.
        :type message: :class:`str`
        """
        pass

    @abc.abstractmethod
    def set_temp(self, bed=None, nozzle1=None, nozzle2=None):
        """
        Set printer target temperatures.

        :param bed: Bed target temperature
        :type bed: :class:`float`
        :param bed: Nozzle 1 target temperature
        :type bed: :class:`float`
        :param bed: Nozzle 2 target temperature
        :type bed: :class:`float`
        """
        pass

    def _print_file():
        # TODO: implement
        #    thread_printer = threading.Thread(target=self._print_file)
        #    thread_printer.setDaemon(True)
        #    thread_printer.setName('print_file')
        #    thread_printer.start()
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

    def _reset_gcode_state(self):
        """
        Reset globals related to gcode state.
        """
        self._gcode = [] 
        self._gcode_file = None
        self._gcode_position = 0
        
    def _load_gcode_file(self, path):
        """
        Load a gcode file into memory, ready to be sent to the printer.

        :param path: Path to gcode file.
        :type path: :class:`str`
        :raises IOError: if unable to open gcode file
        """
        self._reset_gcode_state()
        #TODO: Currently just loads raw file lines into list. Replace this and
        # all gcode refs in this class with GCode class from original codebase.
        with open(path) as gcode:
            self.gcode = list(gcode)

    def _process_message_to_printer(self, message):
        """
        Process a message that was sent to the printer via the
        :obj:`self._to_printer` queue by calling the specified `method` with
        the specified `params`.

        A message should be a dictionary containing values for `method` and
        `params`. E.g.

            {
                'method':   'set_temp',
                'params':   {
                    'base':     110
                    'nozzle1':  210
                    'nozzle2':  210
                }
            }
            
        :param message: Message to be sent to the printer.
        :type message: :class:`dict`
        """
        self._callbacks.log(logging.DEBUG,
                            'Processing printer message: ' + str(message))
        #TODO: Use decorator to designate allowed methods.
        if 'method' and 'params' in message.keys():
            getattr(self, message['method'])(**message['params'])
       
    def _reader(self):
        """
        Loop forever collecting messages from the printer and converting
        them to `self._callbacks`.
        
        Runs as a separate thread.
        """
        while True:
            self._callbacks.log(logging.DEBUG, 'Reading from_printer queue')
            msg_from_printer = self._get_message_from_printer()
            if msg_from_printer:
                self._process_message_from_printer(msg_from_printer)
            time.sleep(self._run_loop_delay_sec)
    
    def _writer(self):
        """
        Loops forver sending messages to the printer:

        * Requesting metric updates.
        * Forwarding message from the `self._to_printer` queue.

        Runs as a separate thread.
        """
        while True:
            # Request a metric update if the requisite interval has passed.
            metric_interval = time.time() - self._metric_update_time
            if (self._state == State.PRINTING and
                metric_interval > self._metric_interval_print_sec):
                   self._request_printer_metrics()
                   self._metric_update_time = time.time()
            elif (self._state == State.READY and
                metric_interval > self._metric_interval_idle_sec):
                   self._request_printer_metrics()
                   self._metric_update_time = time.time()
            # Process a message from the to_printer queue.
            if self._state == State.READY and not self._to_printer.empty():
                message = self._to_printer.get()
                try:
                    self._process_message_to_printer(json.loads(message))
                except KeyError as e:
                    self._callbacks.log(logging.ERROR,
                        'Malformed message sent to printer: ' + message)
            time.sleep(self._run_loop_delay_sec)
            
    def _print_file(self, gcode_file_path):
        """
        Load a gcode file into memory and print.

        Runs as a separate thread for the duration of a print.

        :param file_path: File path to print.
        """
        try:
            self._load_gcode_file(gcode_file_path)
        except IOError as e:
            self._callbacks.log(logging.ERROR, e)
        self._update_state(State.Printing)
        while self._gcode_position <= len(self._gcode):
            try:
                self._print_line(self._gcode[self._gcode_position])
                self._gcode_position += 1
            except Exception as e:
                # TODO: catch specific exceptions
                self._callbacks.log(logging.ERROR, e)
            time.sleep(self._print_loop_delay_sec)
        self._reset_gcode_state()
        self._update_state(State.Ready)

    def run(self):
        """
        Printer run loop.
        """
        # TODO: move this check to read/write serial method
        if self._state == State.DISCONNECTED:
            try:
                self._connect()
                self._callbacks.log(logging.INFO, 'Connected to printer')
                self._update_state(State.READY)
            except ConnectionError as e:
                self._callbacks.log(logging.ERROR, e)
                time.sleep(self._connect_retry_sec)

        thread_writer = threading.Thread(target=self._writer)
        thread_writer.setDaemon(True)
        thread_writer.setName('writer')
        thread_writer.start()

        thread_reader = threading.Thread(target=self._reader)
        thread_reader.setDaemon(True)
        thread_reader.setName('reader')
        thread_reader.start()

        for each in [thread_reader, thread_writer]:
            each.join()
