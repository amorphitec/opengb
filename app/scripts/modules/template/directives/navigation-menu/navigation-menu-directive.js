(function(angular) {

    'use strict';

    function directive(location) {
        
        /* ----- BEGIN LINK FUNCTION FOR DIRECTIVE ----- */
        function link(scope, element, attrs) {

            /* ---- SETTING UP DEFAULT PAGE OBJECTS -- TO BE REPLACED BY SCOPE OBJECT ----- */
            var defaultPages = {
                            home:{name:'my openGB',url:'home',icon:'home'},
                            controls:{name:'controls',url:'controls',icon:'open_with'},
                            files:{name:'my files',url:'files',icon:'folder'},
                            statistics:{name:'statistics',url:'statistics',icon:'equalizer'},
                            settings:{name:'settings',url:'settings',icon:'settings'}
                        };

            scope.currentPage = "";
            scope.pages = ('pages' in attrs) ? scope.pages : defaultPages;

            scope.isCurrentPageKey = function(page){
                var current = location.path().substring(1);
                return page === current;
            };

        }
        /* ----- END LINK FUNCTION FOR DIRECTIVE ----- */

        return {
            'restrict': 'E',
            'replace':true,
            'scope': {
                pages:'=nmPages'
            },
            'templateUrl': 'scripts/modules/template/directives/navigation-menu/navigation-menu-template.html',
            'link': link
        };

    }

    angular
        .module('materialDesignTemplate')
        .directive('mdtNavigationMenu',[ '$location', directive ]);

})(angular);