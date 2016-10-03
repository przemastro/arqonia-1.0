'use strict';


    //var __env = {};

    //if(window){
    //  Object.assign(__env, window.__env);
    //}

 angular.module('astroApp.controller', ['ngResource', 'ngAnimate', 'ui.bootstrap', 'smart-table',
 'angularModalService', 'angularSpinner', 'nvd3', 'ngCookies', 'ngAnimate', 'ngSanitize', 'ngCsv', 'angular-bind-html-compile']);

    // Register environment in AngularJS as constant
    astroApp.constant('__env', __env);


//----------------------------------------------------Photometry--------------------------------------------------------

	astroApp.controller('photometryCtrl', function($scope) {
	});


    astroApp.controller("processPhotometryCtrl", ['$rootScope', '$scope', '$timeout', '$window', '$sce', '$compile', '$location', '$route',
                        (function ($rootScope, $scope, $timeout, $window, $sce, $compile, $location, $route) {

    })]);