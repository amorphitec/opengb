import serial
import time
import threading
import random
import logging
import re

from opengb.printer import IPrinter
from opengb.printer import State 


# Map Marlin message patterns to callbacks.
MSG_PATTERNS = [
    # Standard 'echo' message.
    (re.compile(r'echo:\s*(?P<msg>.*)$'),
     lambda g, c: (getattr(c, 'log')(logging.INFO, g['msg']))),
    # Temperature update.
    (re.compile(r'ok T:(?P<n1temp>.*)\s/'
                '(?P<n1target>.*)\s'
                'B:(?P<btemp>.*)\s/'
                '(?P<btarget>.*)\s'
                'T0:(?P<n2temp>.*)\s/'
                '(?P<n2target>.*).*$'),
     lambda g, c: (getattr(c, 'temp_update')(g['btemp'], g['n1temp'],
                                             g['n2temp']))),
]


class Marlin(IPrinter):
    """
    A printer controlled by `Marlin <http://www.marlinfirmware.org>`_ firmware.
    """

    def __init__(self, to_printer, printer_callbacks=None, baud_rate=115200,
                 port='/dev/ttyACM0'):
        self._baud_rate = baud_rate
        # TODO: make default port None and auto-find if unspecified.
        self._port = port
        self._timeout = 0.01
        self._serial = serial.Serial()
        self._serial_lock = threading.Lock()
        super().__init__(to_printer, printer_callbacks=printer_callbacks)

    def _connect(self):
        try:
            self._serial.setBaudrate(self._baud_rate)
            self._serial.setPort(self._port)
            self._serial.setTimeout(self._timeout)
            self._serial.open()
            # Allow time for serial open to complete before reading/writing.
            time.sleep(1)
        except serial.SerialException as e:
            raise ConnectionError(e)

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

    def _print_line(self, line):
        """
        Generates a log response containing the gode that would be printed.

        :param line: Line of gcode.
        :type line: :class:`str`
        """
        # TODO: implement

    def _get_message_from_printer(self):
        """
        Read a message from the serial port, atttempting to re-connect if
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
        except IOError:
            # Unable to lock the serial port.
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
                each[1](m.groupdict(), self._callbacks)
                break
            time.sleep(1)
        else:
            self._callbacks.log(logging.DEBUG, 'Unparsed: ' + message)
