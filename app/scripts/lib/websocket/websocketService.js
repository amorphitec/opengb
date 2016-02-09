(function(angular) {

    'use strict';

    function factory($document, $q, $rootScope){

        var wsinst = function(url){

            var callbacks = {};
            var eventsMap = {};
            var current_cb_id = 0
            var ready = false

            var ws = new WebSocket(url)

            ws.onopen = function(){
                console.debug("WS ready")
                ready = true
            }

            ws.onmessage = function(msg) {
                var reply = JSON.parse(msg.data)
                console.debug("Received data from websocket: ", reply)
                if (!!reply['id']) {
                    if(!!reply['error']) {
                        console.debug("Firing callback with error", reply['error'])
                        $rootScope.$apply(callbacks[reply.id].cb.reject(reply.error))
                    }

                    if(!!reply['result']) {
                        console.debug("Firing callback with result", reply['result'])
                        $rootScope.$apply(callbacks[reply.id].cb.resolve(reply.result))
                    }

                    delete callbacks[reply.id]
                } else {

                    var handler = eventsMap[reply.event];
                    if (typeof handler === 'function') {
                        handler.apply(null, [reply.params]);
                        $rootScope.$apply();
                    }

                }
            }

            return {
                call: function(method, params) {
                    var request = {
                        "jsonrpc": "2.0",
                        "method": method,
                        "params": params
                    }

                    current_cb_id += 1
                    request.id = current_cb_id

                    var defer = $q.defer()
                    callbacks[request.id] = {
                        time: new Date(),
                        cb: defer
                    }
                    console.debug("Sending request", request, ready)
                    if (!ready) { 
                        console.error('WS not ready!'); 
                    }else{
                        ws.send(JSON.stringify(request))
                    }
                    return defer.promise
                },
                $on: function(event, callback){
                    eventsMap[event] = callback;
                },
                notify: function(method, params) {
                }
            }

        }

        return wsinst;

    }

  angular.module('websocket', [])
    .factory('$websocket', ['$document', '$q', '$rootScope', factory]);

})(angular);    