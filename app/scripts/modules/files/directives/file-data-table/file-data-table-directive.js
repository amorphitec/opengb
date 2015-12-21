(function(angular) {

    'use strict';

    function directive() {
		
        /* ----- BEGIN LINK FUNCTION FOR DIRECTIVE ----- */
        function link(scope, element, attrs) {

            scope.$watch("file",function( newValue, oldValue ){

                if( newValue !== null ){



                }

            });

        }
        /* ----- END LINK FUNCTION FOR DIRECTIVE ----- */

        return {
            'restrict': 'E',
			'replace':true,
			'scope': {
                file: "=ogFdtFile",
                cancel: "&ogFdtCancel"
            },
            'templateUrl': 'scripts/modules/files/directives/file-data-table/file-data-table-template.html',
            'link': link
        };

    }

    angular
        .module('openGbApp')
        .directive('ogFileDataTable', directive);

})(angular);