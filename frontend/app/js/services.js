'use strict';

var services = angular.module('astroApp.services', ['ngResource']);

astroApp.service('fileUpload', ['$http', function ($http) {
            this.uploadFileToUrl = function(file, uploadUrl){
               var fd = new FormData();
               fd.append('file', file);

               $http.post(uploadUrl, fd, {
                  transformRequest: angular.identity,
                  headers: {'Content-Type': undefined}
               })

               .success(function(){
               })

               .error(function(){
               });
            }
         }]);

services.factory('getObservations', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5000/observations', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

services.factory('getObservationsDiagram', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5000/observationsDiagram', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

services.factory('getObservationsHRDiagram', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5000/observationsHRDiagram', {}, {
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

services.factory('removeObservation', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5000/deletedObservations', {}, {
        save: {method:'POST'}
    });
}]);

services.factory('updateObservation', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5000/observations', {}, {
        update: {method:'PUT'}
    });
}]);