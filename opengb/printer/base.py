"""
Printer exceptions and interface.
"""

import multiprocessing
import abc
import json
import enum


class NotReadyException(Exception):
    """
    Raised then printer is unable to perform an action due to it not being in a
    `READY `:class:`State`'
    """
    pass


class State(enum.Enum):
    """
    Printer state.
    """

    DISCONNECTED = 10
    READY = 20
    EXECUTING = 30
    PAUSED = 40
    FILAMENT_SWAP = 50
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
    occur.

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

    def extrude_override_change(self, percent): 
        """
        Publish an extrude override percentage change event.

        :param percent: Percentage by which extrusion will be overridden. 
        :type percent: :class:`float`
        """
        pass

    def speed_override_change(self, percent):
        """
        Publish an extrude override percentage change event.

        :param percent: Percentage by which movement speed will be overridden.
        :type percent: :class:`float`
        """
        pass

    def fan_speed_change(self, fan, percent):
        """
        Publish a fan speed change event.

        :param fan: Number of fan for which speed was set.
        :type fan: class:`int` (0-2)
        :param percent: Percentage of maximum speed to which fan was set.
        :type percent: :class:`float`
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

    def position_update(self, x, y, z):
        """
        Publish a position update event.

        :param x: Print head absolute X position.
        :type x: :class:`float`
        :param y: Print head absolute Y position.
        :type y: :class:`float`
        :param z: Print head absolute Z position.
        :type z: :class:`float`
        """
        pass

    def progress_update(self, current_line, total_lines):
        """
        Publish an execution progress update event.

        :param current_line: Line number currently being executed.
        :type current_line: :class:`int`
        :param total_lines: Total number of lines to be executed.
        :type total_lines: :class:`int`
        """
        pass

    def steppers_update(self, enabled):
        """
        Publish a stepper motors update event.

        :param enabled: Whether or not stepper motors are enabled.
        :type enabled: :class:`bool`
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
    Printer callbacks that place
    `JSON-RPC 2.0 <http://www.jsonrpc.org/specification>`_ event objects on a
    :class:`multiprocessing.Queue`. E.g.

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
            'event':   'state_change',
            'params':   {
                'old':      old.name,
                'new':      new.name,
            }
        })

    def speed_override_change(self, percent):
     self._publish({
            'event':   'speed_override_change',
            'params':   {
                'percent':      percent,
            }
        })

    def extrude_override_change(self, percent):
     self._publish({
            'event':   'extrude_override_change',
            'params':   {
                'percent':      percent,
            }
        })

    def fan_speed_change(self, fan, percent):
        self._publish({
            'event':   'fan_speed_change',
            'params':   {
                'fan':          fan,
                'percent':      percent,
            }
        })

    def temp_update(self, bed_current, bed_target, nozzle1_current,
                    nozzle1_target, nozzle2_current, nozzle2_target):
        self._publish({
            'event':   'temp_update',
            'params':   {
                'bed_current':      bed_current,
                'bed_target':       bed_target,
                'nozzle1_current':  nozzle1_current,
                'nozzle1_target':   nozzle1_target,
                'nozzle2_current':  nozzle2_current,
                'nozzle2_target':   nozzle2_target,
            }
        })

    def position_update(self, x, y, z):
        self._publish({
            'event':   'position_update',
            'params':   {
                'x':      x,
                'y':      y,
                'z':      z,
            }
        })

    def progress_update(self, current_line, total_lines):
        self._publish({
            'event':   'progress_update',
            'params':   {
                'current_line': current_line,
                'total_lines':  total_lines,
            }
        })

    def steppers_update(self, enabled):
        self._publish({
            'event':   'steppers_update',
            'params':   {
                'enabled':      enabled,
            }
        })

    def z_change(self, position):
        self._publish({
            'event':  'z_change',
            'position':  position,
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

    def __init__(self, to_printer, printer_callbacks=None, baud_rate=None,
                 port=None):
        # Configuration.
        self._state = State.DISCONNECTED
        # Print queue.
        self._to_printer = to_printer
        # Callbacks.
        if printer_callbacks is None:
            self._callbacks = PrinterCallbacks()
        else:
            self._callbacks = printer_callbacks
        super().__init__()

    def _update_state(self, new_state):

        """
        Update printer state.

        :param new_state: New printer state.
        :type new_state: :class:`State`
        """
        old_state = self._state
        self._state = new_state
        if old_state != new_state:
            self._callbacks.state_change(old_state, new_state)

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

    @abc.abstractmethod
    def move_head_relative(self, x=0, y=0, z=0):
        """
        Move the print head along one or more axes relative to the current
        position.

        :param x: Millimeters to move along the X axis.
        :type x: :class:`float`
        :param y: Millimeters to move along the Y axis.
        :type y: :class:`float`
        :param z: Millimeters to move along the Z axis.
        :type z: :class:`float`
        """
        pass

    @abc.abstractmethod
    def move_head_absolute(self, x=0, y=0, z=0):
        """
        Move the print head along one or more axes to an absolute position.

        :param x: Position to move to along the X axis.
        :type x: :class:`float`
        :param y: Position to move to along the Y axis.
        :type y: :class:`float`
        :param z: Position to move to along the Z axis.
        :type z: :class:`float`
        """
        pass

    @abc.abstractmethod
    def home_head(self, x=True, y=True, z=True):
        """
        Home the print head along one or more axes.

        :param x: Whether or not to home the X axis.
        :type x: :class:`bool`
        :param y: Whether or not to home the Y axis.
        :type y: :class:`bool`
        :param z: Whether or not to home the Z axis.
        :type z: :class:`bool`
        """
        pass

    @abc.abstractmethod
    def retract_filament(self, head=0, length=0, rate=0):
        """
        Retract filament into the print head.

        :param head: Print head to retract (0 or 1).
        :type head: :class:`int`
        :param length: Amount of filament to retract in mm.
        :type length: :class:`float`
        :param rate: Rate at which to retract in mm/s.
        :type rate: :class:`float`
        """
        pass

    @abc.abstractmethod
    def unretract_filament(self, head=0, length=0, rate=0):
        """
        Unretract filament from the print head.

        :param head: Print head to unretract (0 or 1).
        :type head: :class:`int`
        :param length: Amount of filament to unretract in mm.
        :type length: :class:`float`
        :param rate: Rate at which to unretract in mm/s.
        :type rate: :class:`float`
        """
        pass

    @abc.abstractmethod
    def set_extrude_override(self, percent):
        """
        Set percentage override applied to extrusion commands.

        :param percent: Percentage by which extrusion should be overridden.
        :type percent: :class:`float`
        """
        pass

    @abc.abstractmethod
    def set_speed_override(self, percent):
        """
        Set speed percentage override applied to movement commands.

        :param percent: Percentage by which movement speed should be overridden.
        :type percent: :class:`float`
        """
        pass

    @abc.abstractmethod
    def filament_swap_begin(self):
        """
        Begin filament swap procedure.

        ..note::

            This doesn't sit neatly within the paradigm used by the various
            other printer methods. This is due to the Marlin functionality
            upon which it is based being somewhat unusual.

            Ultimately all aspects of automated filament swap should be
            implemented in OpenGB using generic gcode commands to ensure
            consistency. But for now we are leveraging what Marlin provides for
            free.
        """
        pass

    @abc.abstractmethod
    def filament_swap_complete(self):
        """
        Begin filament swap procedure.

        See note in :meth:`filament swap_begin`.
        """
        pass

    @abc.abstractmethod
    def set_fan_speed(self, fan, percent):
        """
        Set fan speed.

        :param fan: Number of fan for which to set speed.
        :type fan: class:`int` (0-2)
        :param percent: Percentage of maximum speed to set.
        :type percent: :class:`float`
        """
        pass

    @abc.abstractmethod
    def enable_steppers(self):
        """
        Enable stepper motors.

        Prevents motors and axes from moving freely.
        """
        pass

    @abc.abstractmethod
    def disable_steppers(self):
        """
        Enable stepper motors.

        Prevents motors and axes from moving freely.
        """
        pass

    @abc.abstractmethod
    def execute_gcode(self, gcode_commands):
        """
        Execute a sequence of gcode commands.

        Sequences may represent prints, bed levelling scripts etc.

        .. note::

            This method should set `self._state` to `EXECUTING` to ensure
            that commands are executed with limited interruptions.

        :param gcode_commands: A sequence of gcode commands to be executed.
        :type gcode_commands: :class:`iterable` of :class:`str`
        """
        pass

    @abc.abstractmethod
    def pause_execution(self):
        """
        Pause execution of a sequence of gcode commands.

        .. note::

            This method should set `self._state` to `PAUSED` to ensure
            that commands are executed with limited interruptions.
        """
        pass

    @abc.abstractmethod
    def resume_execution(self):
        """
        Resume paused execution of a sequence of gcode commands.
        """
        pass

    @abc.abstractmethod
    def stop_execution(self):
        """
        Stop execution of a sequence of gcode commands.

        The current gcode sequence and position will be forgotten.
        """
        pass

    @abc.abstractmethod
    def emergency_stop(self):
        """
        Immediately stop the printer.
        """
        pass
