(function(angular) {

    'use strict';

    function controller($scope, $http, printerFactory){


    	var vm = this;

	vm.printer = printerFactory;

    }

    angular
        .module('openGbApp')
        .controller('printerController', ['$scope', '$http', 'printerFactory', controller ]);

})(angular);    
