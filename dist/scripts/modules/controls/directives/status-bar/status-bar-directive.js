(function(angular) {

    'use strict';

    function directive(printerFactory) {
		
        /* ----- BEGIN LINK FUNCTION FOR DIRECTIVE ----- */
        function link(scope, element, attrs) {

            scope.percentComplete = 0;

            scope.isPrinting = function(){
                var test = printerFactory.printer.state == 'EXECUTING';
                return test;
            };

            scope.$watch(
                function(){return printerFactory.printer.print},
                function(){
                    var print = printerFactory.printer.print;
                    if(print.currentLine != null){
                        scope.percentComplete = (print.currentLine/print.totalLines*100).toFixed(0);
                    }else{
                        scope.percentComplete = 0;
                    }
                },
                true
            );

        }
        /* ----- END LINK FUNCTION FOR DIRECTIVE ----- */

        return {
            'restrict': 'E',
			'replace':true,
            'transclude':true,
			'scope': {
				
            },
            'templateUrl': 'scripts/modules/controls/directives/status-bar/status-bar-template.html',
            'link': link
        };

    }

    angular
        .module('openGbApp')
        .directive('ogStatusBar',[ 'printerFactory', directive ]);

})(angular);