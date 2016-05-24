'use strict';


var astroApp = angular.module('astroApp.controller', ['ngResource', 'ngAnimate', 'ui.bootstrap', 'smart-table',
'angularjs-datetime-picker', 'angularModalService']);

    astroApp.config(['$httpProvider', function ($httpProvider) {
                $httpProvider.defaults.useXDomain = true;
                delete $httpProvider.defaults.headers.common['X-Requested-With'];
            }]);

//---------------------------------------------------Table List---------------------------------------------------------
    //tableListCtrl
	astroApp.controller('tableListCtrl', function($scope) {
	});

    //tableCtrl
    astroApp.controller('tableCtrl', ['$scope', '$routeParams', 'getObservations',
                                     function($scope, $routeParams, Observations) {
       $scope.displayedObservations = [];
       $scope.observations = Observations.query();


       $scope.toggleAnimation = function () {
       $scope.animationsEnabled = !$scope.animationsEnabled;

       scope.itemsByPage=15
       };

    }]);

    astroApp.controller('ModalCtrl', ['$scope', '$uibModal', 'postObservation', function ($scope, $uibModal, NewObservation) {

       $scope.animationsEnabled = true;


       $scope.addObservation = function () {
            var modalInstance = $uibModal.open({
              animation: $scope.animationsEnabled,
              templateUrl: 'newModalContent.html',
              controller: 'ModalInstanceCtrl'
            });


          /*modalInstance.addRow = function(){
   	      modalInstance.observations.push({ 'name':$scope.name,
   	                           'startDate': $scope.startDate,
   	                           'endDate':$scope.endDate,
   	                           'uPhotometry':$scope.uPhotometry,
   	                           'vPhotometry':$scope.vPhotometry,
   	                           'bPhotometry':$scope.bPhotometry});

   		   NewObservation.save({name:$scope.name,startDate:$scope.startDate,endDate:$scope.endDate,
   		                     uPhotometry:$scope.uPhotometry,vPhotometry:$scope.vPhotometry,bPhotometry:$scope.bPhotometry}, function(response){
   		      modalInstance.message = response.message;
   		   });

   	      $scope.name='';
   	      $scope.startDate='';
   	      $scope.endDate='';
   	      $scope.uPhotometry='';
             $scope.vPhotometry='';
             $scope.bPhotometry='';
          };*/
       };

        $scope.removeObservation = function (size, index) {
           var modalInstance = $uibModal.open({
              animation: $scope.animationsEnabled,
              templateUrl: 'removeObservationModal.html',
              controller: 'ModalCtrl'
           });

           $scope.observations.splice( index, 1);
        }

        $scope.editObservation = function (size) {
           var modalInstance = $uibModal.open({
              animation: $scope.animationsEnabled,
              templateUrl: 'editObservationModal.html',
              controller: 'ModalCtrl'
           });
        }

        $scope.editPhotometry = function (size) {
           var modalInstance = $uibModal.open({
              animation: $scope.animationsEnabled,
              templateUrl: 'editPhotometryModal.html',
              controller: 'ModalCtrl'
           });
        }
    }]);

    astroApp.controller('ModalInstanceCtrl', function ($scope, $uibModalInstance) {
      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };
    });

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