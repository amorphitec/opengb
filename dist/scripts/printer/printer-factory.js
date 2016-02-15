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
        var selectedFile = {file:null};

        // This is the printer object
        printerFactory.printer = printer;
        printerFactory.files = files;
        printerFactory.selectedFile = selectedFile;


        //Setup url location of webservice
        //can be manually updated using setBaseUrl function
//        var baseUrl = 'ws://localhost:8000/ws';
        var ws;
        printer.connection.baseUrl = 'ws://'+$location.host()+':'+$location.port()+'/ws';
//        printer.connection.baseUrl = 'ws://'+$location.host()+':8000/ws';

        printerFactory.connect = function(){

            console.log('attempting to connect to: ' + printer.connection.baseUrl );

            ws = $websocket(printer.connection.baseUrl);

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

            // ws.$on('pos', function (message) {
            //     var params = message;
            //     printer.position.x = params.x;
            //     printer.position.y = params.y;
            //     printer.position.z = params.z;
            //     console.log('position event:', message);
            // });
            /* ------------- END WEBSOCKET EVENTS ------------------ */


        }
        printerFactory.connect();



        /* -------- BEGIN PRIVATE WEBSOCKET FUNCTIONS ---------- */
        //file should be in form of: 
        //{'name':<name>,'contents':<gcode>}
        function getFiles() {
            ws.call('get_gcode_files')
                .then(function(d){
                    angular.forEach(d['gcode_files'],function(f){
                        files[f.id] = f;
                    });
                }, function(e){

                });
        }

        function getFile(fid,getContent) {
            var method = 'get_gcode_file';
            var params = {
                            'id':fid,
                            'content':!!getContent
                         };
            ws.call(method, params)
                .then(function(d){
                    printer.connection.printReady = true;
                    printerFactory.selectedFile.file = d;
                }, function(e){
                    printer.connection.printReady = false;
                    printerFactory.selectedFile.file = null;
                })
        }

        function putFile(file) {
            var method = 'put_gcode_file';
            var params = {
                    'name':file.name,
                    'payload':file.contents
                };

            ws.call(method,params)
                .then(function(d){
                    getFile(d.id)
                    printer.connection.printReady = true;
                }, function(e){
                    printer.connection.printReady = false;
                })
            
        }

        function printFile(fid){
            var method = 'print_gcode_file';
            var params = {
                            'id':fid
                         };
            ws.call(method, params);
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
            var method = 'get_gcode_file';
            var params = {
                            "bed":temps.bed,
                            "nozzle1":temps.nozzle1,
                            "nozzle2":temps.nozzle2
                         };
            ws.call(method, params);
        }

        //position should be in form of: 
        //{'x':<val>,'y':<val>,'z':<val>}
        function movePrintHead(position){
            var method = 'get_gcode_file';
            var params = {
                            "x":position.x,
                            "y":position.y,
                            "z":position.z
                         };
            ws.call(method, params);
        }

        //home should be in form of: 
        //{'x':<bool>,'y':<bool>,'z':<bool>}
        function homePrintHead(home){
            //TODO: Remove next 3 lines once testing is done;
            printer.position.x = home.x ? 0 : printer.position.x;
            printer.position.y = home.y ? 600 : printer.position.y;
            printer.position.z = home.z ? 0 : printer.position.z;

            var method = 'get_gcode_file';
            var params = {
                            "x":!!home.x,
                            "y":!!home.y,
                            "z":!!home.z
                         };
            ws.call(method, params);
        }
        /* --------- END PRIVATE WEBSOCKET FUNCTIONS ---------- */


        /* -------- BEGIN PUBLIC WEBSOCKET FUNCTIONS ---------- */

        printerFactory.putFile = function(file){
            putFile(file);
        };
        printerFactory.getFile = function(id){
            getFile(id,true);
        };
        printerFactory.getFiles = function(){
            getFiles();
        };
        printerFactory.deselectFile = function(){
            printerFactory.selectedFile.file = null;
        };
        printerFactory.printFile = function(fid){
            if(printer.connection.printReady){
                printFile(fid);
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

        return printerFactory;

    }
        
    /* ----- END FUNCTION FOR FACTORY ----- */

    angular
        .module('openGbApp')
        .factory('printerFactory', ['$websocket','$rootScope','$location', factory]);
    
})(angular);        
    
