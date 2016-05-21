'use strict';


var astroApp = angular.module('astroApp.controller', ['ngResource', 'ngAnimate', 'ui.bootstrap', 'smart-table']);

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

       $scope.removeRow = function(index){
          $scope.observations.splice( index, 1);
       };

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

       $scope.items = ['item1', 'item2', 'item3'];
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

       modalInstance.result.then(function (selectedItem) {
          $scope.selected = selectedItem;
          }, function () {
               $log.info('Modal dismissed at: ' + new Date());
             });
       };

       $scope.toggleAnimation = function () {
       $scope.animationsEnabled = !$scope.animationsEnabled;

       scope.itemsByPage=15
       };

}]);


//---------------------------------------------------------Rest Form----------------------------------------------------
    //restFormCtrl
	astroApp.controller('restFormCtrl', function($scope) {
       $scope.reset = function(){
       $scope.firstName = "";
       $scope.startDate = "";
       $scope.endDate = "";
       $scope.uPhotometry = "";
       $scope.vPhotometry = "";
       $scope.bPhotometry = "";
       }
       $scope.reset();
	});

    //submitFormCtrl
    astroApp.controller("submitFormCtrl", ['$scope', 'getEmployee', '$resource', '$routeParams', 'postEmployee',
        function($scope, Employee, $resource, $routeParams, NewEmployee) {


       $scope.company = Employee.query();//get json


       $scope.removeRow = function(index){
          $scope.company.splice( index, 1);
       };
    }]);



//-----------------------------------------------------------Home-------------------------------------------------------

    //mainCtrl
	astroApp.controller('mainCtrl', function($scope) {
	   $scope.message = 'Home made HR diagram';
	});