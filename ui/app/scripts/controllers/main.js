'use strict';

/**
 * @ngdoc function
 * @name idkendurApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the idkendurApp
 */
angular.module('idkendurApp')
  .controller('MainCtrl', function ($scope, Idkendur) {
  	$scope.idkendur = [];
  	Idkendur.query({ club: '', username:'', password:'' }, function(data) {
      $scope.idkendur = data.data;
    });  
  });
