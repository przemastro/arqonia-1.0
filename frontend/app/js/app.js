'use strict';

	// create the module and name in astroApp
	var astroApp = angular.module('astroApp', ['ngRoute', 'astroApp.services', 'astroApp.controller', 'ngMessages'])

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

			.when('/photometry', {
				templateUrl : 'pages/photometry.html',
				controller  : 'photometryCtrl'
			})

			.when('/reduction', {
				templateUrl : 'pages/reduction.html',
				controller  : 'reductionCtrl'
			})

			.when('/table-list', {
				templateUrl : 'pages/table-list.html',
				controller  : 'tableListCtrl'
			})

			.when('/hr-diagram', {
				templateUrl : 'pages/hr-diagram.html',
				controller  : 'hrDiagramCtrl',
			})

			.when('/lc-diagram', {
				templateUrl : 'pages/lc-diagram.html',
				controller  : 'lcDiagramCtrl',
			})

			.when('/diagram', {
				templateUrl : 'pages/diagrams.html',
				controller  : 'DiagramCtrl',
			})

			.when('/admin', {
				templateUrl : 'pages/admin.html',
				controller  : 'adminCtrl',
			})

			.when('/search', {
				templateUrl : 'pages/search.html',
				controller  : 'searchCtrl',
			})

			.when('/logout', {
				templateUrl : 'pages/logout.html',
				controller  : 'logoutCtrl',
			})

            //PRODUCTION
			//$locationProvider.html5Mode(true);
	}]);