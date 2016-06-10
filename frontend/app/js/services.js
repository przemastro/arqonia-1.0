'use strict';

var services = angular.module('astroApp.services', ['ngResource']);

services.factory('getObservations', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5000/observations', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

services.factory('postObservation', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5000/observations', {}, {
        save: {method:'POST'}
    });
}]);

services.factory('processData', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5000/lastLoad', {}, {
        query: {method:'PUT', isArray:true}
    });
}]);

services.factory('getProcessedData', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5000/lastLoad', {}, {
        query: {method:'GET', isArray:true}
    });
}]);
