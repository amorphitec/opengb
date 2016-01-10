(function(angular) {

    'use strict';

    function directive(printerFactory) {
		
        /* ----- BEGIN LINK FUNCTION FOR DIRECTIVE ----- */
        function link(scope, element, attrs) {

        	scope.tempTargetTemp = scope.targetTemp;

            scope.applyTarget = function(){
                var obj = {};
                obj[scope.name] = scope.tempTargetTemp;
                printerFactory.setTemperatures(obj);
            }

        }
        /* ----- END LINK FUNCTION FOR DIRECTIVE ----- */

        return {
            'restrict': 'E',
			'replace':true,
            'transclude':true,
			'scope': {
				name:'@tsName',
                slug:'@tsSlug',
				currentTemp:'@tsCurrentTemp',
				targetTemp:'@tsTargetTemp'
            },
            'templateUrl': 'scripts/modules/controls/directives/temperature-status/colored-temperature-status-template.html',
            'link': link
        };

    }

    angular
        .module('openGbApp')
        .directive('ogTemperatureStatus',[ 'printerFactory', directive ]);

})(angular);