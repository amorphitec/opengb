"""
OpenGB server.

This is the core of openGB. It creates a printer object to run in a separate
process and communicates with it via queues.
"""

import os
import sys
import json
import multiprocessing
from pkg_resources import Requirement, resource_filename

import tornado.httpserver
import tornado.ioloop
import tornado.log
import tornado.websocket
from tornado.options import options
from tornado.web import Application, RequestHandler, StaticFileHandler
from jsonrpc import JSONRPCResponseManager, Dispatcher

import opengb.config
import opengb.printer
import opengb.database as OGD
import opengb.utils as OGU

# TODO: use rotated file logging.
LOGGER = tornado.log.app_log

# Websocket clients.
CLIENTS = []

# Local cache of printer state.
PRINTER = {
    'state':    opengb.printer.State.DISCONNECTED,
    'temp':     {
        'bed':      0,
        'nozzle1':  0,
        'nozzle2':  0,
    },
    'position': {
        'x':        0,
        'y':        0,
        'z':        0,
    },
    'progress': {
        'current':  0,
        'total':    0,
    },
    'steppers': {
        'enbabled': True,
    },
    'extrude_override': {
        'percent':  100,
    },
    'speed_override': {
        'percent':  100,
    },
    'fan_speed': {
        0:          100,
        1:          100,
        2:          100,
    },
}


class MessageHandler(object):
    """
    Handles JSON-RPC calls received via websocket.

    :param to_printer: A queue whose messages will be sent to the printer.
    :type to_printer: :class:`multiuprocessing.Queue`
    """

    def __init__(self, to_printer):
        self._to_printer = to_printer

    def set_temp(self, bed=None, nozzle1=None, nozzle2=None):
        """
        Set printer target temperatures.

        Unspecified target temperatures will remain unchanged.

        :param bed: Bed target temperature.
        :type bed: :class:`float`
        :param nozzle1: Nozzle1 target temperature.
        :type nozzle1: :class:`float`
        :param nozzle2: Nozzle2 target temperature.
        :type nozzle2: :class:`float`
        """
        self._to_printer.put(json.dumps({
            'method':   'set_temp',
            'params': {
                'bed':      bed,
                'nozzle1':  nozzle1,
                'nozzle2':  nozzle2,
            }
        }))
        return True

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
        self._to_printer.put(json.dumps({
            'method':   'move_head_relative',
            'params': {
                'x':    x,
                'y':    y,
                'z':    z,
            }
        }))
        return True

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
        self._to_printer.put(json.dumps({
            'method':   'move_head_absolute',
            'params': {
                'x':    x,
                'y':    y,
                'z':    z,
            }
        }))
        return True

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
        self._to_printer.put(json.dumps({
            'method':   'home_head',
            'params': {
                'x':    x,
                'y':    y,
                'z':    z,
            }
        }))
        return True

    def retract_filament(self, head, length, rate):
        """
        Retract filament into the print head.

        :param head: Print head to retract (0 or 1).
        :type head: :class:`int`
        :param length: Amount of filament to retract in mm.
        :type length: :class:`float`
        :param rate: Rate at which to retract in mm/s.
        :type rate: :class:`float`
        """
        if head not in [0, 1]:
            raise IndexError('Head must be either 0 or 1')
        self._to_printer.put(json.dumps({
            'method':   'retract_filament',
            'params': {
                'head':     head,
                'length':   length,
                'rate':     rate,
            }
        }))
        return True

    def unretract_filament(self, head, length, rate):
        """
        Unretract filament from the print head.

        :param head: Print head to unretract (0 or 1).
        :type head: :class:`int`
        :param length: Amount of filament to unretract in mm.
        :type length: :class:`float`
        :param rate: Rate at which to unretract in mm/s.
        :type rate: :class:`float`
        """
        if head not in [0, 1]:
            raise IndexError('Head must be either 0 or 1')
        self._to_printer.put(json.dumps({
            'method':   'unretract_filament',
            'params': {
                'head':     head,
                'length':   length,
                'rate':     rate,
            }
        }))
        return True

    def set_extrude_override(self, percent):
        """
        Set percentage override applied to extrusion commands.

        :param percent: Percentage by which extrusion should be overridden.
        :type percent: :class:`float`
        """
        if percent not in range(0,101):
            raise IndexError('Percent must be 0-100')
        self._to_printer.put(json.dumps({
            'method':   'set_extrude_override_percent',
            'params': {
                'percent':     percent,
            }
        }))
        return True

    def set_speed_override(self, percent):
        """
        Set speed percentage override applied to movement commands.

        :param percent: Percentage by which movement speed should be overridden.
        :type percent: :class:`float`
        """
        if percent not in range(0,101):
            raise IndexError('Percent must be 0-100')
        self._to_printer.put(json.dumps({
            'method':   'set_speed_override_percent',
            'params': {
                'percent':     percent,
            }
        }))
        return True

    def set_fan_speed(self, fan, percent):
        """
        Set fan speed.

        :param fan: Number of fan for which to set speed.
        :type fan: class:`int` (0-2)
        :param percent: Percentage of maximum speed to set.
        :type percent: :class:`float`
        """
        if fan not in range(0, 2):
            raise IndexError('Fan must be 0-2')
        if percent not in range(0,101):
            raise IndexError('Percent must be 0-100')
        self._to_printer.put(json.dumps({
            'method':   'set_fan_speed',
            'params': {
                'fan':         fan,
                'percent':     percent,
            }
        }))


    def enable_steppers(self):
        """
        Enable stepper motors.

        Prevents motors and axes from moving freely.
        """
        self._to_printer.put(json.dumps({
            'method':   'enable_steppers',
            'params': {}
        }))
        return True

    def disable_steppers(self):
        """
        Disable stepper motors.

        Allows motors and axes to moving freely.
        """
        self._to_printer.put(json.dumps({
            'method':   'disable_steppers',
            'params': {}
        }))
        return True

    def pause_print(self):
        """
        Pause the current print job.
        """
        self._to_printer.put(json.dumps({
            'method':   'pause_execution',
            'params': {}
        }))
        return True

    def resume_print(self):
        """
        Resume a paused print job.
        """
        self._to_printer.put(json.dumps({
            'method':   'resume_execution',
            'params': {}
        }))
        return True

    def cancel_print(self):
        """
        Cancel the current print job.

        The current print job status and position will be discarded.
        """
        self._to_printer.put(json.dumps({
            'method':   'stop_execution',
            'params': {}
        }))
        return True

    def emergency_stop(self):
        """
        Halt the printer immediately.

        .. note::

            Use only in emergencies as this will most likely lock the printer
            and require a reboot.
        """
        self._to_printer.put(json.dumps({
            'method':   'emergency_stop',
            'params': {}
        }))
        return True

    def put_gcode_file(self, payload, name, print_material='',
                       print_quality='', print_extruders='', print_time_sec=0,
                       print_filament_mm=0, print_material_gm=0,
                       thumbnail_png_base64=''):
        """
        Upload a gcode file.

        :param payload: Gcode file as ASCII text.
        :type payload: :class:`str`
        :param name: Gcode file name.
        :type name: :class:`str`
        :param print_material: Intended print material (e.g. "PLA").
        :type print_material: :class:`str`
        :param print_quality: Intended print quality (e.g. "High").
        :type print_quality: :class:`str`
        :param print_extruders: Extruders utilised (e.g. "Both").
        :type print_extruders: :class:`str`
        :param print_time_sec: Estimated print time in seconds.
        :type print_time_sec: :class:`int`
        :param print_filament_mm: Estimated print filament length in
            millimeters.
        :type print_filament_mm: :class:`int`
        :param print_material_gm: Estimated print material weight in grams.
        :type print_material_gm: :class:`int`
        :param thumbnail_png_base64: Thumbnail image.
        :type thumbnail_png_base64: :class:`str` representing a base64-encoded
            png file
        """

        # TODO: Validate gcode. Could use gctools for this if it is
        # ever uploaded to PyPI https://github.com/thegaragelab/gctools
        payload_bytes = payload.encode()
        payload_size = len(payload_bytes)
        gcode_file = OGD.GCodeFile.create(
            name=name,
            size=payload_size,
            print_material = print_material,
            print_quality = print_quality,
            print_extruders = print_extruders,
            print_time_sec = print_time_sec,
            print_filament_mm = print_filament_mm,
            print_material_gm = print_material_gm,
            thumbnail_png_base64 = thumbnail_png_base64,
        )
        destination = os.path.join(options.gcode_dir, str(gcode_file.id))
        with open(destination, "wb") as gcode_file_out:
            try:
                gcode_file_out.write(payload_bytes)
            except IOError as e:
                LOGGER.error('Error writing gcode file {0}: '
                             '{1}'.format(destination, e))
                raise IOError('Unable to save gcode file.')
        return {
            'id': gcode_file.id,
            'name': name,
            'size': payload_size,
            'print_material': print_material,
            'print_quality': print_quality,
            'print_extruders': print_extruders,
            'print_time_sec': print_time_sec,
            'print_filament_mm': print_filament_mm,
            'print_material_gm': print_material_gm,
            'thumbnail_png_base64': thumbnail_png_base64,
        }

    def get_gcode_file(self, id, content=False):
        """
        Get details of a single gcode file with the given `id`.

        Optionally include the gcode file content.

        :param id: ID of the gcode file to get.
        :type id: :class:`int`
        :param content: Include the gcode file content in the results.
        :type content: :class:`bool` (default False)
        """
        try:
            result = OGD.GCodeFile.get(OGD.GCodeFile.id == id)
            gcode_file = {
                'id':   result.id,
                'name': result.name,
                'size': result.size,
                'print_material': result.print_material,
                'print_quality': result.print_quality,
                'print_extruders': result.print_extruders,
                'print_time_sec': result.print_time_sec,
                'print_filament_mm': result.print_filament_mm,
                'print_material_gm': result.print_material_gm,
                'thumbnail_png_base64': result.thumbnail_png_base64,
            }
        except OGD.GCodeFile.DoesNotExist:
            raise IndexError('No gcode file found with id {0}'.format(id))
        if content:
            try:
                gcode_file['content'] = OGU.load_gcode_file(id)
            except IOError as err:
                LOGGER.error('Error reading gcode file with id {0}: '
                             '{1}'.format(id, err))
                raise IndexError('Error reading gcode file with '
                                 'id {0}'.format(id))
        return gcode_file

    def get_gcode_files(self):
        """
        Get details of all gcode files.
        """
        return {'gcode_files': [
            {
                'id': g.id,
                'name': g.name,
                'size': g.size,
                'print_material': g.print_material,
                'print_quality': g.print_quality,
                'print_extruders': g.print_extruders,
                'print_time_sec': g.print_time_sec,
                'print_filament_mm': g.print_filament_mm,
                'print_material_gm': g.print_material_gm,
                'thumbnail_png_base64': g.thumbnail_png_base64,
            }
            for g in OGD.GCodeFile.select()]}

    def delete_gcode_file(self, id):
        """
        Delete a single gcode file with the given `id`.

        :param id: ID of the gcode file to delete.
        :type id: :class:`int`
        """
        try:
            OGU.delete_gcode_file(id)
        except IOError as err:
            LOGGER.error('Error deleting gcode file with id {0}: '
                         '{1}'.format(id, err))
            raise IndexError('Error deleting gcode file with '
                             'id {0}'.format(id)) from None
        return True

    def print_gcode_file(self, id):
        """
        Print gcode file with given `id`.

        :param id: ID of the gcode file to get.
        :type id: :class:`int`
        """
        if PRINTER['state'] != opengb.printer.State.READY:
            raise IndexError('Printer not ready')
        try:
            OGD.GCodeFile.get(OGD.GCodeFile.id == id)
        except OGD.GCodeFile.DoesNotExist:
            raise IndexError('No gcode file found with id {0}'.format(id))
        try:
            gcode = OGU.prepare_gcode(OGU.load_gcode_file(id))
        except IOError as err:
            LOGGER.error('Error reading gcode file with id {0}: '
                         '{1}'.format(id, err))
            raise IndexError('Error reading gcode file with '
                             'id {0}'.format(id))
        self._to_printer.put(json.dumps({
            'method':   'execute_gcode',
            'params': {
                'gcode_sequence':    gcode,
            }
        }))
        return True

    def get_status(self):
        """
        Get current printer status.

        .. note::

            This method should only be used to determine baseline printer
            status. To maintain a view of current printer status listen for
            the various `jsonrpc` events.
        """
        # Enums don't serialise so replace with name.
        printer = PRINTER.copy()
        printer['state'] = printer['state'].name
        return {'status': printer}

    def get_counters(self):
        """
        Get printer counter values.

        Counters are listed in :data:`opengb.database.COUNTERS`.
        """
        return {'counters': {c.name: c.count for c in OGD.Counter.select()}}


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    """
    Handles all websocket communication with clients.

    Uses `json-rpc <https://pypi.python.org/pypi/json-rpc/>`_ to map messages
    to methods and generate valid JSON-RPC 2.0 responses.
    """

    def __init__(self, *args, **kwargs):
        message_handler = MessageHandler(kwargs.pop('to_printer'))
        self.dispatcher = Dispatcher(message_handler)
        super().__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True

    def open(self):
        LOGGER.info('New connection from {0}'.format(self.request.remote_ip))
        CLIENTS.append(self)

    def on_close(self):
        LOGGER.info('Connection closed to {0}'.format(self.request.remote_ip))
        CLIENTS.remove(self)

    def on_message(self, message):
        """
        Passes an incoming JSON-RPC message to the dispatcher for processing.
        """
        LOGGER.debug('Message received from {0}: {1}'.format(
            self.request.remote_ip, message[:75]))
        response = JSONRPCResponseManager.handle(message, self.dispatcher)
        LOGGER.debug('Sending response to {0}: {1}'.format(
            self.request.remote_ip, str(response._data)[:75]))
        self.write_message(response.json)


class StatusHandler(RequestHandler):
    def get(self):
        self.write(json.dumps(PRINTER, cls=opengb.printer.StateEncoder))
        self.set_header("Content-Type", "application/json")


def broadcast_message(message):
    """
    Broadcast message to websocket clients.
    """
    for each in CLIENTS:
        each.write_message(message)


def process_event(event):
    """
    Process an event from the printer.
    """
    global PRINTER
    try:
        if event['event'] == 'state_change':
            # TODO: if state changes from printing to ready, reset progress.
            PRINTER['state'] = opengb.printer.State[event['params']['new']]
        elif event['event'] == 'extrude_override_change':
            PRINTER['extrude_override'] = event['params']
        elif event['event'] == 'speed_override_change':
            PRINTER['speed_override'] = event['params']
        elif event['event'] == 'fan_speed_change':
            PRINTER['fan_speed'][event['params']['fan']] = event['params']['percent']
        elif event['event'] == 'temp_update':
            PRINTER['temp'] = event['params']
        elif event['event'] == 'position_update':
            PRINTER['position'] = event['params']
        elif event['event'] == 'progress_update':
            PRINTER['progress'] = event['params']
        elif event['event'] == 'steppers_update':
            PRINTER['steppers'] = event['params']
        elif event['event'] == 'z_change':
            # TODO: trigger update camera image.
            pass
    except KeyError:
        LOGGER.error('Malformed event from printer: {0}'.format(event))


def process_printer_events(from_printer):
    """
    Process events from printer.

    Runs via a :class:`tornado.ioloop.PeriodicCallback`.

    :param from_printer: A queue which will be populated with messages sent
        from the printer.
    :type from_printer: :class:`multiuprocessing.Queue`
    """
    if not from_printer.empty():
        try:
            event = json.loads(from_printer.get())
            if event['event'] == 'log':
                LOGGER.log(event['params']['level'], event['params']['msg'])
            else:
                broadcast_message(event)
                process_event(event)
        except TypeError as e:
            LOGGER.exception(e)


def update_counters(count=1):
    """
    Increment all printer counters.

    Runs via a :class:`tornado.ioloop.PeriodicCallback`.

    :param count: Value by which to increment counters.
    :type count: :class:`int`
    """
    LOGGER.debug('Incrementing printer counters')
    query = OGD.Counter.update(count=OGD.Counter.count+1).where(
        OGD.Counter.name.contains('uptime'))
    query.execute()


def get_frontend_handlers(frontend_name):
    """
    Return handlers for frontend with the given name.

    Returns an empty list if running backend-only and no frontend is defined.

    NOTE: Currently each frontend dir must conform to a specific layout:

        frontend_name
            /static
            index.html

    :param frontend_name: Name of frontend whose handlers to return.
    :type frontend_name: :class:`str`
    :returns: A list of handlers for the frontend with the given name.
    :rtype: :class:`iterable` of :class:`tornado.web.RequestHandler`
    :raises `IOError` if no frontend exists with `frontend_name`.
    """
    if frontend_name == 'None':
        return []
    install_dir = resource_filename(Requirement.parse('openGB'), 'opengb')
    frontend_dir = os.path.join(install_dir, 'frontend', frontend_name)
    if not os.path.isdir(frontend_dir):
        raise IOError('Frontend dir not found: {0}.'.format(frontend_dir))
    return [
        (r"/static/(.*)", StaticFileHandler,
            {"path": os.path.join(frontend_dir, "static")}),
        (r"/(.*)", StaticFileHandler,
            {"path": os.path.join(frontend_dir, "index.html")}),
    ]


def main():
    # Load config.
    options.parse_config_file(opengb.config.CONFIG_FILE)

    # Initialize database.
    OGD.initialize(options.db_file)

    # Initialize printer queues.
    to_printer = multiprocessing.Queue()
    from_printer = multiprocessing.Queue()

    # Initialize printer using queue callbacks.
    printer_callbacks = opengb.printer.QueuedPrinterCallbacks(from_printer)
    printer_type = getattr(opengb.printer, options.printer)
    printer = printer_type(to_printer, printer_callbacks,
                           baud_rate=options.baud_rate,
                           port=options.serial_port)
    printer.daemon = True
    printer.start()

    # Initialize web server.
    # Backend handler is always required.
    handlers = [(r"/ws", WebSocketHandler, {"to_printer": to_printer})]
    # Frontend-specfic handlers added if required.
    try:
        handlers += get_frontend_handlers(options.frontend)
    except IOError as e:
        LOGGER.exception(e)
        LOGGER.warn('No frontend will be served.')
    app = Application(handlers=handlers, debug=options.debug)
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.http_port)

    # Create event loop and periodic callbacks
    main_loop = tornado.ioloop.IOLoop.instance()
    printer_event_processor = tornado.ioloop.PeriodicCallback(
        lambda: process_printer_events(from_printer), 10, io_loop=main_loop)
    counter_updater = tornado.ioloop.PeriodicCallback(
        lambda: update_counters(), 60000)
    # TODO: ioloop for watchdog
    # TODO: ioloop for camera

    # Rock and roll.
    printer_event_processor.start()
    counter_updater.start()
    main_loop.start()

    return(os.EX_OK)

if __name__ == '__main__':
    sys.exit(main())
