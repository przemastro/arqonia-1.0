'use strict';


	// create the module and name it astroApp
	angular.module('astroApp', ['ngRoute', 'astroApp.services', 'astroApp.controller', 'ngMessages'])

	// configure routes
	   .config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
		 $routeProvider
            .when('/', {
				templateUrl : 'pages/main.html',
				controller  : 'mainCtrl'
			})

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

			.when('/search', {
				templateUrl : 'pages/search.html',
				controller  : 'searchCtrl',
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

			//$locationProvider.html5Mode(true);
	}]);