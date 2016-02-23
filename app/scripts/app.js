'use strict';

/**
 * @ngdoc overview
 * @name openGbApp
 * @description
 * # openGbApp
 *
 * Main module of the application.
 */
angular
  .module('openGbApp', [
    'ngAnimate',
    'ngAria',
    'ngCookies',
    'ngMessages',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'ngMaterial',
    'ngFileUpload',
    'ngLodash',
    'websocket',
    'ui.ace',
    'materialDesignTemplate',
    'd3',
    'three',
    'gcode',
    'angular-virtual-keyboard'
  ])
  .config([
      '$routeProvider','$locationProvider','VKI_CONFIG', 
      function ($routeProvider,$locationProvider,VKI_CONFIG) {

//    $locationProvider.html5Mode(true).hashPrefix('!');
        
        $routeProvider
          .when('/:name*', {
            templateUrl: function(urlattr){
                    return 'views/' + urlattr.name + '.html';
                },
          })
          .otherwise({
            redirectTo: 'home'
          });

          VKI_CONFIG.layout.Temperature = {
            'name': "Temperature", 'keys': [
            [["PLA"], ["ABS"]],
            [["1", '1'], ["2", "2"], ["3", "3"]],
            [["4", "4"], ["5", "5"], ["6", '6']],
            [["7", "7"], ["8", "8"], ["9", "9"]],
            [["0", "0"]],
            [["Bksp", "Bksp"],["Enter", "Enter"]]
          ], 'lang': ["en"] };

  }]);
