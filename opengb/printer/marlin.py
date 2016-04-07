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

# Response message patterns mapped to callbacks.
RESPONSE_MSG_PATTERNS = [
    # Standard 'ok' message.
    (re.compile(r'ok$'),
     lambda g, c: (None)),
    # Temperature update - single nozzle.
    (re.compile(r'ok T:(?P<alltemp>\d*\.?\d+)\s/(?P<alltarget>\d*\.?\d+)\s'
                'B:(?P<btemp>\d*\.?\d+)\s/(?P<btarget>\d*\.?\d+)\s'
                'T0:(?P<n1temp>\d*\.?\d+)\s/(?P<n1target>\d*\.?\d+)\s'
                '@:\d*\sB@:\d*$'),
     lambda g, c: (getattr(c, 'temp_update')(g['btemp'], g['btarget'],
                                             g['n1temp'], g['n1target'],
                                             None, None))),
    # Temperature update - dual nozzle.
    (re.compile(r'ok T:(?P<alltemp>\d*\.?\d+)\s/(?P<alltarget>\d*\.?\d+)\s'
                'B:(?P<btemp>\d*\.?\d+)\s/(?P<btarget>\d*\.?\d+)\s'
                'T0:(?P<n1temp>\d*\.?\d+)\s/(?P<n1target>\d*\.?\d+)\s'
                'T1:(?P<n2temp>\d*\.?\d+)\s/(?P<n2target>\d*\.?\d+)\s'
                '@:\d*\sB@:\d*$'),
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
]

# Event message patterns mapped to callbacks.
EVENT_MSG_PATTERNS = [
    # Standard 'echo' message.
    (re.compile(r'echo:\s*(?P<msg>.*)$'),
     lambda g, c: (getattr(c, 'log')(logging.DEBUG, g['msg']))),
    # Bed heating temperature update.
    (re.compile(r'T:(?P<ntemp>\d*\.?\d+)\sE:(?P<extruded>\d*)\s'
                'B:(?P<btemp>\d*\.?\d+)$'),
     lambda g, c: (getattr(c, 'temp_update')(g['btemp'], None,
                                             g['ntemp'], None,
                                             g['ntemp'], None))),
    # Nozzle 1 heating temperature update.
    (re.compile(r'T:(?P<ntemp>\d*\.?\d+)\sE:0\s'
                'W:(?P<countdown>(\?|\d+))$'),
     lambda g, c: (getattr(c, 'temp_update')(None, None,
                                             g['ntemp'], None,
                                             None, None))),
    # Nozzle 2 heating temperature update.
    (re.compile(r'T:(?P<ntemp>\d*\.?\d+)\sE:1\s'
                'W:(?P<countdown>(\?|\d+))$'),
     lambda g, c: (getattr(c, 'temp_update')(None, None,
                                            None, None,
                                            g['ntemp'], None))),
]

# State-change message patterns mapped to log level and new state.
STATE_CHANGE_MSG_PATTERNS = [
    # Filament swap.
    # If Marlin is configured with a `FILAMENT_RUNOUT_SENSOR` then an M600
    # message is generally sent when it is triggered. However an M600 is
    # also appended to Marlin's *incoming* command queue and if
    # `FILAMENTCHANGEENABLE` is configured Marlin will enter its filament
    # swap script.
    (re.compile(r'M600'), logging.INFO, State.FILAMENT_SWAP),
    # Error.
    (re.compile(r'Error:(?P<error>.*)$'), logging.ERROR, State.ERROR),
]

# USB device name patterns.
USB_PATTERNS = [
    'ttyUSB\d*?',
    'ttyACM\d*?',
]

# Defaults
DEFAULT_BAUD_RATE = 115200
DEFAULT_SERIAL_BUFFER_SIZE = 4

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
        self._serial_buffersize = DEFAULT_SERIAL_BUFFER_SIZE
        self._serial_buffer = multiprocessing.Queue(self._serial_buffersize)
        # Timing
        self._read_loop_delay_sec = 0.001
        self._write_loop_delay_sec = 0.001
        self._temp_poll_execute_sec = 5
        self._temp_poll_ready_sec = 1
        self._temp_update_time = time.time() - self._temp_poll_ready_sec
        self._progress_update_sec = 5
        self._progress_update_time = time.time() - \
            self._progress_update_sec
        # Gcode
        self._gcode_command_queue = []
        self._gcode_sequence = []
        self._gcode_sequence_position = 0
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
                self._update_state(State.DISCONNECTED)
                raise
        else:
            port = self._serial_port
        try:
            # Ensure port is closed in case last disconnect was ungraceful.
            self._serial.close()
            self._serial.setPort(port)
            self._serial.setBaudrate(self._serial_baud_rate)
            self._serial.setTimeout(self._serial_timeout)
            self._callbacks.log(logging.INFO, 'Connecting to printer.')
            self._serial.open()
            self._update_state(State.READY)
        except serial.SerialException as err:
            self._update_state(State.DISCONNECTED)
            raise ConnectionError(err.args[0])

    def _detect_port(self):
        """
        Detect which port has a Marlin printer connected.

        .. note:: presently this is quite basic. It just looks for a connected
        USB device. In future it should probably attempt to connect to the
        port, send a piece of gcode and wait for a response.
        """
        self._callbacks.log(logging.DEBUG, 'Detecting port.')
        usb_patterns_combined = "(" + ")|(".join(USB_PATTERNS) + ")"
        usb_paths = [os.path.join('/dev', p)
                     for p in os.listdir('/dev')
                     if re.match(usb_patterns_combined, p)]
        if len(usb_paths) == 0:
            raise ConnectionError('No printer found')
        self._callbacks.log(logging.DEBUG, 'Found ports: ' + str(usb_paths))
        return usb_paths[0]

    def _queue_command(self, command, deduplicate=False):
        """
        Queue a gcode command to be sent to the printer.

        :param command: Gcode command to queue.
        :type command: :class:`bytes`
        :param deduplicate: Only add command if it does not already exist in
            the queue.
        :type deduplicate: :class:`bool`
        """
        if deduplicate and command in self._gcode_command_queue:
            self._callbacks.log(logging.DEBUG, 'Deduplicated queued '
                                'command: ' + str(command))
            return
        self._gcode_command_queue.append(command)

    def _send_command(self, command, buffer=True):
        """
        Send a command to the serial port, attempting to re-connect if
        necessary.

        TODO: consider renaming this method such that it is analagous to
        get_message_from_printer (send_message_to_printer?)

        :param command: Command to send to the serial port.
        :type command: :class:`bytes`
        :param buffer: Only send command if space exists in the buffer.
        :type buffer: :class:`bool`
        :returns: True if successful, otherwise False.
        :rtype: :class:`bool`
        :raises: `BufferFullException` if unable to send because the send
            buffer is full.
        """

        try:
            with self._serial_lock:
                if buffer and self._serial_buffer.full():
                    raise BufferFullException('Buffer full. Unable to send '
                                              'command: ' + str(command))
                self._callbacks.log(logging.DEBUG,
                                    'Sending command: ' + str(command))
                try:
                    self._serial.write(command + b'\n')
                    self._serial_buffer.put(command)
                except (serial.SerialException, IOError):
                    self._callbacks.log(logging.WARN, 'Error writing to '
                                        'serial port - reconnecting')
                    # TODO: consider just updating state to DISCONNECTED
                    # and letting the main read thread reconnect.
                    try:
                        self._connect()
                        self._serial.write(command)
                    except ConnectionError as err:
                        self._callbacks.log(logging.ERROR, 'Unable to '
                                            'connect to serial '
                                            'port: ' + str(err.args[0]))
                        return False
        except IOError:
            self._callbacks.log(logging.DEBUG, 'Unable to lock serial port')
            return False
        return True

    def _reset_printer(self):
        self._callbacks.log(logging.DEBUG, 'Resetting printer')
        self._queue_command(b'M999', deduplicate=True)

    def _request_printer_temperature(self):
        """
        Request a temperature update from the printer.
        """
        self._callbacks.log(logging.DEBUG, 'Requesting printer temperature')
        self._queue_command(b'M105', deduplicate=True)

    def _request_printer_position(self):
        """
        Request a position update from the printer.
        """
        self._callbacks.log(logging.DEBUG, 'Requesting printer position')
        self._queue_command(b'M114', deduplicate=True)

    def _get_message_from_printer(self):
        """
        Read a message from the serial port, attempting to re-connect if
        neccessary.

        TODO: tidy returns/exceptions and document.
        """
        try:
            with self._serial_lock:
                try:
                    message = self._serial.readline()
                except (serial.SerialException, IOError, TypeError):
                    self._callbacks.log(logging.WARN, 'Error reading from '
                                          'serial port - reconnecting')
                    # TODO: consider just updating state to DISCONNECTED
                    # and letting the main read thread reconnect.
                    try:
                        self._connect()
                    except ConnectionError as err:
                        self._callbacks.log(logging.ERROR, 'Unable to '
                                              'connect to serial '
                                              'port: ' + str(err))
                    finally:
                        return None
        except IOError:
            # Unable to lock the serial port.
            self._callbacks.log(logging.WARN, 'Unable to lock serial port '
                                  'for reading')
            return False
        return message

    def _process_message_from_printer(self, message):
        """
        Process Marlin messages and fire appropriate callbacks.

        TODO: describe how this works in conjunction w/MSG_PATTERNS.
        """
        message = message.decode().rstrip()
        for each in RESPONSE_MSG_PATTERNS:
            matched = each[0].match(message)
            if matched:
                self._callbacks.log(logging.DEBUG,
                                    'Parsed response: ' + message)
                each[1](matched.groupdict(), self._callbacks)
                # Response message indicates a command was processed.
                # Pop an item off the serial buffer.
                if not self._serial_buffer.empty():
                    self._serial_buffer.get()
                return
        for each in EVENT_MSG_PATTERNS:
            matched = each[0].match(message)
            if matched:
                self._callbacks.log(logging.DEBUG,
                                    'Parsed event: ' + message)
                each[1](matched.groupdict(), self._callbacks)
                return
        for each in STATE_CHANGE_MSG_PATTERNS:
            matched = each[0].match(message)
            if matched:
                self._callbacks.log(each[1], message)
                self._update_state(each[2])
        self._callbacks.log(logging.ERROR, 'Unparsed message: ' + message)
        # An unparsed message sometimes indicates a message was "split" across
        # multiple lines and thus did not match a regex. This should not
        # happen but occasionally does causing the buffer to fill and printing
        # to stop. Until we work out why this splitting occurs and how to fix
        # it we simply take a message off the buffer for each of these.
        if not self._serial_buffer.empty():
            self._serial_buffer.get()

    def set_temp(self, bed=None, nozzle1=None, nozzle2=None):
        if bed != None:
            self._queue_command(b'M140 S' + str(bed).encode())
        if nozzle1 != None:
            self._queue_command(b'T0')
            self._queue_command(b'M104 S' + str(nozzle1).encode())
        if nozzle2 != None:
            self._queue_command(b'T1')
            self._queue_command(b'M104 S' + str(nozzle2).encode())

    def move_head_relative(self, x=0, y=0, z=0):
        # Switch to relative coordinates before sending.
        self._queue_command(b'G91')
        self._queue_command('G0 X{0} Y{1} Z{2}'.format(x, y, z).encode())
        self._request_printer_position()

    def move_head_absolute(self, x=0, y=0, z=0):
        # Switch to absolute coordinates before sending.
        self._queue_command(b'G90')
        self._queue_command('G0 X{0} Y{1} Z{2}'.format(x, y, z).encode())
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
        self._queue_command(command.encode())
        self._request_printer_position()

    def unretract_filament(self, head=0, length=5, rate=300):
        if head not in [0, 1]:
            self._callbacks.log(logging.ERROR, 'Invalid head: ' + str(head))
            return
        # Convert rate from mm/sec to mm/min.
        rate *= 60
        # Switch to relative coordinates before sending.
        self._queue_command(b'G91')
        # Switch to defined head.
        self._queue_command('T{0}'.format(head).encode())
        self._queue_command('G1 E{0} F{1}'.format(length, rate).encode())

    def retract_filament(self, head=0, length=5, rate=300):
        self.unretract_filament(head, -length, rate)

    def set_extrude_override(self, percent):
        self._queue_command('M221 S{0}'.format(percent).encode())
        self._callbacks.extrude_override_change(percent)

    def set_speed_override(self, percent):
        self._queue_command('M220 S{0}'.format(percent).encode())
        self._callbacks.speed_override_change(percent)

    def set_fan_speed(self, fan, percent):
        speed = int(percent / 100 * 255)
        self._queue_command('M106 P{0} S{1}'.format(fan, speed).encode())
        self._callbacks.fan_speed_change(fan, percent)

    def filament_swap_begin(self):
        self._callbacks.log(logging.DEBUG, 'Beginning filament swap')
        self._update_state(State.FILAMENT_SWAP)
        self._queue_command(b'M600')

    def filament_swap_complete(self):
        self._callbacks.log(logging.DEBUG, 'Completing filament swap')
        self._update_state(State.EXECUTING)
        # TODO: trigger a GPIO pin to simulate an lcd button press.

    def enable_steppers(self):
        self._queue_command(b'M17')
        self._callbacks.steppers_update(True)

    def disable_steppers(self):
        self._queue_command(b'M18')
        self._callbacks.steppers_update(False)

    def execute_gcode(self, gcode_sequence):
        self._update_state(State.EXECUTING)
        self._gcode_sequence = gcode_sequence
        self._gcode_sequence_position = 0

    def pause_execution(self):
        self._callbacks.log(logging.DEBUG, 'Pausing execution')
        self._update_state(State.PAUSED)

    def resume_execution(self):
        if self._state == State.PAUSED:
            self._callbacks.log(logging.DEBUG, 'Resuming execution')
            self._update_state(State.EXECUTING)

    def stop_execution(self):
        self._callbacks.log(logging.DEBUG, 'Stopping execution')
        self._reset_gcode_state()
        self._update_state(State.READY)

    def emergency_stop(self):
        # NOTE: Marlin will skip buffering and process an M112 immediately
        # regardless of printer state:
        # https://github.com/MarlinFirmware/Marlin/issues/836
        self._send_command(b'M112', buffer=False)
        self._callbacks.log(logging.ERROR, 'Emergency stop')
        self._update_state(State.ERROR)

    def run(self):
        """
        Printer run loop.
        """
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
        Clear the current gcode sequence and return position to 0.
        """
        self._gcode_sequence = []
        self._gcode_sequence_position = 0

    def _execute_next_queued_command(self):
        """
        Execute the next priority gcode command.
        """
        try:
            self._send_command(
                self._gcode_command_queue[0])
            self._gcode_command_queue.pop(0)
        except BufferFullException:
            # This probably means we're waiting for bed or nozzle temperature.
            pass

    def _execute_next_sequence_command(self):
        """
        Execute the next gcode command in the current sequence.
        """
        try:
            self._send_command(
                self._gcode_sequence[self._gcode_sequence_position].encode())
            self._gcode_sequence_position += 1
            # Complete execution if previous line was last in sequence.
            if self._gcode_sequence_position >= len(self._gcode_sequence):
                # Our last progress_update message probably didn't indicate
                # 100% complete. So send one last update to be sure.
                self._callbacks.progress_update(
                        self._gcode_sequence_position,
                        len(self._gcode_sequence))
                self._reset_gcode_state()
                self._update_state(State.READY)
        except BufferFullException:
            # This probably means we're waiting for bed or nozzle temperature.
            pass

    def _reader(self):
        """
        Loop forever collecting messages from the printer and converting
        them to `self._callbacks`.

        Also attempts to recover when printer enters a DISCONNECTED or ERROR
        state. If an attempt to recover fails the loops waits an arbitrary 1
        second before attempting to recover once again.

        Runs as a separate thread.
        """
        while True:
            if self._state == State.DISCONNECTED:
                try:
                    self._connect()
                except ConnectionError as err:
                    self._callbacks.log(logging.ERROR, 'Unable to '
                                        'connect to serial '
                                        'port: ' + str(err.args[0]))
                    time.sleep(1)
            elif self._state == State.ERROR:
                self._reset_printer()
                self._update_state(State.READY)
                time.sleep(1)
            else:
                msg_from_printer = self._get_message_from_printer()
                if msg_from_printer:
                    self._process_message_from_printer(msg_from_printer)
            time.sleep(self._read_loop_delay_sec)

    def _writer(self):
        """
        Loops forver sending messages to the printer:

        * Requesting metric updates.
        * Forwarding message from the `self._to_printer` queue.
        * Executing buffered priority gcode commands
        * Executing buffered sequence of gcode commands

        Runs as a separate thread.
        """
        while True:
            # If the printer is in an unhealthy state wait for the _reader
            # thread to take care of it.
            if self._state in [State.ERROR, State.DISCONNECTED]:
                time.sleep(self._write_loop_delay_sec)
                continue
            # Request a metric update if the requisite interval has passed.
            try:
                metric_interval = time.time() - self._temp_update_time
                if (self._state == State.EXECUTING and
                    metric_interval > self._temp_poll_execute_sec):
                    self._request_printer_temperature()
                    self._temp_update_time = time.time()
                elif (self._state in [State.READY, State.PAUSED] and
                    metric_interval > self._temp_poll_ready_sec):
                    self._request_printer_temperature()
                    self._temp_update_time = time.time()
            except BufferFullException:
                # Buffer is full so wait until next time.
                pass
            # Process a message from the to_printer queue.
            if not self._to_printer.empty():
                message = self._to_printer.get()
                try:
                    self._process_message_to_printer(json.loads(message))
                except KeyError as err:
                    self._callbacks.log(logging.ERROR,
                                        'Malformed message sent to '
                                        'printer: ' + str(err))
                # TODO: catch BufferFullException
            # Execute the next queued gcode command.
            if len(self._gcode_command_queue) > 0:
                self._execute_next_queued_command()
            # Execute the next command in the current sequence.
            if (self._state == State.EXECUTING and
                len(self._gcode_sequence) > 0):
                self._execute_next_sequence_command()
                # Request a position update if the requisite interval has 
                # passed.
                progress_interval = time.time() - self._progress_update_time
                if progress_interval > self._progress_update_sec:
                    self._callbacks.progress_update(
                        self._gcode_sequence_position,
                        len(self._gcode_sequence))
                    self._progress_update_time = time.time()
            time.sleep(self._write_loop_delay_sec)

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
        # TODO: create a utils.truncate which only truncates >80 and adds ...
        self._callbacks.log(logging.DEBUG,
                            'Processing printer message: ' + str(message)[:75])
        # TODO: Use decorator to designate allowed methods. Catch
        # NotReadyException and log error?
        if 'method' and 'params' in message.keys():
            getattr(self, message['method'])(**message['params'])
