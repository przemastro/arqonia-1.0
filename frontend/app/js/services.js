'use strict';

var services = angular.module('astroApp.services', ['ngResource']);

services.factory('getObservations', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5000/:objectId', {}, {
        query: {method:'GET', params:{objectId:'observations'}, isArray:true}
    });
}]);

services.factory('postObservation', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5000/observations', {}, {
        save: {method:'POST'}
    });
}]);

