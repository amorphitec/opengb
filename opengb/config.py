"""
Configuration defaults.
"""

from tornado.options import define


define('port', default=80, help='Webserver listening port')
define('debug', default=False, help='Run in debug mode.')
