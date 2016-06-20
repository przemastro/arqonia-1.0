'use strict';

var services = angular.module('astroApp.services', ['ngResource']);

/*services.factory('httpPostFactory', function($http) {
  return function(file, data, callback) {
    $http({
      url: file,
      method: "POST",
      data: data,
      headers: {
        'Content-Type': undefined
      }
    }).success(function(response) {
      callback(response);
    });
  };
});*/

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