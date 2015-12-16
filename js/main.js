'use strict';

/**
 * @ngdoc function
 * @name hayboys.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the I have an opinion app
 */
var app = angular.module('iho', ['ngResource', 'ngAnimate']);


angular
  .module('iho')
  .controller('main', MainCtrl);

function MainCtrl($resource, $scope) {
  var vm = $scope;

}
