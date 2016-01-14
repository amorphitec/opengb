(function(angular) {

    'use strict';

    function controller($scope, printerFactory){


        var vm = this;

        vm.printer = printerFactory.printer;
        vm.connection = vm.printer.connection;

        vm.connect = function(){
            printerFactory.connect();
        }


    }

    angular
        .module('openGbApp')
        .controller('settingsController', ['$scope', 'printerFactory', controller ]);

})(angular);    
