(function (exports) {
  'use strict'

  exports.wsinst = function (url) {
    var callbacks = {}
    var eventsMap = {}
    var current_cb_id = 0
    var ready = false

    var ws = new WebSocket(url)

    ws.onopen = function () {
      console.debug('WS ready')
      ready = true
    }

    ws.onmessage = function (msg) {
      var reply = JSON.parse(msg.data)
      console.debug('Received data from websocket: ', reply)
      if (!!reply['id']) {
        if (!!reply['error']) {
          console.debug('Firing callback with error', reply['error'])
          delete callbacks[reply.id]
        }

        if (!!reply['result']) {
          console.debug('Firing callback with result', reply['result'])
          var cback = callbacks[reply.id]
          if (cback) {
            cback.apply(this, [reply.result])
            delete callbacks[reply.id]
          }
        }

        delete callbacks[reply.id]
      } else {
        var handler = eventsMap[reply.event]
        if (typeof handler === 'function') {
          handler.apply(null, [reply.params])
        }
      }
    }

    return {
      call: function (method, params, cback) {
        var request = {
          'jsonrpc': '2.0',
          'method': method,
          'params': params
        }

        current_cb_id += 1
        request.id = current_cb_id

        callbacks[request.id] = cback

        console.debug('Sending request', request, ready)
        if (!ready) {
          console.error('WS not ready!')
        } else {
          ws.send(JSON.stringify(request))
        }
      },
      $on: function (event, callback) {
        eventsMap[event] = callback
      },
      notify: function (method, params) {
      }
    }
  }
})(window)
