(function(angular) {

    'use strict';

    function directive(mdSidenav,timeout,location) {

        /* ----- BEGIN LINK FUNCTION FOR DIRECTIVE ----- */
        function link(scope, element, attrs) {

            var menuId = 'left';

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
            scope.currentPageName = scope.pages[location.path().substring(1)].name;

            scope.toggleSidenav = function() {
                mdSidenav(menuId).toggle();
            };

            scope.$on('$locationChangeSuccess', function(event) {

                scope.currentPageName = scope.pages[location.path().substring(1)].name;

                timeout(
                    function(){
                        mdSidenav(menuId).close();
                    },
                    300
                );

            });

        }
        /* ----- END LINK FUNCTION FOR DIRECTIVE ----- */

        return {
            'restrict': 'E',
            'replace':true,
            'scope': {
                currentPageName: '=ogCurrentPageName'
            },
            'templateUrl': 'scripts/modules/template/directives/top-toolbar/top-toolbar-template.html',
            'link': link
        };

    }

    angular
        .module('materialDesignTemplate')
        .directive('mdtTopToolbar',[ '$mdSidenav','$timeout','$location', directive ]);

})(angular);