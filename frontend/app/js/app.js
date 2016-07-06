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

			.when('/hr-diagram', {
				templateUrl : 'pages/hr-diagram.html',
				controller  : 'hrDiagramCtrl',
			})

			.when('/admin', {
				templateUrl : 'pages/admin.html',
				controller  : 'adminCtrl',
			})

			.when('/login', {
				templateUrl : 'pages/login.html',
				controller  : 'loginCtrl',
			})

			.when('/register', {
				templateUrl : 'pages/register.html',
				controller  : 'registerCtrl',
			})

			.when('/logout', {
				templateUrl : 'pages/logout.html',
				controller  : 'logoutCtrl',
			})
	}]);