(function(angular) {

    'use strict';

    function directive(printerFactory) {
		
        /* ----- BEGIN LINK FUNCTION FOR DIRECTIVE ----- */
        function link(scope, element, attrs) {

            var on = false;
            scope.onButton;
        	scope.tempTargetTemp = scope.targetTemp;

            if(scope.targetTemp && scope.targetTemp > 0){
                on = true;
            }

            scope.status = function(){
                var status = on ? 'on' : 'off';
                scope.onButton = 'On';
                if(on && scope.tempTargetTemp != scope.targetTemp){
                    status = 'update';
                    scope.onButton = 'update';
                }
                return status;
            }

            scope.$watch("tempTargetTemp",function(newValue){
                if(newValue.substr(newValue.length - 3) == 'PLA'){
                    scope.tempTargetTemp = 170;
                }
                if(newValue.substr(newValue.length - 3) == 'ABS'){
                    scope.tempTargetTemp = 220;
                }
            });

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

            element.find("input").on('click', function () {
                if (!$window.getSelection().toString()) {
                    // Required for mobile Safari
                    this.setSelectionRange(0, this.value.length)
                }
            });

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