"""
OpenGB server.

This is the core of openGB. It creates a printer object to run in a separate
process and communicates with it via queues.
"""

import os
import sys
import json
import logging
import multiprocessing
from pkg_resources import Requirement, resource_filename

import tornado.httpserver
import tornado.ioloop
import tornado.log
import tornado.websocket
from tornado.options import options
from tornado.web import Application, RequestHandler, StaticFileHandler

import opengb.config
import opengb.printer
import opengb.database


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
    'progress': {
        'current':  0,
        'total':    0,
    },
}


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        LOGGER.info('New connection from {0}'.format(self.request.remote_ip))
        CLIENTS.append(self)
        self.write_message(json.dumps(
            {'cmd': 'STATE', 'new': PRINTER['state']},
            cls=opengb.printer.StateEncoder))
 
    def on_message(self, message):
        LOGGER.debug('Message received from {0}: {1)'.format(
            message ,self.request.remote_ip))
        # TODO: Parse incoming control/print messages and send to Printer
 
    def on_close(self):
        LOGGER.info('Connection closed to {0}'.format(self.request.remote_ip))
        CLIENTS.remove(self)


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


def process_message(message):
    """
    Process a message from the printer.
    """
    broadcast_message(message)
    global PRINTER
    try:
        cmd = message.pop('cmd')
        if cmd == 'STATE':
            # TODO: if state changes from printing to ready, reset progress.
            PRINTER['state'] = opengb.printer.State(message['new'])
        elif cmd == 'TEMP':
            PRINTER['temp'] = message
        elif cmd  == 'PROGRESS':
            PRINTER['progress'] = message
        elif cmd == 'ZCHANGE':
            # TODO: trigger update camera image. 
            pass
    except KeyError as e:
        LOGGER.error('Malformed message from printer: {0}'.format(message))


def process_printer_messages(from_printer):
    """
    Process messages from printer.

    Runs via a :class:`tornado.ioloop.PeriodicCallback`.

    :param from_printer: Queue containing messages from the printer.
    :type from_printer: :class:`multiprocessing.Queue`
    """
    if not from_printer.empty():
        try:
            message = json.loads(from_printer.get())
            if message['cmd'] == 'LOG':
                LOGGER.log(message['level'], message['msg'])
            else:
                broadcast_message(message)
                process_message(message)
        except TypeError as e:
            LOGGER.exception(e)


def main():
    # Load config.
    options.parse_config_file(opengb.config.CONFIG_FILE)

    # Initialise database.
    opengb.database.initialize(options.db_file)

    # Initialise queues.
    to_printer = multiprocessing.Queue()
    from_printer = multiprocessing.Queue()

    # Initialize printer using queue callbacks.
    printer_callbacks = opengb.printer.QueuedPrinterCallbacks(from_printer)
    printer_type = getattr(opengb.printer, options.printer)
    printer = printer_type(to_printer, printer_callbacks)
    printer.daemon = True
    printer.start()

    # Initialize web server.
    install_dir = resource_filename(Requirement.parse('openGB'), 'opengb')
    static_dir = os.path.join(install_dir, 'static')
    handlers = [
        (r"/ws", WebSocketHandler),
        (r"/api/status", StatusHandler),
        (r"/fonts/(.*)", StaticFileHandler, {"path": os.path.join(static_dir, "fonts")}),
        (r"/img/(.*)", StaticFileHandler, {"path": os.path.join(static_dir, "img")}),
        (r"/js/(.*)", StaticFileHandler, {"path": os.path.join(static_dir, "js")}),
        (r"/css/(.*)", StaticFileHandler, {"path": os.path.join(static_dir, "css")}),
        (r"/(.*)", StaticFileHandler, {"path": os.path.join(static_dir, "index.html")}),
    ]
    app = Application(handlers=handlers, debug=options.debug)
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port)

    # Rock and roll.
    main_loop = tornado.ioloop.IOLoop.instance()
    printer_msg_processor = tornado.ioloop.PeriodicCallback(
        lambda: process_printer_messages(from_printer), 10, io_loop=main_loop)
    # TODO: ioloop for watchdog
    # TODO: ioloop for camera
    printer_msg_processor.start()
    main_loop.start()

    return(os.EX_OK)

if __name__ == '__main__':
    sys.exit(main())
