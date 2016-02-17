(function(angular) {

    'use strict';

    function controller($scope, printerFactory){


        var vm = this;

        vm.printer = printerFactory;
        vm.position = vm.printer.printer.position;
        vm.temperatures = vm.printer.printer.temperatures;
        vm.statistics = vm.printer.printer.statistics;
        vm.absolute = true;

        var prevPos;

        vm.homeX = function(){
            vm.printer.homePrintHead({x:true});
            setTimeout(function(){prevPos = vm.position;},100);
        };
        vm.homeY = function(){
            vm.printer.homePrintHead({y:true});
            setTimeout(function(){prevPos = vm.position;},100);
        };
        vm.homeZ = function(){
            vm.printer.homePrintHead({z:true});
            setTimeout(function(){prevPos = vm.position;},100);
        };
        vm.homeAll = function(){
            vm.printer.homePrintHead({x:true,y:true,z:true});
            setTimeout(function(){prevPos = vm.position;},100);
        };

        vm.applyPosition = function(){
            if(vm.absolute){
                prevPos = vm.position;
                vm.printer.setPosition(vm.position);
            }else{
                prevPos = prevPos != null ? prevPos : {x:0,y:0,z:0};
                var pos = {
                            x:parseFloat( parseFloat(vm.position.x) - parseFloat(prevPos.x)).toFixed(2),
                            y:parseFloat( parseFloat(vm.position.y) - parseFloat(prevPos.y)).toFixed(2),
                            z:parseFloat( parseFloat(vm.position.z) - parseFloat(prevPos.z)).toFixed(2)
                    }
                prevPos = vm.position;
                vm.printer.setPosition(pos);
            }
        };

        vm.temperatureData = {
                                purple:vm.statistics.temperatures.bed.current,
                                cyan:vm.statistics.temperatures.nozzle1.current,
                                magenta:vm.statistics.temperatures.nozzle2.current
                             };


    }

    angular
        .module('openGbApp')
        .controller('controlsController', ['$scope', 'printerFactory', controller ]);

})(angular);    
