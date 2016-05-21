'use strict';

	// create the module and name it astroApp
	angular.module('astroApp', ['ngRoute', 'astroApp.services', 'astroApp.controller', 'ngMessages'])

	// configure routes
	   .config(['$routeProvider', function($routeProvider) {
		 $routeProvider
            .when('/main', {
				templateUrl : 'pages/main.html',
				controller  : 'mainCtrl'
			})

			.when('/table-list', {
				templateUrl : 'pages/table-list.html',
				controller  : 'tableListCtrl'
			})

			.when('/rest-form', {
				templateUrl : 'pages/rest-form.html',
				controller  : 'restFormCtrl',
			})
	}]);