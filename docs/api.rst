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

    {"jsonrpc":"2.0","id":1,"method":"set_temp","params":{"bed":105,"nozzle1":206,"nozzle2":203}}

Example response: ::

    {"jsonrpc":"2.0","id":1 "result":true}

Event
=====

The server sends an unsolicited JSON-RPC 2.0 message to the client defining an event which has occured.

Example event (temperature update): ::

    {"event":"temp","jsonrpc":"2.0","params":{"bed_current":203,"bed_target":105,"nozzle2_target":203,"nozzle1_current":104,"nozzle2_current":108,"nozzle1_target":206}}

Methods
^^^^^^^

The :class:`opengb.server.MessageHandler` class contains the methods exposed to JSON-RPC 2.0 clients.

set_temp
========

.. automethod:: opengb.server.MessageHandler.set_temp

Example request: ::

    {"jsonrpc":"2.0","id":1,"method":"set_temp","params":{"bed":105,"nozzle1":206,"nozzle2":203}}

Example response: ::

    {"jsonrpc":"2.0","id":1,"result":true}

move_head_relative
==================

.. automethod:: opengb.server.MessageHandler.move_head_relative

Example request: ::

    {"jsonrpc":"2.0","id":1,"method":"move_head_relative","params":{"x":13.2,"y":-2,"z":0.03}}

Example response: ::

    {"jsonrpc":"2.0","id":1,"result":true}

move_head_absolute
==================

.. automethod:: opengb.server.MessageHandler.move_head_absolute

Example request: ::

    {"jsonrpc":"2.0","id":1,"method":"move_head_absolute","params":{"x":105,"y":80,"z":20}}

Example response: ::

    {"jsonrpc":"2.0","id":1,"result":true}

home_head
=========

.. automethod:: opengb.server.MessageHandler.home_head

Example request: ::

    {"jsonrpc":"2.0","id":1,"method":"home_head","params":{"x":true,"y":true,"z":false}}

Example response: ::

    {"jsonrpc":"2.0","id":1,"result":true}

retract_filament
================

.. automethod:: opengb.server.MessageHandler.retract_filament

Example request: ::

    {"jsonrpc":"2.0","id":1,"method":"retract_filament","params":{"head":0,"length":5,"rate":300}}

Example response: ::

    {"jsonrpc":"2.0","id":1,"result":true}

unretract_filament
================

.. automethod:: opengb.server.MessageHandler.unretract_filament

Example request: ::

    {"jsonrpc":"2.0","id":1,"method":"unretract_filament","params":{"head":0,"length":5,"rate":300}}

Example response: ::

    {"jsonrpc":"2.0","id":1,"result":true}

print_gcode_file
================

.. automethod:: opengb.server.MessageHandler.print_gcode_file

Example request: ::

    {"jsonrpc":"2.0","id":1,"method":"print_gcode_file","params":{"id":1}}

Example response: ::

    {"jsonrpc":"2.0","id":1,"result":true}


pause_print
===============

.. automethod:: opengb.server.MessageHandler.pause_print

Example request: ::

    {"jsonrpc":"2.0","id":1,"method":"pause_print","params":{}}

Example response: ::

    {"jsonrpc":"2.0","id":1,"result":true}

resume_print
================

.. automethod:: opengb.server.MessageHandler.resume_print

Example request: ::

    {"jsonrpc":"2.0","id":1,"method":"resume_print","params":{}}

Example response: ::

    {"jsonrpc":"2.0","id":1,"result":true}

cancel_print
==============

.. automethod:: opengb.server.MessageHandler.cancel_print

Example request: ::

    {"jsonrpc":"2.0","id":1,"method":"cancel_print","params":{}}

Example response: ::

    {"jsonrpc":"2.0","id":1,"result":true}

emergency_stop
==============

.. automethod:: opengb.server.MessageHandler.emergency_stop

Example request: ::

    {"jsonrpc":"2.0","id":1,"method":"emergency_stop","params":{}}

Example response: ::

    {"jsonrpc":"2.0","id":1,"result":true}

put_gcode_file
==============

.. automethod:: opengb.server.MessageHandler.put_gcode_file

Example request: ::

    {"jsonrpc":"2.0","id":1,"method":"put_gcode_file","params":{"name":"test_cube.gco","payload":<gcode>}}

Example response: ::

    {"jsonrpc":"2.0","id":1,"result":{"id":3,"name":"test_cube.gco"}}

get_gcode_file
==============

.. automethod:: opengb.server.MessageHandler.get_gcode_file

Example request: ::
 
    {"jsonrpc":"2.0","id":1,"method":"get_gcode_file","params":{"id": 1}}
 
Example response: ::
 
    {"id": 1, "jsonrpc": "2.0", "result": {"size": 2914599, "id": 1, "name": "FE_Drakkar_Bow.gcode"}}

get_gcode_files
===============

.. automethod:: opengb.server.MessageHandler.get_gcode_files

Example request: ::
 
    {"jsonrpc":"2.0","id":1,"method":"get_gcode_files","params":{}
 
Example response: ::

    {"jsonrpc": "2.0", "id": 1, "result": {"gcode_files": [{"size": 2914599, "id": 1, "name": "FE_Drakkar_Bow.gcode"}, {"size": 24356, "id": 2, "name": "10mm_Test_Cube.gcode"}]}} 
 
get_counters
============

.. automethod:: opengb.server.MessageHandler.get_counters

Example request: ::

    {"jsonrpc":"2.0","id":2,"method":"get_counters","params":{}}

Example response: ::

    {"jsonrpc":"2.0","id":2,"result":{"counters":{"nozzle_2_up_mins":128,"motor_x1_up_mins":128,"motor_x2_up_mins":128 "motor_y2_up_mins":128,"nozzle_1_up_mins":128,"motor_z2_up_mins":128,"motor_z1_up_mins":128,"printer_up_mins":128,"printer_print_mins":46,"bed_up_mins":128,"motor_y1_up_mins":128,"printer_up_mins_session":32}}}

Events
^^^^^^

state_change
============

Sent when the printer status changes. Valid states are:

#. ``DISCONNECTED``
#. ``READY``
#. ``EXECUTING``
#. ``PAUSED``
#. ``ERROR``

Example event: ::

    {"jsonrpc": "2.0", "event": "state_change", "params": { "old": "READY", "new": "EXECUTING"}}

temp_update
===========

Sent periodically to provide current and target temperatures of printer components.

Example event: ::

    {"jsonrpc": "2.0", "event": "temp_update", "params": { "bed_current": 205, "bed_target": 0, " "nozzle1_current": 106, nozzle1_target": 0, "nozzle2_current": 101, "nozzle2_target": 0}}


position_update
===============

Sent on print head movement to provide current print head position.

Example event: ::

    {"jsonrpc": "2.0", "event": "position_update", "params": { "x": 100, "y": 80, "z": 20}}


progress_update
===============

Sent periodically while printer is executing a gcode sequence.

Example event: ::

    {"jsonrpc": "2.0", "event": "progress_update", "params": { "current_line": 327, "total_lines": 4393}}

.. _`JSON-RPC 2.0`: http://www.jsonrpc.org
.. _`JSON-RPC 2.0 spec`: http://www.jsonrpc.org/specification
