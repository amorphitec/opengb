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

    {'result': True, 'id': 1}

Event
=====

The server sends a message to the client to notify the client of an event which has occured.

Example event (status update): ::

    {"event": "temp", "jsonrpc": "2.0", "params": {"bed_current": 203, "bed_target": 105, "nozzle2_target": 203, "nozzle1_current": 104, "nozzle2_current": 108, "nozzle1_target": 206}}

Methods
^^^^^^^

The :class:`opengb.server.MessageHandler` class contains the methods exposed to JSON-RPC 2.0 clients:

.. automethod:: opengb.server.MessageHandler.set_temp

Example request: ::

    {"jsonrpc":"2.0","id":1,"method":"set_temp","params":{"bed":105,"nozzle1":206,"nozzle2":203}}

Example response: ::

    {'result': True, 'id': 1}

.. _`JSON-RPC 2.0`: http://www.jsonrpc.org
.. _`JSON-RPC 2.0 spec`: http://www.jsonrpc.org/specification
