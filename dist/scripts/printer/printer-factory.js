(function(angular) {

    'use strict';

    /* ----- BEGIN FUNCTION FOR FACTORY ----- */
    function factory($websocket,$rootScope) {

        var startTime = new Date();
        var printerFactory = {};
        var printer = {
                        position:{x:null,y:null,z:null},
                        temperatures:{
                            bed:{target:null,current:null},
                            nozzle1:{target:null,current:null},
                            nozzle2:{target:null,current:null},
                        },
                        statistics:{
                            temperatures:{
                                bed:{target:[],current:[]},
                                nozzle1:{target:[],current:[]},
                                nozzle2:{target:[],current:[]},                                    
                            }
                        }
                      };
        var files = {};


        //Setup url location of webservice
        //can be manually updated using setBaseUrl function
        var baseUrl = 'ws://localhost:8000/ws';
        printerFactory.setBaseUrl = function(url){
            baseUrl = url;
        };
        var ws = $websocket.$new(baseUrl);
        //OVERRIDE NG-WEBSOCKET ON MESSAGE TO POINT TO .PARAMS INSTEAD OF .DATA
        ws.$$ws.onmessage = function (message) {
            try {
                var decoded = JSON.parse(message.data);
                ws.$$fireEvent(decoded.event, decoded.params);
                ws.$$fireEvent('$message', decoded);
            }
            catch (err) {
                ws.$$fireEvent('$message', message.params);
            }
            $rootScope.$apply();
        };

        /* ------------- BEGIN WEBSOCKET EVENTS ------------------ */
//        ws.$$ws.onmessage = function(message){
//          console.log(message);
//        };

        ws.$on('temp_update', function (message) {
            var params = message;
            var time = (new Date() - startTime)/1000;
            printer.temperatures.bed.current = params.bed_current;
            printer.temperatures.bed.target = params.bed_target;
            printer.temperatures.nozzle1.current = params.nozzle1_current;
            printer.temperatures.nozzle1.target = params.nozzle1_target;
            printer.temperatures.nozzle2.current = params.nozzle2_current;
            printer.temperatures.nozzle2.target = params.nozzle2_target;

            printer.statistics.temperatures.bed.current.push({x:time,y:params.bed_current});
            printer.statistics.temperatures.nozzle1.current.push({x:time,y:params.nozzle1_current});
            printer.statistics.temperatures.nozzle2.current.push({x:time,y:params.nozzle2_current});

        });
        ws.$on('pos', function (message) {
            var params = message;
            printer.position.x = params.x;
            printer.position.y = params.y;
            printer.position.z = params.z;
            console.log('position event:', message);
        });
        /* ------------- END WEBSOCKET EVENTS ------------------ */


        /* -------- BEGIN PRIVATE WEBSOCKET FUNCTIONS ---------- */
        //file should be in form of: 
        //{'name':<name>,'contents':<gcode>}
        function getFiles() {
            var data = {
                'jsonrpc': '2.0',
                'id':       1,
                'method':   'get_gcode_files',
                'params': {
                }
            };
            ws.$$send(data);
        }

        function getFile(id) {
            var data = {
                'jsonrpc': '2.0',
                'id':       1,
                'method':   'get_gcode_file',
                'params': {
                    'id':id
                }
            };
            ws.$$send(data);
        }

        function loadFile(file) {
            var data = {
                'jsonrpc': '2.0',
                'id':       1,
                'method':   'put_gcode_file',
                'params': {
                    'name':file.name,
                    'payload':file.contents
                }
            };
            ws.$$send(data);
        }

        function startPrint() {
            return null;
        }

        function pausePrint() {
            return null;
        }

        //temps should be in form of: 
        //{'bed':<temp>,'nozzle1':<temp>,'nozzle2':<temp>}
        function setTemp(temps) {
            var data = {
                'jsonrpc': '2.0',
                'id':       1,
                'method':   'set_temp',
                'params': {
                    "bed":temps.bed,
                    "nozzle1":temps.nozzle1,
                    "nozzle2":temps.nozzle2
                }
            };
            ws.$$send(data);
        }

        function getPrintProgress() {
            return null;
        }

        //position should be in form of: 
        //{'x':<val>,'y':<val>,'z':<val>}
        function movePrintHead(position){
            var data = {
                "jsonrpc":"2.0",
                "id":1,
                "method":"move_head",
                "params":{
                    "x":position.x,
                    "y":position.y,
                    "z":position.z
                }
            };
            ws.$$send(data);
        }

        //home should be in form of: 
        //{'x':<bool>,'y':<bool>,'z':<bool>}
        function homePrintHead(home){
            //TODO: Remove next 3 lines once testing is done;
            printer.position.x = home.x ? 0 : printer.position.x;
            printer.position.y = home.y ? 0 : printer.position.y;
            printer.position.z = home.z ? 0 : printer.position.z;

            var data = {
                "jsonrpc":"2.0",
                "id":1,
                "method":"home_head",
                "params":{
                    "x":!!home.x,
                    "y":!!home.y,
                    "z":!!home.z
                }
            };
            ws.$$send(data);
        }
        /* --------- END PRIVATE WEBSOCKET FUNCTIONS ---------- */


        /* -------- BEGIN PUBLIC WEBSOCKET FUNCTIONS ---------- */

        printerFactory.setGcode = function(gcode){
            printer.gcode = gcode;
            console.log("new gcode has be loaded");
        };
        printerFactory.getGcode = function(){
            return printer.gcode;
        };

        printerFactory.setTemperatures = function(temps){
            setTemp(temps);
            console.log("temps to:", temps );
        };
        printerFactory.setPosition = function(position){
            //TODO: remove postition=position line after testing is done
            printer.position = position;

            movePrintHead(position);
            console.log("move to:", position );
        };
        //home should be in format of {x:bool,y:bool,z:bool}
        printerFactory.homePrintHead = function(home){
            homePrintHead(home);
        };

        /* -------- END PUBLIC WEBSOCKET FUNCTIONS ---------- */


        // This is the printer object
        printerFactory.printer = printer;

        return printerFactory;

    }
        
    /* ----- END FUNCTION FOR FACTORY ----- */

    angular
        .module('openGbApp')
        .factory('printerFactory', ['$websocket','$rootScope', factory]);
    
})(angular);        
    