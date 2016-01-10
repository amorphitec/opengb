(function(angular) {

    'use strict';

    function directive() {
		
        /* ----- BEGIN LINK FUNCTION FOR DIRECTIVE ----- */
        function link(scope, element, attrs) {

			scope.side = "edge-top";

			var addPositions = function(a,b){
				var result = parseFloat( parseFloat(a) + parseFloat(b)).toFixed(2);
				result = result > 0 ? result : 0 ;
				return result;
			};
			var subtractPositions = function(a,b){
				var result = parseFloat( parseFloat(a) - parseFloat(b)).toFixed(2);
				result = result > 0 ? result : 0 ;
				return result;
			};

			scope.jogUpX = function(){
				scope.posX = addPositions(scope.posX, scope.resolution);
				setTimeout(scope.apply,100);
			};
			scope.jogDownX = function(){
				scope.posX = subtractPositions(scope.posX, scope.resolution);
				setTimeout(scope.apply,100);
			};
			scope.jogUpY = function(){
				scope.posY = addPositions(scope.posY, scope.resolution);
				setTimeout(scope.apply,100);
			};
			scope.jogDownY = function(){
				scope.posY = subtractPositions(scope.posY, scope.resolution);
				setTimeout(scope.apply,100);
			};
			scope.jogUpZ = function(){
				scope.posZ = addPositions(scope.posZ, scope.resolution);
				setTimeout(scope.apply,100);
			};
			scope.jogDownZ = function(){
				scope.posZ = subtractPositions(scope.posZ, scope.resolution);
				setTimeout(scope.apply,100);
			};

        }
        /* ----- END LINK FUNCTION FOR DIRECTIVE ----- */

        return {
            'restrict': 'E',
			'replace':true,
			'scope': {
				posX:'=ccPosX',
				posY:'=ccPosY',
				posZ:'=ccPosZ',
				resolution:'=ccResolution',
				apply:'&ccApply'
            },
            'templateUrl': 'scripts/modules/controls/directives/controls-cube/controls-cube-template.html',
            'link': link
        };

    }

    angular
        .module('openGbApp')
        .directive('controlsCube', directive);

})(angular);