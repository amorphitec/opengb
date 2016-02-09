(function(angular) {

    'use strict';

    function directive(lodash,printerFactory) {
		
        /* ----- BEGIN LINK FUNCTION FOR DIRECTIVE ----- */
        function link(scope, element, attrs) {

            scope.filterFiles = function(){

                if(scope.filterString.length > 0){

                    var regex = new RegExp(scope.filterString, "i");
                           
                    var result = lodash.filter(scope.fileList, function(elem) {
                        var elemTestString = elem.name + ' ' + elem.url + ' ' + lodash(elem.tags).toString();
                        return regex.test(elemTestString);
                    });

                    scope.filteredFileList = result;

                }else{

                    scope.filteredFileList = scope.fileList;

                }

            };

            scope.selectFile = function(file){
                printerFactory.getFile(file.id)
            };

            scope.hide = function(){
                return (scope.hideEmpty && scope.filterString.length === 0);
            };

            scope.$watch("fileList", function(newValue, oldValue){
                scope.filterFiles();
            });

            scope.filterString = '';
            scope.hideEmpty = scope.hideEmpty != null ? scope.hideEmpty : false;

        }
        /* ----- END LINK FUNCTION FOR DIRECTIVE ----- */

        return {
            'restrict': 'E',
			'replace':true,
			'scope': {
                fileList:'=ogFslFiles',
                selectedFile:'=ogFslSelectedFile',
                view:'@ogFslView',
                hideEmpty:'=ogFslHideEmpty'
            },
            'templateUrl': 'scripts/modules/files/directives/file-search-list/file-search-list-template.html',
            'link': link
        };

    }

    angular
        .module('openGbApp')
        .directive('ogFileSearchList', [ 'lodash', 'printerFactory', directive ] );

})(angular);