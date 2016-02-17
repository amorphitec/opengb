(function(angular) {

    'use strict';

    function directive(printerFactory) {
		
        /* ----- BEGIN LINK FUNCTION FOR DIRECTIVE ----- */
        function link(scope, element, attrs) {

            var on = true;
            scope.onButton;
        	scope.tempTargetTemp = scope.targetTemp;

            scope.status = function(){
                var status = on ? 'on' : 'off';
                scope.onButton = 'on';
                if(on && scope.tempTargetTemp != scope.targetTemp){
                    status = 'update';
                    scope.onButton = 'update';
                }
                return status;
            }

            scope.off = function(){
                var obj = {};
                obj[scope.name] = 0;
                printerFactory.setTemperatures(obj);
                on = false;
            }

            scope.applyTarget = function(){
                var obj = {};
                obj[scope.name] = scope.tempTargetTemp;
                printerFactory.setTemperatures(obj);
                on = true;
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
            'templateUrl': 'scripts/modules/controls/directives/temperature-status/temperature-status-template.html',
            'link': link
        };

    }

    angular
        .module('openGbApp')
        .directive('ogTemperatureStatus',[ 'printerFactory', directive ]);

})(angular);