'use strict';

var services = angular.module('astroApp.services', ['ngResource']);

    //services.constant('__env', __env);

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
    return $resource(__env.apiUrlService+'/register', {}, {
        save: {method:'POST'}
    });
}]);

//Login
services.factory('login', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/login', {}, {
        update: {method:'PUT'}
    });
}]);


//Subscribe
services.factory('subscribe', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/subscribe', {}, {
        save: {method:'POST'}
    });
}]);


//Table list data - all
services.factory('getObservations', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observations', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

//Table list data - user
services.factory('getUserObservations', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/userObservations', {}, {
        update: {method:'PUT', isArray:true}
    });
}]);

//LC Diagram data Range
services.factory('getObservationsLCUDiagramRange', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observationsLCUDiagramRange', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

services.factory('getObservationsLCVDiagramRange', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observationsLCVDiagramRange', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

services.factory('getObservationsLCBDiagramRange', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observationsLCBDiagramRange', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

services.factory('getObservationsLCRDiagramRange', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observationsLCRDiagramRange', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

services.factory('getObservationsLCIDiagramRange', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observationsLCIDiagramRange', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

//LC-Diagram data
services.factory('getObservationsLCUDiagram', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observationsLCUDiagram', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

services.factory('getObservationsLCVDiagram', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observationsLCVDiagram', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

services.factory('getObservationsLCBDiagram', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observationsLCBDiagram', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

services.factory('getObservationsLCRDiagram', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observationsLCRDiagram', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

services.factory('getObservationsLCIDiagram', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observationsLCIDiagram', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

//HR Diagram data Range
services.factory('getObservationsBVDiagramRange', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observationsBVDiagramRange', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

services.factory('getObservationsUBDiagramRange', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observationsUBDiagramRange', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

services.factory('getObservationsRIDiagramRange', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observationsRIDiagramRange', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

services.factory('getObservationsVIDiagramRange', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observationsVIDiagramRange', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

//HR-Diagram data
services.factory('getObservationsBVDiagram', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observationsBVDiagram', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

services.factory('getObservationsUBDiagram', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observationsUBDiagram', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

services.factory('getObservationsRIDiagram', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observationsRIDiagram', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

services.factory('getObservationsVIDiagram', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observationsVIDiagram', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

//Statistics data
services.factory('getStatistics', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/statistics', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

//Add new observation
services.factory('postObservation', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observations', {}, {
        save: {method:'POST'}
    });
}]);

//Trigger SQL process procedure
services.factory('processData', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/lastLoad', {}, {
        query: {method:'PUT', isArray:true}
    });
}]);

//Get Last processed observation
services.factory('getProcessedData', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/lastLoad', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

//Trigger SQL Search procedure
services.factory('searchData', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/search', {}, {
        update: {method:'PUT', isArray:true}
    });
}]);

//Remove observation
services.factory('removeObservation', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/deletedObservations', {}, {
        save: {method:'POST'}
    });
}]);

//Update observation
services.factory('updateObservation', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/observations', {}, {
        update: {method:'PUT'}
    });
}]);

//Trigger SQL Catalog values queries
services.factory('searchCatalogData', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/catalog', {}, {
        update: {method:'PUT', isArray:true}
    });
}]);