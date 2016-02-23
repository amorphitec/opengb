(function(angular) {

    'use strict';

    function controller($scope, $http, printerFactory, lodash, gcodeService){

    	function getAllFiles(){

            printerFactory.getFiles();

    	}

    	var vm = this;
        
        vm.printer = printerFactory.printer;
        vm.temperatures = vm.printer.temperatures;
        vm.connection = vm.printer.connection;
    	vm.fileList = printerFactory.files;
        vm.selectedFile = printerFactory.selectedFile.file;

    	getAllFiles();

        vm.fileSelector = true;
        vm.fileRenderer = true;
        vm.gcode = null;
        vm.loading = false;

        vm.deselectFile = function(){
            printerFactory.deselectFile();
        };

        vm.printSelectedFile = function(){
            console.log("trying to print file",[vm.selectedFile]);
            if(vm.selectedFile && vm.selectedFile.content){
                printerFactory.printFile(vm.selectedFile.id);
            }
        }

        // In order to watch a 'vm.' vs '$scope.' object, you must use 
        // $watch(function(){},function(){}) format
        $scope.$watch(
            function( scope ) {
                return( vm.uploadFile );
            },
            function( newValue, oldValue ) {
                if (newValue != null) {

                    printerFactory.putFile(vm.uploadFile);
                    vm.fileSelector = false;

                }
            }
        );

        $scope.$watch(
            function( scope ) {
                return( printerFactory.selectedFile.file );
            },
            function( newValue, oldValue ) {
                if (newValue != null) {

                    vm.selectedFile = printerFactory.selectedFile.file;
                    vm.fileSelector = false;
                    vm.fileRenderer = true;

                    if(newValue.content){
                        vm.printReady = true;
                        console.log("ready to print")
                    }

                }else{

                    vm.selectedFile = null;
                    vm.fileSelector = true;
                    vm.fileRenderer = true;
                    vm.printReady = null;

                }
            },
            true
        );

    }

    angular
        .module('openGbApp')
        .controller('homeController', ['$scope', '$http', 'printerFactory', 'lodash', 'gcodeService', controller ]);

})(angular);