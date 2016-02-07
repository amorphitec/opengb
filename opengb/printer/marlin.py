import os
import serial
import time
import multiprocessing
import threading
import logging
import re
import json

from opengb.printer import IPrinter
from opengb.printer import State
from opengb.printer import NotReadyException

# Map Marlin message patterns to callbacks.
MSG_PATTERNS = [
    # Standard 'ok' message.
    (re.compile(r'ok$'),
     lambda g, c: (None)),
    # Standard 'echo' message.
    (re.compile(r'echo:\s*(?P<msg>.*)$'),
     lambda g, c: (getattr(c, 'log')(logging.DEBUG, g['msg']))),
    # Temperature update.
    (re.compile(r'ok T:(?P<n1temp>\d*\.?\d+)\s/(?P<n1target>\d*\.?\d+)\s'
                'B:(?P<btemp>\d*\.?\d+)\s/(?P<btarget>\d*\.?\d+)\s'
                'T0:(?P<n2temp>\d*\.?\d+)\s/(?P<n2target>\d*\.?\d+).*?$'),
     lambda g, c: (getattr(c, 'temp_update')(g['btemp'], g['btarget'],
                                             g['n1temp'], g['n1target'],
                                             g['n2temp'], g['n2target']))),
    # Position update.
    # Note: Marlin sends an errant space between X: and <xsteps>.
    (re.compile(r'X:(?P<xpos>\d*\.?\d+)\sY:(?P<ypos>\d*\.?\d+)\s'
                'Z:(?P<zpos>\d*\.?\d+)\sE:(?P<epos>\d*\.?\d+)\sCount\s'
                'X:\s(?P<xsteps>\d*\.?\d+)\sY:(?P<ysteps>\d*\.?\d+)\s'
                'Z:(?P<zsteps>\d*\.?\d+).*?$'),
     lambda g, c: (getattr(c, 'position_update')(g['xpos'], g['ypos'],
                                                 g['zpos']))),
    # Error.
    (re.compile(r'Error:(?P<error>.*)$'),
     lambda g, c: (getattr(c, 'log')(logging.ERROR, g['error']))),
]

# USB device name patterns.
USB_PATTERNS = [
    'ttyUSB\d*?',
    'ttyACM\d*?',
]

# Default baud rate
DEFAULT_BAUD_RATE = 115200


class BufferFullException(Exception):
    """
    Raised when a serial command cannot be sent to the printer because the
    buffer is full.
    """
    pass


class Marlin(IPrinter):
    """
    A printer controlled by `Marlin <http://www.marlinfirmware.org>`_ firmware.

    All Gcode execution is performed via the serial link.

    .. note:

        The paradigms here are likely to be useable with other serially-linked
        printers. In future it may be worth moving some of the relevant code
        to a separate base :class:`SerialExec` which can be inherited by other
        implementations of :class:`IPrinter`.

    .. note:

        This implementation of :Class:`IPrinter` for Marlin executes gcode for
        printing, bed levelling and other such sequential actions via
        individual commands sent down the serial link. An alternative approach
        for boards equipped with sd-cards is to first dump all gcode to the SD
        card and then let Marlin handle printing via the M20-M40 commands. Both
        approaches have advantages and disadvantages. This could be
        implemented via a separate base :class:`SDExec`.
    """

    def __init__(self, *args, **kwargs):
        # Connection
        if kwargs['baud_rate'] is None:
            self._serial_baud_rate = DEFAULT_BAUD_RATE
        else:
            self._serial_baud_rate = kwargs['baud_rate']
        if kwargs['port'] is None:
            self._serial_port = kwargs['port']
        else:
            self._serial_port = None
        self._serial_timeout = 0.01
        self._connect_retry_sec = 2
        self._serial = serial.Serial()
        self._serial_lock = threading.Lock()
        self._serial_buffersize = 10 
        self._serial_buffer = multiprocessing.Queue(self._serial_buffersize)
        # Timing
        self._idle_loop_delay_sec = 0.1
        self._print_loop_delay_sec = 0.001
        self._temp_poll_execute_sec = 5
        self._temp_poll_ready_sec = 1
        self._temp_update_time = time.time() - self._temp_poll_ready_sec
        # Gcode
        self._gcode_commands = []
        self._gcode_position = 0
        super().__init__(*args, **kwargs)

    def _connect(self):
        # Detect serial port if unspecified.
        if self._serial_port is None:
            try:
                self._callbacks.log(logging.INFO, 'Searching for printer.')
                port = self._detect_port()
                self._callbacks.log(logging.INFO, 'Printer found at ' + port)
            except ConnectionError:
                self._callbacks.log(logging.ERROR, 'No printer found.')
                raise
        else:
            port = self._serial_port
        try:
            self._serial.setPort(port)
            self._serial.setBaudrate(self._serial_baud_rate)
            self._serial.setTimeout(self._serial_timeout)
            self._serial.open()
            # Allow time for serial open to complete before reading/writing.
            time.sleep(1)
        except serial.SerialException as err:
            raise ConnectionError(err.args[0])

    def _detect_port(self):
        """
        Detect which port has a Marlin printer connected.

        .. note:: presently this is quite basic. It just looks for a connected
        USB device. In future it should probably attempt to connect to the
        port, send a piece of gcode and wait for a response.
        """
        usb_patterns_combined = "(" + ")|(".join(USB_PATTERNS) + ")"
        usb_paths = [os.path.join('/dev', p)
                     for p in os.listdir('/dev')
                     if re.match(usb_patterns_combined, p)]
        if len(usb_paths) == 0:
            raise ConnectionError('No printer found')
        return usb_paths[0]

    def _send_command(self, command, buffer=True):
        """
        Send a command to the serial port, attempting to re-connect if
        necessary.

        :param command: Command to send to the serial port.
        :type command: :class:`bytes`
        :returns: True if successful, otherwise False.
        :rtype: :class:`bool`
        :raises: `BufferFullException` if unable to send because the send
            buffer is full.
        """

        self._callbacks.log(logging.DEBUG, 'Sending command: ' + str(command))
        try:
            with self._serial_lock:
                if self._serial_buffer.full():
                    raise BufferFullException
                try:
                    self._serial.write(command + b'\n')
                    self._serial_buffer.put(command)
                except serial.SerialException:
                    self._callbacks.log, (logging.WARN, 'Error writing to '
                                          'serial port - reconnecting')
                    try:
                        self._connect()
                        self._serial.write(command)
                    except ConnectionError as err:
                        self._callbacks.log, (logging.ERROR, 'unable to '
                                              'connect to serial '
                                              'port: ' + err.args[0])
                        return False
        except IOError:
            self._callbacks.log, (logging.WARN, 'unable to lock serial port')
            return False
        return True

    def _request_printer_temperature(self):
        self._callbacks.log(logging.DEBUG, 'Requesting printer temperature')
        self._send_command(b'M105')

    def _request_printer_position(self):
        self._callbacks.log(logging.DEBUG, 'Requesting printer position')
        self._send_command(b'M114')

    def _get_message_from_printer(self):
        """
        Read a message from the serial port, attempting to re-connect if
        neccessary.
        """
        try:
            with self._serial_lock:
                try:
                    message = self._serial.readline()
                except serial.SerialException:
                    self._callbacks.log, (logging.WARN, 'Error reading from '
                                          'serial port - reconnecting')
                    try:
                        self._connect()
                    except ConnectionError as err:
                        self._callbacks.log, (logging.ERROR, 'unable to '
                                              'connect to serial '
                                              'port: ' + str(err))
                    finally:
                        return None
                except TypeError:
                    # Occasionally we encounter a BlockingIOError when reading
                    # from the serial port. This is not neccessarily a problem
                    # so log and continue.
                    self._callbacks.log, (logging.WARN, 'Blocking IO while '
                                          'reading from serial port')
                    return False
        except IOError:
            # Unable to lock the serial port.
            self._callbacks.log, (logging.WARN, 'Unable to lock serial port '
                                  'for reading')
            return False
        return message

    def _process_message_from_printer(self, message):
        """
        Process Marlin messages and fire appropriate callbacks.

        TODO: describe how this works in conjunction w/MSG_PATTERNS.
        """
        message = message.decode().rstrip()
        for each in MSG_PATTERNS:
            matched = each[0].match(message)
            if matched:
                self._callbacks.log(logging.DEBUG, 'Parsed: ' + message)
                each[1](matched.groupdict(), self._callbacks)
                break
        else:
            self._callbacks.log(logging.DEBUG, 'Unparsed: ' + message)
        # A message indicates a command was processed. So pop an item from
        # the serial buffer.
        if not self._serial_buffer.empty():
            self._serial_buffer.get()

    def set_temp(self, bed=None, nozzle1=None, nozzle2=None):
        if bed:
            self._send_command(b'M140 S' + str(bed).encode())
        if nozzle1:
            self._send_command(b'M104 T0 S' + str(nozzle1).encode())
        if nozzle2:
            self._send_command(b'M104 T1 S' + str(nozzle2).encode())

    def move_head_relative(self, x=0, y=0, z=0):
        # Switch to relative coordinates before sending.
        self._send_command(b'G91')
        self._send_command('G0 X{0} Y{1} Z{2}'.format(x, y, z).encode())
        self._request_printer_position()

    def move_head_absolute(self, x=0, y=0, z=0):
        # Switch to absolute coordinates before sending.
        self._send_command(b'G90')
        self._send_command('G0 X{0} Y{1} Z{2}'.format(x, y, z).encode())
        self._request_printer_position()

    def home_head(self, x=True, y=True, z=True):
        if not x and not y and not z:
            # Not homing any axes so don't bother sending a command.
            return
        command = 'G28'
        if x:
            command += ' X'
        if y:
            command += ' Y'
        if z:
            command += ' Z'
        self._send_command(command.encode())
        self._request_printer_position()

    def execute_gcode(self, gcode_commands):
        self._update_state(State.BUSY)
        self._gcode_commands = gcode_commands
        self._gcode_position = 0

    def emergency_stop(self):
        # NOTE: Marlin will skip buffering and process an M112 immediately
        # regardless of printer state:
        # https://github.com/MarlinFirmware/Marlin/issues/836
        self._send_command(b'M112')
        self._update_state(State.ERROR)

    def run(self):
        """
        Printer run loop.
        """
        if self._state == State.DISCONNECTED:
            try:
                self._connect()
                self._callbacks.log(logging.INFO, 'Connected to printer')
                self._update_state(State.READY)
            except ConnectionError as err:
                self._callbacks.log(logging.ERROR, err.args[0])
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

    def _reset_gcode_state(self):
        """
        Reset gcode state.
        """
        self._gcode = []
        self._gcode_position = 0

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
            print('queue: ' + str(self._serial_buffer.qsize()))
            time.sleep(self._idle_loop_delay_sec)

    def _writer(self):
        """
        Loops forver sending messages to the printer:

        * Requesting metric updates.
        * Forwarding message from the `self._to_printer` queue.
        * Executing buffered sequence of gcode commands

        Runs as a separate thread.
        """
        while True:
            # Request a metric update if the requisite interval has passed.
            metric_interval = time.time() - self._temp_update_time
            if (self._state == State.EXECUTING and
                metric_interval > self._temp_poll_execute_sec):
                    self._request_printer_temperature()
                    self._temp_update_time = time.time()
            elif (self._state == State.READY and
                metric_interval > self._temp_poll_ready_sec):
                    self._request_printer_temperature()
                    self._temp_update_time = time.time()
            # Process a message from the to_printer queue.
            if not self._to_printer.empty():
                message = self._to_printer.get()
                try:
                    self._process_message_to_printer(json.loads(message))
                except KeyError as err:
                    self._callbacks.log(logging.ERROR,
                                        'Malformed message sent to '
                                        'printer: ' + str(err))
            time.sleep(self._idle_loop_delay_sec)

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
        # TODO: Use decorator to designate allowed methods. Catch
        # NotReadyException and log error?
        if 'method' and 'params' in message.keys():
            getattr(self, message['method'])(**message['params'])
