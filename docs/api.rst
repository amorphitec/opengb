.. _api:

API
---

OpenGB functionality is exposed via a `JSON-RPC 2.0`_ API over HTTP using WebSockets.


Connecting
^^^^^^^^^^

The OpenGB web server exposes a WebSocket at `http://<hostname>:<port>/ws`.

To connect using Javascript::

    var socket = new WebSocket("ws://" + window.location.host + "/ws");
    socket.onmessage = function (message) {
      parseMessage(message)
    };


Message Types
^^^^^^^^^^^^^

In accordance with the `JSON-RPC 2.0 spec`_ there are two distinct message types used by the API. The payloads of both are encoded as JSON objects.

Method
======

The client sends a JSON-RPC 2.0 request to the server defining a method call and the server replies with a JSON-RPC 2.0 response.

Example request (setting target temperatures): ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "set_temp",
        "params": {
            "bed": 105,
            "nozzle1": 206,
            "nozzle2": 203
        }
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

Event
=====

The server sends an unsolicited JSON-RPC 2.0 message to the client defining an event which has occured.

Example event (temperature update): ::

    {
        "jsonrpc": "2.0",
        "event": "temp",
        "params": {
            "bed_current": 203,
            "bed_target": 105,
            "nozzle2_target": 203,
            "nozzle1_current": 104,
            "nozzle2_current": 108,
            "nozzle1_target": 206
        }
    }

Methods
^^^^^^^

The :class:`opengb.server.MessageHandler` class contains the methods exposed to JSON-RPC 2.0 clients.

set_temp
========

.. automethod:: opengb.server.MessageHandler.set_temp

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "set_temp",
        "params":{
            "bed": 105,
            "nozzle1": 206,
            "nozzle2": 203
        }
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

move_head_relative
==================

.. automethod:: opengb.server.MessageHandler.move_head_relative

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "move_head_relative",
        "params": {
            "x": 13.2,
            "y": -2,
            "z": 0.03
        }
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

move_head_absolute
==================

.. automethod:: opengb.server.MessageHandler.move_head_absolute

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "move_head_absolute",
        "params": {
            "x": 105,
            "y": 80,
            "z": 20
        }
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

home_head
=========

.. automethod:: opengb.server.MessageHandler.home_head

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "home_head",
        "params":{
            "x": true,
            "y": true,
            "z": false
        }
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

retract_filament
================

.. automethod:: opengb.server.MessageHandler.retract_filament

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "retract_filament",
        "params": {
            "head": 0,
            "length": 5,
            "rate": 300
        }
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

unretract_filament
==================

.. automethod:: opengb.server.MessageHandler.unretract_filament

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "unretract_filament",
        "params": {
            "head": 0,
            "length": 5,
            "rate": 300
        }
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

set_extrude_override
====================

.. automethod:: opengb.server.MessageHandler.set_extrude_override

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "set_extrude_override",
        "params": {
            "percent":120
        }
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

set_speed_override
==================

.. automethod:: opengb.server.MessageHandler.set_speed_override

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "set_speed_override",
        "params": {
            "percent":120
        }
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

set_fan_speed
=============

.. automethod:: opengb.server.MessageHandler.set_fan_speed

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "set_fan_speed",
        "params": {
            "fan": 1,
            "percent": 75
        }
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

filament_swap_begin
===================

.. automethod:: opengb.server.MessageHandler.filament_swap_begin

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "filament_swap_begin",
        "params": {}
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

filament_swap_complete
======================

.. automethod:: opengb.server.MessageHandler.filament_swap_complete

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "filament_swap_complete",
        "params": {}
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

enable_steppers
===============

.. automethod:: opengb.server.MessageHandler.enable_steppers

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "enable_steppers",
        "params": {}
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

disable_steppers
================

.. automethod:: opengb.server.MessageHandler.disable_steppers

Example request: ::

    { 
        "jsonrpc": "2.0",
        "id": 1,
        "method": "disable_steppers",
        "params": {}
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

print_gcode_file
================

.. automethod:: opengb.server.MessageHandler.print_gcode_file

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "print_gcode_file",
        "params": {
            "id": 1
        }
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }


pause_print
===============

.. automethod:: opengb.server.MessageHandler.pause_print

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "pause_print",
        "params":{}
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

resume_print
================

.. automethod:: opengb.server.MessageHandler.resume_print

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "resume_print",
        "params":{}
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

cancel_print
==============

.. automethod:: opengb.server.MessageHandler.cancel_print

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method":"cancel_print",
        "params": {}
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

emergency_stop
==============

.. automethod:: opengb.server.MessageHandler.emergency_stop

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "emergency_stop",
        "params": {}
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

put_gcode_file
==============

.. automethod:: opengb.server.MessageHandler.put_gcode_file

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "put_gcode_file",
        "params": {
            "name": "test_cube.gco",
            "payload": "<gcode>"
        }
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "id": 3,
            "name":"test_cube.gco"
        }
    }

get_gcode_file
==============

.. automethod:: opengb.server.MessageHandler.get_gcode_file

Example request: ::
 
    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "get_gcode_file",
        "params": {
            "id": 1
        }
    }
 
Example response: ::
 
    {
        "jsonrpc": "2.0",
        "result": {
            "size": 2914599,
            "id": 1,
            "name": "FE_Drakkar_Bow.gcode",
            "uploaded": "2016-04-11 19:54:31.929633"
        }
    }

get_gcode_files
===============

.. automethod:: opengb.server.MessageHandler.get_gcode_files

Example request: ::
 
    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "get_gcode_files",
        "params": {}
    }
 
Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "gcode_files": [
                {
                    "size": 2914599,
                    "id": 1,
                    "name": "FE_Drakkar_Bow.gcode"
                    "uploaded": "2016-04-11 19:54:31.929633"
                },
                {
                    "size": 24356,
                    "id": 2,
                    "name": "10mm_Test_Cube.gcode",
                    "uploaded": "2016-04-12 13:24:15.345623"
                }
            ]
        }
    }
 
delete_gcode_file
=================

.. automethod:: opengb.server.MessageHandler.delete_gcode_file

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "delete_gcode_file",
        "params": {
            "id": 3
        }
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 1,
        "result": true
    }

get_counters
============

.. automethod:: opengb.server.MessageHandler.get_counters

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "get_counters",
        "params":{}
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 2,
        "result":{
            "counters": {
                "nozzle_2_up_mins":128,
                "motor_x1_up_mins":128,
                "motor_x2_up_mins":128,
                "motor_y2_up_mins":128,
                "nozzle_1_up_mins":128,
                "motor_z2_up_mins":128,
                "motor_z1_up_mins":128,
                "printer_up_mins":128,
                "printer_print_mins":46,
                "bed_up_mins":128,
                "motor_y1_up_mins":128,
                "printer_up_mins_session":32
            }
        }
    }

get_filesystem_utilization
==========================

.. automethod:: opengb.server.MessageHandler.get_filesystem_utilization

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "get_filesystem_utilization",
        "params": {}
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 3,
        "result": {
            '/': {
                'free_bytes': 183485939712,
                'total_bytes': 243515678720,
                'utilized_bytes': 47636201472,
                'utilized_percent': 19.6
            },
            '/boot': {
                'free_bytes': 110014464,
                'total_bytes': 246755328,
                'utilized_bytes': 124001280,
                'utilized_percent': 50.3
            }
        }
    }

get_status
==========

.. automethod:: opengb.server.MessageHandler.get_status

Example request: ::

    {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "get_status",
        "params": {}
    }

Example response: ::

    {
        "jsonrpc": "2.0",
        "id": 4,
        "result": {
            "status": {
                "progress": {
                    "current": 0, 
                    "total": 0
                },
                "state": 20,
                "position": {
                    "z": 0,
                    "y": 0,
                    "x": 0
                }, 
                "temp": {
                    "bed_current": 100,
                    "nozzle2_target": 0,
                    "bed_target": 0,
                    "nozzle1_target": 0,
                    "nozzle2_current": 209,
                    "nozzle1_current": 205
                },
                "steppers": {
                    "enabled": true
                },
                "extrude_override": {
                    "percent": 100
                },
                "speed_override": {
                    "percent": 120"
                },
                "fan_speed":  {
                    0: 100,
                    1: 75,
                    2: 0
                }
            }
        }
    }

Events
^^^^^^

state_change
============

Sent when the printer status changes. Valid states are:

#. ``DISCONNECTED``
#. ``READY``
#. ``EXECUTING``
#. ``PAUSED``
#. ``FILAMENT_SWAP``
#. ``ERROR``

Example event: ::

    {
        "jsonrpc": "2.0", 
        "event": "state_change",
        "params": { 
            "old": "READY",
            "new": "EXECUTING"
        }
    }

extrude_override_change
=======================

Sent when the extrude override percentage changes.

Example event: ::

    {
        "jsonrpc": "2.0",
        "event": "extrude_override_change",
        "params": { 
            "percent": 120
        }
    }

speed_override_change
=====================

Sent when the movement speed override percentage changes.

Example event: ::

    {
        "jsonrpc": "2.0",
        "event": "speed_override_change",
        "params": { 
            "percent": 120
        }
    }

fan_speed_change
================

Sent when the speed of a fan changes.

Example event: ::

    {
        "jsonrpc": "2.0",
        "event": "fan_speed_change",
        "params": { 
            "fan": 1 
            "percent": 75
        }
    }

temp_update
===========

Sent periodically to provide current and target temperatures of printer components.

.. note::

    Not all parameters of every `temp_update` will necessarily contain values.
    If a parameter's value is `null` then the update does not contain any new
    data for that parameter and its value should be considered *unchanged*.

Example event: ::

    {
        "jsonrpc": "2.0",
        "event": "temp_update",
        "params": { 
            "bed_current": 205,
            "bed_target": 0,
            "nozzle1_current": 106,
            "nozzle1_target": 0,
            "nozzle2_current": 101,
            "nozzle2_target": 0
        }
    }

position_update
===============

Sent on print head movement to provide current print head position.

Example event: ::

    {
        "jsonrpc": "2.0",
        "event": "position_update",
        "params": {
            "x": 100,
            "y": 80,
            "z": 20
        }
    }

progress_update
===============

Sent periodically while printer is executing a gcode sequence.

Example event: ::

    {
        "jsonrpc": "2.0",
        "event": "progress_update",
        "params": { 
            "current_line": 327,
            "total_lines": 4393
        }
    }

steppers_update
===============

Sent when stepper motors are enabled/disabled.

Example event: ::

    {
        "jsonrpc": "2.0",
        "event": "steppers_update",
        "params": { 
            "enabled": true
        }
    }

.. _`JSON-RPC 2.0`: http://www.jsonrpc.org
.. _`JSON-RPC 2.0 spec`: http://www.jsonrpc.org/specification
