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

function MainCtrl($resource, $scope, $http) {
  var vm = $scope;

  var couchUrl = 'http://couch.kocsen.com/opinions';
  var Couch = $resource(couchUrl);

  var url = 'http://ihoapi.kocsen.com/opinion';

  vm.loading = false;
  vm.error = false;
  vm.userOpinion = '';

  vm.shareOpinion = function () {
    if (!vm.userOpinion) {
      vm.error = true;
      return
    }

    vm.loading = true;




    couchSave(vm.userOpinion);
  };


  /**
   * Save opinion to couchdb instance
   * @param opinion
   */
  function couchSave(opinion) {
    var couch = new Couch({
      opinion: opinion,
      created_at: new Date()
    });

    couch.$save();
  }

  $('.ui.accordion').accordion();
  $('#help').popup();
}
