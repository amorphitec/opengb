"""
OpenGB server.

This is the core of openGB. It creates a printer object to run in a separate
process and communicates with it via queues.
"""

import os
import sys
import json
import multiprocessing

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import options

import opengb.config
import opengb.printer


# Local cache of printer state.
# TODO: store this in the DB somewhere?
PRINTER = {
    'state':    opengb.printer.States.INITIALIZING,
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


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        # TODO: make this return the web app from /static
        self.write('Hello world!')


class StatusHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('printer state:' + PRINTER['state'].name)


def process_message(message):
    """
    Process a message from the printer.
    """
    # Store printer status in local cache for JSON API calls.
    global PRINTER
    if message['cmd'] == 'STATE':
        # TODO: if state changes from printing to ready, reset progress.
        PRINTER['state'] = opengb.printer.States(message['new'])
    elif message['cmd'] == 'TEMP':
        PRINTER['temp']['bed'] = message['bed']
        PRINTER['temp']['nozzle1'] = message['nozzle1']
        PRINTER['temp']['nozzle1'] = message['nozzle2']
    elif message['cmd'] == 'PROGRESS':
        PRINTER['progress']['current'] = message['current']
        PRINTER['progress']['total'] = message['total']
    elif message['cmd'] == 'ZCHANGE':
        # TODO: trigger update camera image. 
        pass
    #TODO: for each in clients: each.write_message(message)


def process_printer_messages(from_printer):
    if not from_printer.empty():
        try:
            message = json.loads(from_printer.get())
            if message['cmd'] == 'LOG':
                # TODO: log the message
                pass
            else:
                process_message(message)
        except TypeError:
            #TODO: debug log this
            pass


def main():

    # TODO: handle this file not being present
    # TODO: include a sample config file to be deployed via a package
    #       manager or optionally on startup
    options.parse_config_file("/etc/opengb/opengb.conf")

    # Initialise queues.
    to_printer = multiprocessing.Queue()
    from_printer = multiprocessing.Queue()

    # Initialize printer using queued callbacks.
    printer_callbacks = opengb.printer.QueuedPrinterCallbacks(from_printer)
    printer = opengb.printer.Marlin(to_printer, printer_callbacks)
    printer.daemon = True
    printer.start()

    # Initialize web server.
    app = tornado.web.Application(
        handlers=[
            (r"/", IndexHandler),
            (r"/api/status", StatusHandler),
            #(r"/ws", WebSocketHandler),
        ],
        debug=options.debug,
    )
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
