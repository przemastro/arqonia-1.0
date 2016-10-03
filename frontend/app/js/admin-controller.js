'use strict';


    //var __env = {};

    //if(window){
    //  Object.assign(__env, window.__env);
    //}

 angular.module('astroApp.controller', ['ngResource', 'ngAnimate', 'ui.bootstrap', 'smart-table',
 'angularModalService', 'angularSpinner', 'nvd3', 'ngCookies', 'ngAnimate', 'ngSanitize', 'ngCsv', 'angular-bind-html-compile']);

    // Register environment in AngularJS as constant
    astroApp.constant('__env', __env);




//--------------------------------------------------------Admin Panel---------------------------------------------------

	astroApp.controller('adminCtrl', ['$rootScope', '$cookies', function($scope, $cookies) {
	   $scope.message = 'Admin Panel';
	   $scope.isAdminLoggedIn = $cookies.get('admin');
	}]);

	astroApp.controller('processCtrl', ['$scope', 'usSpinnerService', '$rootScope', 'processData', 'getProcessedData', '$window', '$timeout', '$cookies',
      function($scope, usSpinnerService, $rootScope, ProcessData, GetProcessedData, $window, $timeout, $cookies) {

        $scope.message = 'Admin Panel';
        $scope.isAdminLoggedIn = $cookies.get('admin');
        $scope.displayedObservations = [];
        //Call getProcessedData service
        $scope.observations = GetProcessedData.query();

        $scope.startSpin = function() {
          if (!$scope.spinneractive) {
            usSpinnerService.spin('spinner-1');

            //Call processData service
   		    ProcessData.query(function(response){
   		      $scope.message = response.message;
   		   });
          }

          $scope.successTextAlert = "Your request has been added to the queue. Results will be visible in few seconds!";
              $scope.showSuccessAlert = true;

              // switch flag
              $scope.switchBool = function (value) {
                  $scope[value] = !$scope[value];
              };

          $timeout(function(){
             $scope.showSuccessAlert = false;
             }, 15000);
          $timeout(function(){
             $window.location.reload();
             }, 15000);

        };

        $scope.spinneractive = false;

        $rootScope.$on('us-spinner:spin', function(event, key) {
          $scope.spinneractive = true;
        });

        $rootScope.$on('us-spinner:stop', function(event, key) {
          $scope.spinneractive = false;
        });
      }
    ]);

