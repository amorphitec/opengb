(function(angular) {

    'use strict';

    function controller($scope, $http, printerFactory){


    	var vm = this;

	vm.printer = printerFactory;

	vm.position = {x:0,y:0,z:0};
	$scope.$watch( function(){return vm.position}, 
		function(newValue, oldValue){
			if(newValue != null){
				vm.printer.movePrintHead(newValue);
				console.log("printer Head has been moved to:", newValue );
			}
		},
		true
	);

    }

    angular
        .module('openGbApp')
        .controller('printerController', ['$scope', '$http', 'printerFactory', controller ]);

})(angular);    
