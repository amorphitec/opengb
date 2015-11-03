.. _api:

API
---

OpenGB functionality is exposed via a `JSON-RPC 2.0` API over HTTP using WebSockets.


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

In accordance with the `JSON-RPC 2.0 spec` there are two distinct message types used by the API. The payloads of both are encoded as JSON objects.

Request/Response
================

The client sends a JSON-RPC 2.0 request and the server responds with a JSON-RPC 2.0 response.

Example request (setting temperatures): ::

    {"jsonrpc":"2.0","id":1,"method":"set_temp","params":{"bed":105,"nozzle1":206,"nozzle2":203}}

Example response: ::

    {"jsonrpc":"2.0","id":1 "result":true}

Event
=====

The server sends a message to the client to notify the client of an event which has occured.

Example event (status update): ::

    {"event":"temp","jsonrpc":"2.0","params":{"bed_current":203,"bed_target":105,"nozzle2_target":203,"nozzle1_current":104,"nozzle2_current":108,"nozzle1_target":206}}

Methods
^^^^^^^

The :class:`opengb.server.MessageHandler` class contains the methods exposed to JSON-RPC 2.0 clients:

.. automethod:: opengb.server.MessageHandler.set_temp

Example request: ::

    {"jsonrpc":"2.0","id":1,"method":"set_temp","params":{"bed":105,"nozzle1":206,"nozzle2":203}}

Example response: ::

    {"jsonrpc":"2.0","id":1,"result":true}

.. automethod:: opengb.server.MessageHandler.move_head

Example request: ::

    {"jsonrpc":"2.0","id":1,"method":"move_head","params":{"x":13.2,"y":-2,"z":0.03}}

Example response: ::

    {"jsonrpc":"2.0","id":1,"result":true}

.. automethod:: opengb.server.MessageHandler.get_counters

Example request: ::

    {"jsonrpc":"2.0","id":2,"method":"get_counters","params":{}}

Example response: ::

    {"jsonrpc":"2.0","id":2,"result":{"counters":{"nozzle_2_up_mins":128,"motor_x1_up_mins":128,"motor_x2_up_mins":128 "motor_y2_up_mins":128,"nozzle_1_up_mins":128,"motor_z2_up_mins":128,"motor_z1_up_mins":128,"printer_up_mins":128,"printer_print_mins":46,"bed_up_mins":128,"motor_y1_up_mins":128,"printer_up_mins_session":32}}}

Events
^^^^^^

temp_update
===========

Sent periodically to provide current and target temperatures of printer components.

Example event: ::

    {"jsonrpc": "2.0", "event": "temp_update", "params": { "bed_current": 205, "bed_target": 0, " "nozzle1_current": 106, nozzle1_target": 0, "nozzle2_current": 101, "nozzle2_target": 0}}


.. _`JSON-RPC 2.0`: http://www.jsonrpc.org
.. _`JSON-RPC 2.0 spec`: http://www.jsonrpc.org/specification
