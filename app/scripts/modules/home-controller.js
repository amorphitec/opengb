(function(angular) {

    'use strict';

    function controller($scope, $http, fileFactory, printerFactory, lodash, gcodeService){

    	function getAllFiles(){

            printerFactory.getFiles();

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
                return( vm.selectedFile );
            },
            function( newValue, oldValue ) {
                if (newValue != null) {

                    vm.fileSelector = false;
                    vm.fileRenderer = true;
                    vm.printReady = false;

        		    // IF FILE CONTENTS IS NOT LOADED LOAD THE FILE
        		    // SET VM.SELECTED FILE TO NULL, ADD CONTENTS TO OBJ, THEN RESET SELECTED FILE VALUE
               //      if(!vm.selectedFile.contents && vm.selectedFile.url){

               //          var file = {};
               //          angular.copy(vm.selectedFile, file);
               //          vm.selectedFile = null;

               //          // $http.get(file.url).success(
               //          //     function (data) {
               //          //         file.contents = data;
               //          //         vm.selectedFile = file;
               //          //     }).error(function () {
               //          //         console.error( 'Unable to load file: ' , error );
               //          //     }
               //          // );
               //      }

               //      if(vm.selectedFile){
            			// printerFactory.setFile(vm.selectedFile);
               //      }

                }
            }
        );



    	var vm = this;
        
        vm.printer = printerFactory.printer;
        vm.temperatures = vm.printer.temperatures;
        vm.connection = vm.printer.connection;
    	vm.fileList = printerFactory.files;
        vm.selectedFile = printerFactory.selectedFile;

    	getAllFiles();

        vm.fileSelector = true;
        vm.fileRenderer = true;
        vm.gcode = null;

        vm.selectFile = function(file){
            printerFactory.getFile(file.id);
        };

        vm.deselectFile = function(){
            vm.selectedFile = null;
            vm.fileSelector = true;
            vm.fileRenderer=true;
            vm.printReady=null;
        };

        vm.printSelectedFile = function(){
            if(vm.selectedFile && vm.selectedFile.contents){
                printerFactory.printFile(vm.selectedFile);
            }
        }


    }

    angular
        .module('openGbApp')
        .controller('homeController', ['$scope', '$http', 'fileFactory', 'printerFactory', 'lodash', 'gcodeService', controller ]);

})(angular);