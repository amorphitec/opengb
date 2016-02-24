(function(angular) {

    'use strict';

    /* ----- BEGIN FUNCTION FOR FACTORY ----- */
    function factory($websocket,$rootScope,$location) {

        var startTime = new Date();
        var printerFactory = {};
        var printer = {
                        connection:{baseUrl:null,connected:false,printReady:false},
                        position:{x:null,y:null,z:null},
                        print:{},
                        state:"",
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
        var counters = {};
        var selectedFile = {file:null};

        // This is the printer object
        printerFactory.printer = printer;
        printerFactory.files = files;
        printerFactory.counters = counters;
        printerFactory.selectedFile = selectedFile;


        //Setup url location of webservice
        //can be manually updated using setBaseUrl function
        var ws;
        printer.connection.baseUrl = 'ws://'+$location.host()+':'+$location.port()+'/ws';
        // printer.connection.baseUrl = 'ws://'+$location.host()+':8000/ws';

        printerFactory.connect = function(){

            console.log('attempting to connect to: ' + printer.connection.baseUrl );

            ws = $websocket(printer.connection.baseUrl);

            /* ------------- BEGIN WEBSOCKET EVENTS ------------------ */

            ws.$on('state_change', function (message) {
                var params = message;
                printer.state = params["new"];
                console.log('state change event:', message);

                if(params["old"] == 'EXECUTING' && params["new"] == 'READY'){
                    printer.print = {};
                }

            });

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

            ws.$on('position_update', function (message) {
                var params = message;
                printer.position.x = params.x;
                printer.position.y = params.y;
                printer.position.z = params.z;
                console.log('position event:', message);
            });

            ws.$on('progress_update', function (message) {
                var params = message;
                printer.print.currentLine = params["current_line"];
                printer.print.totalLines = params["total_lines"];
                console.log('progress event:', message);
            });

            /* ------------- END WEBSOCKET EVENTS ------------------ */


        }
        printerFactory.connect();



        /* -------- BEGIN PRIVATE WEBSOCKET FUNCTIONS ---------- */

        //temps should be in form of: 
        //{'bed':<temp>,'nozzle1':<temp>,'nozzle2':<temp>}
        function setTemp(temps) {
            var method = 'set_temp';
            var params = {
                            "bed":temps.bed,
                            "nozzle1":temps.nozzle1,
                            "nozzle2":temps.nozzle2
                         };
            ws.call(method, params);
        };


        //position should be in form of: 
        //{'x':<val>,'y':<val>,'z':<val>}
        function movePrintHead(position){
            var method = 'move_head_absolute';
            var params = {
                            "x":position.x,
                            "y":position.y,
                            "z":position.z
                         };
            ws.call(method, params);
        };


        //home should be in form of: 
        //{'x':<bool>,'y':<bool>,'z':<bool>}
        function homePrintHead(home){

            var method = 'home_head';
            var params = {
                            "x":!!home.x,
                            "y":!!home.y,
                            "z":!!home.z
                         };
            ws.call(method, params);
        };


        //should be in form of: 
        //{}
        function retractFilament(){

            var method = 'retract_filament';
            var params = {
                            
                         };
            ws.call(method, params);
        };


        //should be in form of: 
        //{}
        function unretractFilament(){

            var method = 'unretract_filament';
            var params = {
                            
                         };
            ws.call(method, params);
        };


        //should be in form of: 
        //{}
        function printFile(fid){
            var method = 'print_gcode_file';
            var params = {
                            'id':fid
                         };
            ws.call(method, params);
        };


        //should be in form of: 
        //{}
        function pausePrint() {
            var method = 'pause_print';
            var params = {

                         };
            ws.call(method, params);
        }


        //should be in form of: 
        //{}
        function resumePrint() {
            var method = 'resume_print';
            var params = {

                         };
            ws.call(method, params);
        }


        //should be in form of: 
        //{}
        function cancelPrint() {
            var method = 'cancel_print';
            var params = {

                         };
            ws.call(method, params);
        }


        //should be in form of: 
        //{}
        function emergencyStop() {
            var method = 'emergency_stop';
            var params = {

                         };
            ws.call(method, params);
        }


        //file should be in form of: 
        //{'name':<name>,'payload':<gcode>}
        function putFile(file) {
            var method = 'put_gcode_file';
            var params = {
                    'name':file.name,
                    'payload':file.contents
                };

            ws.call(method,params)
                .then(function(d){
                    getFile(d.id,true)
                    printer.connection.printReady = true;
                }, function(e){
                    printer.connection.printReady = false;
                })
            
        }


        //should be in form of: 
        //{id:<fid>,content:<true/false>}
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


        //should be in form of: 
        //{}
        function getFiles() {
            ws.call('get_gcode_files')
                .then(function(d){
                    angular.forEach(d['gcode_files'],function(f){
                        files[f.id] = f;
                    });
                }, function(e){

                });
        }


        //should be in form of: 
        //{}
        function getCounters() {
            ws.call('get_counters')
                .then(function(d){
                    angular.forEach(d['counters'],function(c){
                        counters[c.id] = c;
                    });
                }, function(e){

                });
        }


        /* --------- END PRIVATE WEBSOCKET FUNCTIONS ---------- */


        /* -------- BEGIN PUBLIC WEBSOCKET FUNCTIONS ---------- */

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


        printerFactory.retractFilament = function(){
            retractFilament();
        };

        printerFactory.unretractFilament = function(){
            unretractFilament();
        };

        printerFactory.printFile = function(fid){
            if(printer.connection.printReady){
                printFile(fid);
            }else{
                console.log('cannot print because print file not ready')
            }
        };

        printerFactory.pausePrint = function(){
           pausePrint();
        };

        printerFactory.resumePrint = function(){
            resumePrint();
        };

        printerFactory.cancelPrint = function(){
            cancelPrint();
        };

        printerFactory.emergencyStop = function(){
            emergencyStop();
        };

        printerFactory.putFile = function(file){
            putFile(file);
        };

        printerFactory.getFile = function(id){
            getFile(id,true);
        };

        printerFactory.getFiles = function(){
            getFiles();
        };

        printerFactory.getCounters = function(){
            getCounters();
        };



        printerFactory.deselectFile = function(){
            printerFactory.selectedFile.file = null;
        };


        /* -------- END PUBLIC WEBSOCKET FUNCTIONS ---------- */

        return printerFactory;

    }
        
    /* ----- END FUNCTION FOR FACTORY ----- */

    angular
        .module('openGbApp')
        .factory('printerFactory', ['$websocket','$rootScope','$location', factory]);
    
})(angular);