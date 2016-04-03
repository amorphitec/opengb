import time
import random
import logging
import json

from opengb.printer import IPrinter
from opengb.printer import State


class Dummy(IPrinter):
    """
    Dummy printer for testing purposes.

    Dummy printer responses are inserted into `self._dummy_respones` as tuples
    in the format (method, *args) which represent a callback to fire, e.g.:

        (self._callbacks.log, [logging.DEBUG, 'This is a debug message.'])
        (self._callbacks.temp_update, [205, 108, 109])
    """

    def __init__(self, *args, **kwargs):
        # Temperature
        self._temp_target_bed = 0
        self._temp_target_nozzle1 = 0
        self._temp_target_nozzle2 = 0
        # Timing
        self._idle_loop_delay_sec = 0.1
        self._print_loop_delay_sec = 0.01
        self._temp_poll_execute_sec = 5
        self._temp_poll_ready_sec = 1
        self._temp_update_time = time.time() - self._temp_poll_ready_sec
        self._progress_update_sec = 5
        self._progress_update_time = time.time() - \
            self._progress_update_sec
        # Gcode
        self._gcode_sequence = []
        self._gcode_position = 0
        self._dummy_responses = []

        super().__init__(*args, **kwargs)

        # Some feedback to indicate that the Dummy printer is working.
        self._callbacks.log(logging.INFO, 'Connected to dummy printer.')

    def set_temp(self, bed=None, nozzle1=None, nozzle2=None):
        if bed:
            self._callbacks.log(logging.DEBUG,
                                'Setting bed temp: {0}'.format(bed))
            self._temp_target_bed = bed
        if nozzle1:
            self._callbacks.log(logging.DEBUG,
                                'Setting nozzle1 temp: {0}'.format(nozzle1))
            self._temp_target_nozzle1 = nozzle1
        if nozzle2:
            self._callbacks.log(logging.DEBUG,
                                'Setting nozzle2 temp: {0}'.format(nozzle2))
            self._temp_target_nozzle2 = nozzle2

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

    def unretract_filament(self, head=0, length=5, rate=300):
        if head not in [0, 1]:
            self._callbacks.log(logging.ERROR, 'Invalid head: ' + str(head))
            return
        self._callbacks.log(logging.DEBUG, 'Unretracting filament: '
                                           'head|{0}, length|{1}, rate|'
                                           '{2}'.format(head, length, rate))

    def retract_filament(self, head=0, length=5, rate=300):
        if head not in [0, 1]:
            self._callbacks.log(logging.ERROR, 'Invalid head: ' + str(head))
            return
        self._callbacks.log(logging.DEBUG, 'Retracting filament: '
                                           'head|{0}, length|{1}, rate|'
                                           '{2}'.format(head, length, rate))

    def set_extrude_override(self, percent):
        self._callbacks.log(logging.DEBUG, 'Extrude override set to '
                                           '{0} percent'.format(percent))
        self._callbacks.extrude_override_change(percent)

    def set_speed_override(self, percent):
        self._callbacks.log(logging.DEBUG, 'Movement speed override set to '
                                           '{0} percent'.format(percent))
        self._callbacks.speed_override_change(percent)

    def set_fan_speed(self, fan, percent):
        self._callbacks.log(logging.DEBUG, 'Setting speed of fan {0} to {1} '
                                           'percent'.format(fan, percent))
        self._callbacks.fan_speed_change(fan, percent)

    def enable_steppers(self):
        self._callbacks.log(logging.DEBUG, 'Steppers enabled')
        self._callbacks.steppers_update(True)

    def disable_steppers(self):
        self._callbacks.log(logging.DEBUG, 'Steppers disabled')
        self._callbacks.steppers_update(False)

    def execute_gcode(self, gcode_sequence):
        self._update_state(State.EXECUTING)
        self._gcode_sequence = gcode_sequence
        self._gcode_position = 0

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
        self._callbacks.log(logging.ERROR, 'Emergency stop')
        self._update_state(State.ERROR)

    def _reset_gcode_state(self):
        """
        Clear the current gcode sequence and return position to 0.
        """
        self._gcode_sequence = []
        self._gcode_position = 0

    def _request_printer_temperature(self):
        """
        Request a temperature update from the printer.
        """
        self._callbacks.log(logging.DEBUG, 'Sending temperature update.')
        self._callbacks.temp_update(
            random.randrange(100, 110),
            self._temp_target_bed,
            random.randrange(200, 210),
            self._temp_target_nozzle1,
            random.randrange(200, 210),
            self._temp_target_nozzle2,
        )

    def _reset_gcode_state(self):
        """
        Clear the current gcode sequence and return position to 0.
        """
        self._gcode_sequence = []
        self._gcode_position = 0


    def _execute_next_gcode_command(self):
        """
        Execute the next gcode command in the current sequence.
        """
        self._callbacks.log(logging.DEBUG, 'Executing gcode command {0} at '
            'position {1}'.format(self._gcode_sequence[self._gcode_position],
                                  self._gcode_position))
        self._gcode_position += 1
        # Complete execution if previous line was last in sequence.
        if self._gcode_position >= len(self._gcode_sequence):
            # Our last progress_update message probably didn't indicate
            # 100% complete. So send one last update to be sure.
            self._callbacks.progress_update(self._gcode_position,
                len(self._gcode_sequence))
            self._reset_gcode_state()
            self._update_state(State.READY)

    def run(self):
        """
        Printer run loop.
        """
        while True:
            # Ensure connected
            if self._state == State.DISCONNECTED:
                self._update_state(State.READY)
            # Process a message from the to_printer queue.
            if not self._to_printer.empty():
                message = json.loads(self._to_printer.get())
                try:
                    if 'method' and 'params' in message.keys():
                        getattr(self, message['method'])(**message['params'])
                except (KeyError, AttributeError):
                    self._callbacks.log(logging.ERROR,
                                        'Malformed message sent to '
                                        'printer: ' + str(message))
            # Report temperatures
            metric_interval = time.time() - self._temp_update_time
            if (self._state == State.EXECUTING and
                metric_interval > self._temp_poll_execute_sec):
                self._request_printer_temperature()
                self._temp_update_time = time.time()
            elif (self._state in [State.READY, State.PAUSED] and
                metric_interval > self._temp_poll_ready_sec):
                self._request_printer_temperature()
                self._temp_update_time = time.time()
            # Execute gcode if present.
            if (self._state == State.EXECUTING and
                len(self._gcode_sequence) > 0):
                self._execute_next_gcode_command()
                progress_interval = time.time() - self._progress_update_time
                if progress_interval > self._progress_update_sec:
                    self._callbacks.progress_update(self._gcode_position,
                        len(self._gcode_sequence))
                    self._progress_update_time = time.time()
            # Sleep before continuing. Delay determined by state.
            if (self._state == State.EXECUTING):
                time.sleep(self._print_loop_delay_sec)
            else:
                time.sleep(self._idle_loop_delay_sec)
