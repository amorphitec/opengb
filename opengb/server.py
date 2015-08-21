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

import tornado.httpserver
import tornado.ioloop
import tornado.websocket
import tornado.log
from tornado.options import options
from tornado.web import Application, RequestHandler, StaticFileHandler

import opengb.config
import opengb.printer
import opengb.database


LOGGER = tornado.log.app_log
# TODO: use rotated file logging.

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


class StatusHandler(RequestHandler):
    def get(self):
        self.write(json.dumps(PRINTER, cls=opengb.printer.StateEncoder))
        self.set_header("Content-Type", "application/json") 


def broadcast_message(message):
    """
    Broadcast message to websocket clients.
    """
    # TODO: implement
    pass


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
    handlers = [
        (r"/api/status", StatusHandler),
        (r"/fonts/(.*)", StaticFileHandler, {"path": "static/fonts"}),
        (r"/img/(.*)", StaticFileHandler, {"path": "static/img"}),
        (r"/js/(.*)", StaticFileHandler, {"path": "static/js"}),
        (r"/css/(.*)", StaticFileHandler, {"path": "static/css"}),
        (r"/(.*)", StaticFileHandler, {"path": "static/index.html"}),
        #TODO: (r"/ws", WebSocketHandler),
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
