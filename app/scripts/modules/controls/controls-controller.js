(function(angular) {

    'use strict';

    function controller($scope, printerFactory){


    	var vm = this;

        vm.printer = printerFactory;
        vm.position = vm.printer.printer.position;

        vm.homeX = function(){
            vm.printer.homePrintHead({x:true});
        };
        vm.homeY = function(){
            vm.printer.homePrintHead({y:true});
        };
        vm.homeZ = function(){
            vm.printer.homePrintHead({z:true});
        };
        vm.homeAll = function(){
            vm.printer.homePrintHead({x:true,y:true,z:true});
        };

        vm.applyPosition = function(){
            vm.printer.setPosition(vm.position);
        };

        vm.temperatureData = {cyan:[{ x:0, y:240 }],purple:[{ x:0, y:240 }],magenta:[{ x:0, y:140 }]};
        var startTime = new Date();

        function addToData(){

            setTimeout(function(){
                var now = new Date();
                var t = (now - startTime)/1000;
                var temperature = 240 + (20*Math.random()) - 10;
                if(vm.temperatureData['cyan'] != null){
                    vm.temperatureData['cyan'].push({x:t, y:temperature });
                    vm.temperatureData['magenta'].push({x:t, y:temperature-100 });
                    vm.temperatureData['purple'].push({x:t, y:temperature-10 });
                }else{
                    vm.temperatureData['cyan'] =  [{x:t, y:temperature }]; 
                    vm.temperatureData['magenta'].push({x:t, y:temperature-100 });
                    vm.temperatureData['purple'] =  [{x:t, y:temperature-10 }]; 
                }

                $scope.$apply();

                addToData();
            },500);

        }

        addToData();

    }

    angular
        .module('openGbApp')
        .controller('controlsController', ['$scope', 'printerFactory', controller ]);

})(angular);    
