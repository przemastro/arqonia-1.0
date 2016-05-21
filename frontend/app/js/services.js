'use strict';

var services = angular.module('astroApp.services', ['ngResource']);

services.factory('getEmployee', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5000/:objectId', {}, {
        query: {method:'GET', params:{objectId:'observations'}, isArray:true}
    });
}]);

services.factory('getCounts', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5000/:objectId', {}, {
        query: {method:'GET', params:{objectId:'counter'}, isArray:true}
    });
}]);

services.factory('postEmployee', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5000/', {}, {
        save: {method:'POST'}
    });
}]);

services.factory('postArea', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5000/candidate', {}, {
        save: {method:'POST'}
    });
}]);

services.factory('upload', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5000/file', {}, {
        save: {method:'POST'},
        query: {method:'GET', isArray:true}
    });
}]);

