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
    'ngWebsocket',
    'ui.ace',
    'materialDesignTemplate',
    'd3',
    'three',
    'gcode'
  ])
  .config(function ($routeProvider,$locationProvider) {
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
  });
