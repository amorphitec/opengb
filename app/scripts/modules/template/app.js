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
  .module('materialDesignTemplate', [
    'ngAnimate',
    'ngAria',
    'ngCookies',
    'ngMessages',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'ngMaterial',
  ]).config(function($mdThemingProvider) {
    $mdThemingProvider.theme('default')
      .primaryPalette('yellow')
      .accentPalette('grey');
    }
  );