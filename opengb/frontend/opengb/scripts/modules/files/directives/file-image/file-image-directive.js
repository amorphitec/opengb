(function(angular) {

    'use strict';

    function directive() {
		
        /* ----- BEGIN LINK FUNCTION FOR DIRECTIVE ----- */
        function link(scope, element, attrs) {

            scope.abbr = null;
            var defaultStyle = { 
                                   "text-align":"center",
                                   "border-radius": scope.circle ? "50%" : "0",
                                   "font-size": scope.height != null ? ( scope.height / 2 ) + "px" : "2em",
                                   "height": scope.height != null ? scope.height + "px" : "100%", 
                                   "width": scope.width != null ? scope.width + "px" : "100%" 
                               };

            scope.$watch("file",function( newValue, oldValue ){

                scope.abbr = "";
                scope.style = defaultStyle;

                if( newValue !== null ){

                    scope.abbr =  newValue.name !== null ? newValue.name.toString().substring(0,1).toUpperCase() + newValue.name.toString().substring(1,2).toLowerCase()  : "" ;

                    if(newValue.image !== null){
                        scope.style["background-image"] = "url(" + newValue.image + ")";
                        scope.style["background-size"] = "cover";
                    }else{
                        scope.style["background-image"] = null;
                        scope.style["background-size"] = null;
                    }

                }

                console.log(scope.style);

            });

        }
        /* ----- END LINK FUNCTION FOR DIRECTIVE ----- */

        return {
            'restrict': 'E',
			'replace':true,
			'scope': {
                file: "=ogFiFile",
                height: "=ogFiHeight",
                width: "=ogFiWidth",
                circle: "@ogFiCircle"
            },
            'templateUrl': 'scripts/modules/files/directives/file-image/file-image-template.html',
            'link': link
        };

    }

    angular
        .module('openGbApp')
        .directive('ogFileImage', directive);

})(angular);