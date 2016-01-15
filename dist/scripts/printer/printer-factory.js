(function(angular) {

    'use strict';

    /* ----- BEGIN FUNCTION FOR FACTORY ----- */
    function factory($websocket,$rootScope,$location) {

        var startTime = new Date();
        var printerFactory = {};
        var printer = {
                        connection:{baseUrl:null,connected:false,printReady:false},
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
        var id = 0;


        //Setup url location of webservice
        //can be manually updated using setBaseUrl function
//        var baseUrl = 'ws://localhost:8000/ws';
        var ws;
        printer.connection.baseUrl = 'ws://'+$location.host()+':'+$location.port()+'/ws';
//        printer.connection.baseUrl = 'ws://'+$location.host()+':8000/ws';

        printerFactory.connect = function(){
            console.log('attempting to connect to: ' + printer.connection.baseUrl );
            ws = $websocket.$new({
                                    url: printer.connection.baseUrl,
                                    reconnect: false
                                });

            ws.$on('$open',function(){
                console.log('ws connected to: ' + printer.connection.baseUrl );
                printer.connected = true;
            });
            ws.$on('$close',function(){
                console.log('ws failed connection to: ' + printer.connection.baseUrl );
                printer.connected = false;
            });
            ws.$on('$error',function(){
                console.log('error: ',ws.$status());
            });

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


        }
        printerFactory.connect();



        /* -------- BEGIN PRIVATE WEBSOCKET FUNCTIONS ---------- */
        //file should be in form of: 
        //{'name':<name>,'contents':<gcode>}
        function getFiles() {
            var data = {
                'jsonrpc': '2.0',
                'id':       id,
                'method':   'get_gcode_files',
                'params': {
                }
            };
            ws.$$send(data);
            id++;
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
            id++;
        }

        function putFile(file) {
            var data = {
                'jsonrpc': '2.0',
                'id':       id,
                'method':   'put_gcode_file',
                'params': {
                    'name':file.name,
                    'payload':file.contents
                }
            };
            ws.$$send(data);
            var thisId = id;
            ws.$on('$message',function(message){
                if(thisId == message.id){
                    printer.connection.printReady = true;
                    $rootScope.$apply();
                }
            });
            id++;
        }

        function printFile(){
            var data = {
                'jsonrpc': '2.0',
                'id': id,
                'method': 'print_file',
            };
            ws.$$send(data);
            id++;
        }

        function pausePrint() {
            return null;
        }

        function getPrintProgress() {
            return null;
        }

        //temps should be in form of: 
        //{'bed':<temp>,'nozzle1':<temp>,'nozzle2':<temp>}
        function setTemp(temps) {
            var data = {
                'jsonrpc': '2.0',
                'id':       id,
                'method':   'set_temp',
                'params': {
                    "bed":temps.bed,
                    "nozzle1":temps.nozzle1,
                    "nozzle2":temps.nozzle2
                }
            };
            ws.$$send(data);
        }

        //position should be in form of: 
        //{'x':<val>,'y':<val>,'z':<val>}
        function movePrintHead(position){
            var data = {
                "jsonrpc":"2.0",
                "id":id,
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
            printer.position.y = home.y ? 600 : printer.position.y;
            printer.position.z = home.z ? 0 : printer.position.z;

            var data = {
                "jsonrpc":"2.0",
                "id":id,
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

        printerFactory.setFile = function(file){
            console.log("new gcode has be loaded");
            putFile(file);
        };
        printerFactory.getFile = function(){
            getFile(id);
        };
        printerFactory.listFiles = function(){
            getFiles();
        };
        printerFactory.printFile = function(){
            if(printer.connection.printReady){
                printFile();
            }else{
                console.log('cannot print because print file not ready')
            }
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
        .factory('printerFactory', ['$websocket','$rootScope','$location', factory]);
    
})(angular);        
    
