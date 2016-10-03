'use strict';


    //var __env = {};

    //if(window){
    //  Object.assign(__env, window.__env);
    //}

 angular.module('astroApp.controller', ['ngResource', 'ngAnimate', 'ui.bootstrap', 'smart-table',
 'angularModalService', 'angularSpinner', 'nvd3', 'ngCookies', 'ngAnimate', 'ngSanitize', 'ngCsv', 'angular-bind-html-compile']);

    // Register environment in AngularJS as constant
    astroApp.constant('__env', __env);



//--------------------------------------------------------Search Page---------------------------------------------------

	astroApp.controller('searchCtrl', ['$rootScope', '$cookies', function($scope, $cookies) {
	   $scope.message = 'Search';
	   $scope.isUserLoggedIn = $cookies.get('cook');
	   $scope.isAdminLoggedIn = $cookies.get('admin');
	   $scope.search = false
	   $scope.stars = false
       $scope.comets = false
       $scope.planetoids = false
	}]);

	astroApp.controller('searchDBCtrl', ['$scope', 'usSpinnerService', '$rootScope', 'searchData', '$window', '$timeout', '$cookies',
      function($scope, usSpinnerService, $rootScope, SearchData, $window, $timeout, $cookies) {

        //Call getSearchData service
        $scope.startSpin = function() {

          if (!$scope.spinneractive) {
            usSpinnerService.spin('spinner-1');
            //Call searchData service
   		    SearchData.update({name:$scope.nam}, function(response){
   		    $rootScope.stars = false
   		    $rootScope.comets = false
   		    $rootScope.planetoids = false
   		    var object = response[Object.keys(response)[0]];
   		      if (object.type == "Star") {
                 $scope.Data = response
   		         usSpinnerService.stop('spinner-1');
                 $rootScope.stars = true
              }
   		      else if (object.type == "Comet") {
                 $scope.Data = response
   		         usSpinnerService.stop('spinner-1');
                 $rootScope.comets = true
              }
   		      else if (object.type == "Planetoid") {
                 $scope.Data = response
   		         usSpinnerService.stop('spinner-1');
                 $rootScope.planetoids = true
              }
   		      else {
   		         usSpinnerService.stop('spinner-1');
              }
   		   });
        }};
      }
    ]);

