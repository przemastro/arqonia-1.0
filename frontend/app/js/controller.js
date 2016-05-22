'use strict';


var astroApp = angular.module('astroApp.controller', ['ngResource', 'ngAnimate', 'ui.bootstrap', 'smart-table',
'angularjs-datetime-picker']);

    astroApp.config(['$httpProvider', function ($httpProvider) {
                $httpProvider.defaults.useXDomain = true;
                delete $httpProvider.defaults.headers.common['X-Requested-With'];
            }]);

//---------------------------------------------------Table List---------------------------------------------------------
    //tableListCtrl
	astroApp.controller('tableListCtrl', function($scope) {
	});

    //tableCtrl
    astroApp.controller("tableCtrl", ['$scope', '$routeParams', 'getEmployee', '$uibModal', 'postEmployee', function($scope, $routeParams, Observation, $uibModal, NewObservation) {
       $scope.displayedObservations = [];
       $scope.observations = Observation.query();

       $scope.addRow = function(){
	      $scope.observations.push({ 'name':$scope.name,
	                           'startDate': $scope.startDate,
	                           'endDate':$scope.endDate,
	                           'uPhotometry':$scope.uPhotometry,
	                           'vPhotometry':$scope.vPhotometry,
	                           'bPhotometry':$scope.bPhotometry});

		   NewObservation.save({name:$scope.name,startDate:$scope.startDate,endDate:$scope.endDate,
		                     uPhotometry:$scope.uPhotometry,vPhotometry:$scope.vPhotometry,bPhotometry:$scope.bPhotometry}, function(response){
		      $scope.message = response.message;
		   });

	      $scope.name='';
	      $scope.startDate='';
	      $scope.endDate='';
	      $scope.uPhotometry='';
          $scope.vPhotometry='';
          $scope.bPhotometry='';
       };

       $scope.animationsEnabled = true;

       $scope.open = function (size) {
          var modalInstance = $uibModal.open({
             animation: $scope.animationsEnabled,
             templateUrl: 'myModalContent.html',
             controller: 'tableCtrl',
             size: size,
             resolve: {
                items: function () {
                return $scope.items;
                }
             }
          });
       };

       $scope.removeObservation = function (size, index) {
          var modalInstance = $uibModal.open({
             animation: $scope.animationsEnabled,
             templateUrl: 'removeObservationModal.html',
             controller: 'tableCtrl',
             size: size,
             resolve: {
                items: function () {
                return $scope.items;
                }
             }
          });

          $scope.observations.splice( index, 1);
       }

       $scope.editObservation = function (size) {
          var modalInstance = $uibModal.open({
             animation: $scope.animationsEnabled,
             templateUrl: 'editObservationModal.html',
             controller: 'tableCtrl',
             size: size,
             resolve: {
                items: function () {
                return $scope.items;
                }
             }
          });
       }

       $scope.editPhotometry = function (size) {
          var modalInstance = $uibModal.open({
             animation: $scope.animationsEnabled,
             templateUrl: 'editPhotometryModal.html',
             controller: 'tableCtrl',
             size: size,
             resolve: {
                items: function () {
                return $scope.items;
                }
             }
          });
       }

       $scope.toggleAnimation = function () {
       $scope.animationsEnabled = !$scope.animationsEnabled;

       scope.itemsByPage=15
       };

}]);

//---------------------------------------------------------HR Diagram----------------------------------------------------
    //hrDiagramCtrl
	astroApp.controller('hrDiagramCtrl', function($scope) {
	});


//--------------------------------------------------------Admin Panel---------------------------------------------------

	astroApp.controller('adminCtrl', function($scope) {
	   $scope.message = 'Admin Panel';
	});
//-----------------------------------------------------------Home-------------------------------------------------------

    //mainCtrl
	astroApp.controller('mainCtrl', function($scope) {
	   $scope.message = 'Home made HR diagram';
	});