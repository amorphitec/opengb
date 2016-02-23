(function(angular) {

    'use strict';

    function controller($scope, $http, $location, printerFactory, lodash){

        function getAllFiles(){

            printerFactory.getFiles();

        }

        var vm = this;
        
        vm.printer = printerFactory.printer;
        vm.connection = vm.printer.connection;
        vm.fileList = printerFactory.files;
        vm.selectedFile = printerFactory.selectedFile.file;

        getAllFiles();

        vm.deselectFile = function(){
            printerFactory.deselectFile();
        };

        vm.printSelectedFile = function(){
            console.log("trying to print file",[vm.selectedFile]);
            if(vm.selectedFile && vm.selectedFile.content){
                $location.path('home');
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

                    if(newValue.content){
                        vm.printReady = true;
                        console.log("ready to print")
                    }

                }else{

                    vm.selectedFile = null;
                    vm.printReady = null;

                }
            },
            true
        );

    }

    angular
        .module('openGbApp')
        .controller('fileController', ['$scope', '$http', '$location', 'printerFactory', 'lodash', controller ]);

})(angular);