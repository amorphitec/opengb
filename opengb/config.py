"""
OpenGB configuration.
"""

from tornado.options import define


# TODO: deploy a default config file via package manager and/or on startup.
CONFIG_FILE = "/etc/opengb/opengb.conf"


define('port', default=80, help='Webserver listening port')
define('debug', default=False, help='Run in debug mode.')
define('printer', default='Dummy', help='Printer type')
define('db_file', default='/var/opengb/opengb.db', help='SQLite')
