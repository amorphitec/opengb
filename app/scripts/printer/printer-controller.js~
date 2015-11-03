(function(angular) {

    'use strict';

    function controller($scope, $http, printerFactory){


    	var vm = this;

	vm.printer = printerFactory;

	vm.printer.setPosition({x:0,y:0,z:0});

    }

    angular
        .module('openGbApp')
        .controller('printerController', ['$scope', '$http', 'printerFactory', controller ]);

})(angular);    
