'use strict';

var services = angular.module('astroApp.services', ['ngResource']);

//File Upload
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

//Authentication
//Register
services.factory('register', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5001/register', {}, {
        save: {method:'POST'}
    });
}]);

//Login
services.factory('login', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5001/login', {}, {
        update: {method:'PUT'}
    });
}]);



//Table list data
services.factory('getObservations', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5001/observations', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

//Diagram data
services.factory('getObservationsDiagram', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5001/observationsDiagram', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

//HR-Diagram data
services.factory('getObservationsHRDiagram', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5001/observationsHRDiagram', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

//Add new observation
services.factory('postObservation', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5001/observations', {}, {
        save: {method:'POST'}
    });
}]);

//Trigger SQL procedure
services.factory('processData', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5001/lastLoad', {}, {
        query: {method:'PUT', isArray:true}
    });
}]);

//Get Last processed observation
services.factory('getProcessedData', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5001/lastLoad', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

//Remove observation
services.factory('removeObservation', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5001/deletedObservations', {}, {
        save: {method:'POST'}
    });
}]);

//Update observation
services.factory('updateObservation', ['$resource',
    function ($resource) {
    return $resource('http://localhost\\:5001/observations', {}, {
        update: {method:'PUT'}
    });
}]);