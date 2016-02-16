"""
OpenGB configuration.
"""

from tornado.options import define


# TODO: deploy a default config file via package manager and/or on startup.
CONFIG_FILE = "/etc/opengb/opengb.conf"


define('http_port', default=8000, help='Webserver http listen port')
define('debug', default=False, help='Run in debug mode')
define('db_file', default='/var/opengb/db/opengb.db', help='SQLite database')
define('gcode_dir', default='/var/opengb/gcode/', help='GCode directory')
define('printer', default='Dummy', help='Printer type')
define('baud_rate', default=115200, help='Printer baud rate')
define('serial_port', default=None,
       help='Printer serial port (use "None" for auto)')
define('frontend', default='opengb', help='Frontend (use "None" to disable)')
