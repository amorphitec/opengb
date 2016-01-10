(function(angular) {

    'use strict';

    function controller($scope, printerFactory){


        var vm = this;

        vm.printer = printerFactory;
        vm.position = vm.printer.printer.position;
        vm.temperatures = vm.printer.printer.temperatures;
        vm.statistics = vm.printer.printer.statistics;

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
