(function(angular) {

    'use strict';

    function directive() {
		
        /* ----- BEGIN LINK FUNCTION FOR DIRECTIVE ----- */
        function link(scope, element, attrs) {

        	console.log("name:",scope);

        }
        /* ----- END LINK FUNCTION FOR DIRECTIVE ----- */

        return {
            'restrict': 'E',
			'replace':true,
			'scope': {
				name:'=tsName',
				currentTemp:'=tsCurrentTemp',
				targetTemp:'=tsTargetTemp'
            },
            'templateUrl': '/scripts/modules/controls/directives/temperature-status/colored-temperature-status-template.html',
            'link': link
        };

    }

    angular
        .module('openGbApp')
        .directive('ogTemperatureStatus', directive);

})(angular);