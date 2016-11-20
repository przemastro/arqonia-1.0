'use strict';

var services = angular.module('astroApp.services', ['ngResource']);

    //services.constant('__env', __env);

//File Upload
astroApp.service('fileUpload', ['$http', '$cookies', function ($http, $cookies) {
            this.uploadFileToUrl = function(file, uploadUrl){
               var fd = new FormData();
               fd.append('file', file);

               $http.post(uploadUrl, fd, {
                  transformRequest: angular.identity,
                  headers: {'Content-Type': undefined, 'Email': $cookies.get('email'), 'SessionId': $cookies.get('sessionID')}
               })

               .success(function(){
               })

               .error(function(){
               });
            }
}]);

//Multiple File Upload
astroApp.service('multipleFileUpload', ['$http', function ($http) {
            this.uploadFileToUrl = function(files, uploadUrl){
               var fd = new FormData();
               fd.append('file', files);

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
//Update Account Data
services.factory('updateProfile', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/updateProfile', {}, {
        update: {method:'PUT',
                           interceptor: {
                              responseError: function(response) {
                                  console.log('The login has failed: ' + response.loginFailed);
                                  logOutUnauthorizedUser($resource, $scope, usSpinnerService, $cookies, $location, $timeout);
                              }
                           }
        }
    });
}]);

//Logout User
services.factory('updateUser', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/logout', {}, {
        update: {method:'PUT'}
    });
}]);

//Remove Account
services.factory('removeAccount', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/removeAccount', {}, {
        update: {method:'PUT',
                           interceptor: {
                              responseError: function(response) {
                                  console.log('The login has failed: ' + response.loginFailed);
                                  logOutUnauthorizedUser($resource, $scope, usSpinnerService, $cookies, $location, $timeout);
                              }
                           }
        }
    });
}]);

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

//Reminder
services.factory('reminder', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/reminder', {}, {
        save: {method:'POST'}
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
services.factory('getUserObservations', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/userObservations', {}, {
        update: {method:'PUT', isArray:true,
                   interceptor: {
                      responseError: function(response) {
                          console.log('The login has failed: ' + response.loginFailed);
                          logOutUnauthorizedUser($resource, $scope, usSpinnerService, $cookies, $location, $timeout);
                      }
                   }
                }
    });
}]);

//Get Personalized HR Diagram Data
services.factory('getPesronalizedObservationsDiagram', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/RestPersonalizedObservationHRDiagram', {}, {
        update: {method:'PUT', isArray:true,
                           interceptor: {
                              responseError: function(response) {
                                  console.log('The login has failed: ' + response.loginFailed);
                                  logOutUnauthorizedUser($resource, $scope, usSpinnerService, $cookies, $location, $timeout);
                              }
                           }
        }
    });
}]);

//Get Personalized HR Diagram Range
services.factory('getPesronalizedObservationsDiagramRange', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/RestPersonalizedObservationHRDiagramRange', {}, {
        update: {method:'PUT', isArray:true,
                           interceptor: {
                              responseError: function(response) {
                                  console.log('The login has failed: ' + response.loginFailed);
                                  logOutUnauthorizedUser($resource, $scope, usSpinnerService, $cookies, $location, $timeout);
                              }
                           }
        }
    });
}]);

//Get Personalized LC Diagram Data
services.factory('getPesronalizedLCDiagram', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/RestPersonalizedLCDiagram', {}, {
        update: {method:'PUT', isArray:true,
                           interceptor: {
                              responseError: function(response) {
                                  console.log('The login has failed: ' + response.loginFailed);
                                  logOutUnauthorizedUser($resource, $scope, usSpinnerService, $cookies, $location, $timeout);
                              }
                           }
        }
    });
}]);

//Get Personalized LC Diagram Range
services.factory('getPesronalizedLCDiagramRange', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/RestPersonalizedLCDiagramRange', {}, {
        update: {method:'PUT', isArray:true,
                           interceptor: {
                              responseError: function(response) {
                                  console.log('The login has failed: ' + response.loginFailed);
                                  logOutUnauthorizedUser($resource, $scope, usSpinnerService, $cookies, $location, $timeout);
                              }
                           }
        }
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

//Add Photometry Data
services.factory('postPhotometry', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/photometry', {}, {
        update: {method:'PUT', isArray:true,
                           interceptor: {
                              responseError: function(response) {
                                  console.log('The login has failed: ' + response.loginFailed);
                                  logOutUnauthorizedUser($resource, $scope, usSpinnerService, $cookies, $location, $timeout);
                              }
                           }
        }
    });
}]);

//Add new observation
services.factory('postObservation', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/observations', {}, {
        save: {method:'POST',
                           interceptor: {
                              responseError: function(response) {
                                  console.log('The login has failed: ' + response.loginFailed);
                                  logOutUnauthorizedUser($resource, $scope, usSpinnerService, $cookies, $location, $timeout);
                              }
                           }
        }
    });
}]);

//Process data procedure
services.factory('processData', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/lastLoad', {}, {
        query: {method:'PUT', isArray:true,
                           interceptor: {
                              responseError: function(response) {
                                  console.log('The login has failed: ' + response.loginFailed);
                                  logOutUnauthorizedUser($resource, $scope, usSpinnerService, $cookies, $location, $timeout);
                              }
                           }
        }
    });
}]);

//Process personalized data
services.factory('processUserData', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/processUserData', {}, {
        update: {method:'PUT',
                           interceptor: {
                              responseError: function(response) {
                                  console.log('The login has failed: ' + response.loginFailed);
                                  logOutUnauthorizedUser($resource, $scope, usSpinnerService, $cookies, $location, $timeout);
                              }
                           }
        }
    });
}]);

//Get Last processed observation
services.factory('getProcessedData', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/lastLoad', {}, {
        query: {method:'GET', isArray:true}
    });
}]);

//Search Data
services.factory('searchData', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/search', {}, {
        update: {method:'PUT', isArray:true}
    });
}]);

//Remove observation
services.factory('removeObservation', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/deletedObservations', {}, {
        save: {method:'POST',
                           interceptor: {
                              responseError: function(response) {
                                  console.log('The login has failed: ' + response.loginFailed);
                                  logOutUnauthorizedUser($resource, $scope, usSpinnerService, $cookies, $location, $timeout);
                              }
                           }
        }
    });
}]);

//Update observation
services.factory('updateObservation', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/observations', {}, {
        update: {method:'PUT',
                           interceptor: {
                              responseError: function(response) {
                                  console.log('The login has failed: ' + response.loginFailed);
                                  logOutUnauthorizedUser($resource, $scope, usSpinnerService, $cookies, $location, $timeout);
                              }
                           }
        }
    });
}]);

//Trigger SQL Catalog values queries
services.factory('searchCatalogData', ['$resource',
    function ($resource) {
    return $resource(__env.apiUrlService+'/catalog', {}, {
        update: {method:'PUT', isArray:true}
    });
}]);

//Add new reduction images
services.factory('postReductionImages', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/reductionImages', {}, {
        save: {method:'POST',
                           interceptor: {
                              responseError: function(response) {
                                  console.log('The login has failed: ' + response.loginFailed);
                                  logOutUnauthorizedUser($resource, $scope, usSpinnerService, $cookies, $location, $timeout);
                              }
                           }
        }
    });
}]);

//Add new reduction images
services.factory('deleteReductionImages', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/deleteReductionImages', {}, {
        save: {method:'POST',
                           interceptor: {
                              responseError: function(response) {
                                  console.log('The login has failed: ' + response.loginFailed);
                                  logOutUnauthorizedUser($resource, $scope, usSpinnerService, $cookies, $location, $timeout);
                              }
                           }
        }
    });
}]);

//Reduce images
services.factory('postProcessImages', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/processImages', {}, {
        save: {method:'POST',
                           interceptor: {
                              responseError: function(response) {
                                  console.log('The login has failed: ' + response.loginFailed);
                                  logOutUnauthorizedUser($resource, $scope, usSpinnerService, $cookies, $location, $timeout);
                              }
                           }
        }
    });
}]);

//Save images
services.factory('postSaveImages', ['$resource', '$rootScope', 'usSpinnerService', '$cookies', '$location', '$timeout',
    function ($resource, $scope, usSpinnerService, $cookies, $location, $timeout) {
    return $resource(__env.apiUrlService+'/saveImages', {}, {
        save: {method:'POST',
                           interceptor: {
                              responseError: function(response) {
                                  console.log('The login has failed: ' + response.loginFailed);
                                  logOutUnauthorizedUser($resource, $scope, usSpinnerService, $cookies, $location, $timeout);
                              }
                           }
        }
    });
}]);


function logOutUnauthorizedUser($resource, $scope, usSpinnerService, $cookies, $location, $timeout){
                          	   $scope.message = 'Logout';
                          	   $cookies.remove("cook");
                          	   $cookies.remove("admin");
                          	   $cookies.remove("name");
                          	   $cookies.remove("email");
                          	   $cookies.remove("sessionID");
                          	   $cookies.remove("numberOfDarkFilesUploaded");
                          	   $cookies.remove("numberOfFlatFilesUploaded");
                          	   $cookies.remove("numberOfRawFilesUploaded");
                          	   $cookies.remove("numberOfBiasFilesUploaded");
                          	   $cookies.remove("numberOfProcessedFiles");

                          	   //Firstly we need to kill all active modals
                                      $('.modal-content > .ng-scope').each(function()
                                      {
                                          try
                                          {
                                              $(this).scope().$dismiss();
                                          }
                                          catch(_) {}
                                      });

                                      //Set flags
                                      $scope.isUserLoggedIn = false;
                                      $scope.isAdminLoggedIn = false;
                                            if (!$scope.spinneractive) {
                                              usSpinnerService.spin('spinner-1');
                                            };
                                            $scope.spinneractive = false;
                                            usSpinnerService.stop('spinner-1');
                                      $location.path("main");
                                     	           $scope.successTextAlert = "Logout successful.";
                                                      $scope.showSuccessAlert = true;
                                                      // switch flag
                                                      $scope.switchBool = function (value) {
                                                          $scope[value] = !$scope[value];
                                                      };

                                                   $timeout(function(){
                                                      $scope.showSuccessAlert = false;
                                                      }, 5000);
}