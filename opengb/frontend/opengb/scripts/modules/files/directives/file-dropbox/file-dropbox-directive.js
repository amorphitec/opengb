(function(angular) {

    'use strict';

    function directive() {
		
        /* ----- BEGIN LINK FUNCTION FOR DIRECTIVE ----- */
        function link(scope, element, attrs) {
            scope.preUploadFile = null;

            scope.$watch( "preUploadFile", function( newValue, oldValue ){

                if( newValue != null ){

                    var file;

                    var fr = new FileReader();
                    fr.onload = function(e){

                        var contents = e.target.result;
                        file = {
                                    "name":scope.preUploadFile.name,
                                    "contents":contents,
                                    "image":null,
                                    "meta":{}
                                };

                        scope.uploadFile = file;
                        scope.$apply();
                        console.log(file.name);

                    };

                    fr.readAsText(newValue);

                }

            });
        }
        /* ----- END LINK FUNCTION FOR DIRECTIVE ----- */

        return {
            'restrict': 'E',
			'replace':true,
			'scope': {
                uploadFile: "=ogFdUploadFile"
            },
            'templateUrl': 'scripts/modules/files/directives/file-dropbox/file-dropbox-template.html',
            'link': link
        };

    }

    angular
        .module('openGbApp')
        .directive('ogFileDropbox', [ directive ]);

})(angular);