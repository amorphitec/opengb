import os
import serial
import time
import threading
import random
import logging
import re
import json

from opengb.printer import IPrinter
from opengb.printer import State 

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
]

# USB device name patterns.
USB_PATTERNS = [
    'ttyUSB\d*?',
    'ttyACM\d*?',
]


class Marlin(IPrinter):
    """
    A printer controlled by `Marlin <http://www.marlinfirmware.org>`_ firmware.
    """

    def __init__(self, *args, **kwargs):
        self._serial = serial.Serial()
        self._serial_lock = threading.Lock()
        super().__init__(*args, **kwargs)

    def _connect(self):
        # Detect serial port if unspecified.
        if self._port == None:
            port = self._detect_port()
        else:
            port = self._port
        try:
            self._serial.setPort(port)
            self._serial.setBaudrate(self._baud_rate)
            self._serial.setTimeout(self._timeout)
            self._serial.open()
            # Allow time for serial open to complete before reading/writing.
            time.sleep(1)
        except serial.SerialException as e:
            raise ConnectionError(e.args[0])

    def _detect_port(self):
        """
        Detect which port has a Marlin printer connected.

        NOTE: presently this is quite basic. It just looks for a connected
        USB device. In future it should probably attempt to connect to the
        port, send a piece of gcode and wait for a response.
        """
        self._callbacks.log(logging.INFO, 'Searching for printer.')
        usb_patterns_combined = "(" + ")|(".join(USB_PATTERNS) + ")"
        usb_paths = [os.path.join('/dev', p)
                     for p in os.listdir('/dev')
                     if re.match(usb_patterns_combined, p)]
        if len(usb_paths) == 0:
            #TODO: work out what to do with this downstream.
            self._callbacks.log(logging.ERROR, 'No printer found.')
            return None
        self._callbacks.log(logging.INFO, 'Printer found at '
                                          '{0}.'.format(usb_paths[0]))
        return usb_paths[0]

    def _send_command(self, command):
        """
        Send a command to the serial port, attempting to re-connect if
        necessary.
        
        :param command: Command to send to the serial port.
        :type command: :class:`bytes`
        :returns: True if successful, otherwise False.
        :rtype: :class:`bool`
        """

        self._callbacks.log(logging.DEBUG, 'Sending command: ' + str(command))
        try:
            with self._serial_lock:
                try:
                    self._serial.write(command + b'\n')
                except serial.SerialException:
                    self._callbacks.log, (logging.WARN, 'Error writing to '
                                          'serial port - reconnecting')
                    try:
                        self._connect()
                        self._serial.write(command)
                    except ConnectionError as e:
                        self._callbacks.log, (logging.ERROR, 'unable to connect '
                                          'to serial port: ' + str(e))
                        return False
        except IOError:
            # Unable to lock the serial port.
            return False
        return True

    def _request_printer_metrics(self):
        self._callbacks.log(logging.DEBUG, 'Requesting printer metrics')
        self._send_command(b'M105')

    def _request_printer_position(self):
        self._callbacks.log(logging.DEBUG, 'Requesting printer position')
        self._send_command(b'M114')

    def _print_line(self, line):
        # TODO: implement
        pass

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
                    except ConnectionError as e:
                        self._callbacks.log, (logging.ERROR, 'unable to '
                                          'connect to serial port: ' + e)
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
        """
        message = message.decode().rstrip()
        for each in MSG_PATTERNS:
            m = each[0].match(message)
            if m:
                self._callbacks.log(logging.DEBUG, 'Parsed: ' + message)
                each[1](m.groupdict(), self._callbacks)
                break
        else:
            self._callbacks.log(logging.DEBUG, 'Unparsed: ' + message)

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
        #self._to_printer.put(json.dumps({
        #    'method': '_request_printer_position',
        #    'params': {}}))           

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
        command += '\nM114'
        self._send_command(command.encode())
        self._request_printer_position()
        #self._to_printer.put(json.dumps({
        #    'method': '_request_printer_position',
        #    'params': {}}))           
