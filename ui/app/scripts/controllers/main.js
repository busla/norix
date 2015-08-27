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
  	Idkendur.query({ club: 'armenningar', username:'levy', password:'tkd' }, function(data) {
      $scope.idkendur = data.data;
    });  
  });
