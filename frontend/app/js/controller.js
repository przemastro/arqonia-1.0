'use strict';


    //var __env = {};

    //if(window){
    //  Object.assign(__env, window.__env);
    //}

var astroApp = angular.module('astroApp.controller', ['ngResource', 'ngAnimate', 'ui.bootstrap', 'smart-table',
 'angularModalService', 'angularSpinner', 'nvd3', 'ngCookies']);

    // Register environment in AngularJS as constant
    astroApp.constant('__env', __env);



//---------------------------------------------------Table List---------------------------------------------------------
    //tableListCtrl
	astroApp.controller('tableListCtrl', function($scope) {
	});

    //tableCtrl
    astroApp.controller('tableCtrl', ['$rootScope', '$log', '$routeParams', 'getObservations', '$cookies',
                                     function($scope, $log, $routeParams, Observations, $cookies) {
       //Get data
       $scope.displayedObservations = [];
       $scope.observations = Observations.query();
       $log.debug($scope.observations);

       //Add some animation to the table
       $scope.toggleAnimation = function () {
          $scope.animationsEnabled = !$scope.animationsEnabled;
          $scope.itemsByPage=15
       };
       //$scope.isUserLoggedIn = $cookies.get('cook');

    }]);

    //ModalCtrl
    astroApp.controller('ModalCtrl', ['$scope', '$uibModal', function ($scope, $uibModal) {

       $scope.animationsEnabled = true;

       //New Observation Modal
       $scope.addObservation = function () {
            var modalInstance = $uibModal.open({
              animation: $scope.animationsEnabled,
              templateUrl: 'newModalContent.html',
              controller: 'ModalInstanceCtrl',
            });
       };

       //Remove Observation Modal
       $scope.removeObservation = function (removePhotometry) {
          var modalInstance = $uibModal.open({
             animation: $scope.animationsEnabled,
             templateUrl: 'removeObservationModal.html',
             controller: 'ModalInstanceRemoveCtrl',
             resolve: {
                 removePhotometry: function () {
                     return removePhotometry;
                 }
             }
          });
       }

       //Edit Observation Modal
       $scope.editObservation = function (editPhotometry) {
          var modalInstance = $uibModal.open({
             animation: $scope.animationsEnabled,
             templateUrl: 'editObservationModal.html',
             controller: 'ModalInstanceEditCtrl',
             resolve: {
                 editPhotometry: function () {
                     return editPhotometry;
                 }
             }
          });
       }

       //Edit UPhotometry Modal
       $scope.editUPhotometry = function (editUPhotometry) {
          var modalInstance = $uibModal.open({
             animation: $scope.animationsEnabled,
             templateUrl: 'editUPhotometryModal.html',
             controller: 'ModalInstanceEditUPhotometryCtrl',
             resolve: {
                 editUPhotometry: function () {
                     return editUPhotometry;
                 }
             }
          });
       }

       //Edit VPhotometry Modal
       $scope.editVPhotometry = function (editVPhotometry) {
          var modalInstance = $uibModal.open({
             animation: $scope.animationsEnabled,
             templateUrl: 'editVPhotometryModal.html',
             controller: 'ModalInstanceEditVPhotometryCtrl',
             resolve: {
                 editVPhotometry: function () {
                     return editVPhotometry;
                 }
             }
          });
       }

       //Edit BPhotometry Modal
       $scope.editBPhotometry = function (editBPhotometry) {
          var modalInstance = $uibModal.open({
             animation: $scope.animationsEnabled,
             templateUrl: 'editBPhotometryModal.html',
             controller: 'ModalInstanceEditBPhotometryCtrl',
             resolve: {
                 editBPhotometry: function () {
                     return editBPhotometry;
                 }
             }
          });
       }

       //Edit RPhotometry Modal
       $scope.editRPhotometry = function (editRPhotometry) {
          var modalInstance = $uibModal.open({
             animation: $scope.animationsEnabled,
             templateUrl: 'editRPhotometryModal.html',
             controller: 'ModalInstanceEditRPhotometryCtrl',
             resolve: {
                 editRPhotometry: function () {
                     return editRPhotometry;
                 }
             }
          });
       }

       //Edit IPhotometry Modal
       $scope.editIPhotometry = function (editIPhotometry) {
          var modalInstance = $uibModal.open({
             animation: $scope.animationsEnabled,
             templateUrl: 'editIPhotometryModal.html',
             controller: 'ModalInstanceEditIPhotometryCtrl',
             resolve: {
                 editIPhotometry: function () {
                     return editIPhotometry;
                 }
             }
          });
       }

       //Generate Modal
       $scope.generateModal = function () {
            var modalInstance = $uibModal.open({
              animation: $scope.animationsEnabled,
              templateUrl: 'generateModalContent.html',
              controller: 'ModalGenerateCtrl',
            });
       };
    }]);

    astroApp.controller('ModalInstanceCtrl', ['$scope', '$log', '$uibModalInstance', 'postObservation', 'fileUpload', function ($scope, $log, $uibModalInstance, NewObservation, fileUpload) {

      //[Submit]
      $scope.addRow = function(){
          var file = $scope.myFile;
          //use fileUpload service only if file has been uploaded in modal
          if(file) {
             var uploadUrl = __env.apiUrl+"/fileUpload";
             fileUpload.uploadFileToUrl(file, uploadUrl);
             }
          else {
             var file = 'No file';
             }

          var file2 = $scope.myFile2;
          if(file2) {
             var uploadUrl = __env.apiUrl+"/fileUpload";
             fileUpload.uploadFileToUrl(file2, uploadUrl);
             }
          else {
             var file2 = 'No file2';
             }

          var file3 = $scope.myFile3;
          if(file3) {
             var uploadUrl = __env.apiUrl+"/fileUpload";
             fileUpload.uploadFileToUrl(file3, uploadUrl);
             }
          else {
             var file3 = 'No file3';
             }

          var file4 = $scope.myFile4;
          if(file4) {
             var uploadUrl = __env.apiUrl+"/fileUpload";
             fileUpload.uploadFileToUrl(file4, uploadUrl);
             }
          else {
             var file4 = 'No file4';
             }

          var file5 = $scope.myFile5;
          if(file5) {
             var uploadUrl = __env.apiUrl+"/fileUpload";
             fileUpload.uploadFileToUrl(file5, uploadUrl);
             }
          else {
             var file5 = 'No file5';
             }

          //Call postObservation service...
   		  NewObservation.save({name:$scope.name,startDate:$scope.startDate,endDate:$scope.endDate,
   		                     uFileName:file.name,vFileName:file2.name,bFileName:file3.name,
   		                     rFileName:file4.name,iFileName:file5.name}, function(response){
   		  $scope.message = response.message;
   		  $log.debug($scope.message);
   		  });
   		  //...and close modal
   		  $uibModalInstance.dismiss();
      };

      //[Cancel]
      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };
    }]);

    astroApp.controller('ModalInstanceRemoveCtrl', ['$scope', '$log', '$uibModalInstance', 'removeObservation', 'removePhotometry', function ($scope, $log, $uibModalInstance, RemoveObservation, removePhotometry) {

      $scope.ob = $scope.observations;

      //[Cancel]
      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };

      //[Yes] - remove
      $scope.remove = function () {
        //remove photometry is an observation.id so I can keep the correct index of an observation in table list
        $scope.removePhotometry = removePhotometry;
        $log.debug($scope.removePhotometry);
        //Call removeObservation service
        RemoveObservation.save({id:removePhotometry}, function(response){
           $scope.message = response.message;
        });
        //...and close modal
        $uibModalInstance.dismiss();
        return true;
      };
    }]);

    astroApp.controller('ModalInstanceEditCtrl', ['$scope', '$log', '$uibModalInstance', 'updateObservation', 'editPhotometry', 'fileUpload', function ($scope, $log, $uibModalInstance, UpdateObservation, editPhotometry, fileUpload) {
      $scope.ob = $scope.observations;
      //edit photometry is an observation.id so I can keep the correct index of an observation in table list
      $scope.editPhotometry = editPhotometry;
      //this is to check if input field values changed. If yes get the new value to the scope
      $scope.changeName = function() {
         $scope.name = this.name;
      };
      $scope.changeStartDate = function() {
         $scope.startDate = this.startDate;
      };
      $scope.changeEndDate = function() {
         $scope.endDate = this.endDate;
      };

      //This is done to update scope objects to correct value. I compare clicked observation.id with this in scope
      var editPhotometry2 = -1
      		var evaluatedOb = $scope.ob.length;
      		for( var i = 0; i < evaluatedOb; i++ ) {
      			if( $scope.ob[i].id === editPhotometry ) {
      				editPhotometry2 = i;
      				$log.debug($scope.ob[editPhotometry2].name);
      				$scope.name = $scope.ob[editPhotometry2].name;
      				$scope.startDate = $scope.ob[editPhotometry2].startDate;
      				$scope.endDate = $scope.ob[editPhotometry2].endDate;
      				break;
      			}
      		}

      //[Submit]
      $scope.updateRow = function(){

          var file = $scope.myFile;
          //use fileUpload service only if file has been uploaded in modal
          if(file) {
             var uploadUrl = __env.apiUrl+"/fileUpload";
             fileUpload.uploadFileToUrl(file, uploadUrl);
             }
          else {
             var file = 'No file';
             }

          var file2 = $scope.myFile2;
          if(file2) {
             var uploadUrl = __env.apiUrl+"/fileUpload";
             fileUpload.uploadFileToUrl(file2, uploadUrl);
             }
          else {
             var file2 = 'No file2';
             }

          var file3 = $scope.myFile3;
          if(file3) {
             var uploadUrl = __env.apiUrl+"/fileUpload";
             fileUpload.uploadFileToUrl(file3, uploadUrl);
             }
          else {
             var file3 = 'No file3';
             }
          var file4 = $scope.myFile4;
          if(file4) {
             var uploadUrl = __env.apiUrl+"/fileUpload";
             fileUpload.uploadFileToUrl(file4, uploadUrl);
             }
          else {
             var file4 = 'No file4';
             }

          var file5 = $scope.myFile5;
          if(file5) {
             var uploadUrl = __env.apiUrl+"/fileUpload";
             fileUpload.uploadFileToUrl(file5, uploadUrl);
             }
          else {
             var file5 = 'No file5';
             }

          //Call updateObservation service...
   		  UpdateObservation.update({id:$scope.ob[editPhotometry2].id,name:$scope.name,startDate:$scope.startDate,
   		                            endDate:$scope.endDate,
   		                            uFileName:file.name,vFileName:file2.name,bFileName:file3.name,
   		                            rFileName:file4.name,iFileName:file5.name}, function(response){
   		  $scope.message = response.message;
   		  });
   		  //...and close modal
   		  $uibModalInstance.dismiss();
       };

      //[Cancel]
      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };

      $scope.editPhotometry = editPhotometry2
    }]);

    astroApp.controller('ModalInstanceEditUPhotometryCtrl',  ['$scope', '$log', '$uibModalInstance', 'editUPhotometry', function ($scope, $log, $uibModalInstance, editUPhotometry) {
      $scope.ob = $scope.observations;
      $scope.editUPhotometry = editUPhotometry;
      var editUPhotometry2 = -1
      		var evaluatedOb = $scope.ob.length;
      		for( var i = 0; i < evaluatedOb; i++ ) {
      			if( $scope.ob[i].id === editUPhotometry ) {
      				editUPhotometry2 = i;
      				break;
      			}
      		}
      $scope.editUPhotometry = editUPhotometry2

      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };
    }]);

    astroApp.controller('ModalInstanceEditVPhotometryCtrl', function ($scope, $uibModalInstance, editVPhotometry) {
      $scope.ob = $scope.observations;
      $scope.editVPhotometry = editVPhotometry;
      var editVPhotometry2 = -1
      		var evaluatedOb = $scope.ob.length;
      		for( var i = 0; i < evaluatedOb; i++ ) {
      			if( $scope.ob[i].id === editVPhotometry ) {
      				editVPhotometry2 = i;
      				break;
      			}
      		}
      $scope.editVPhotometry = editVPhotometry2


      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };
    });

    astroApp.controller('ModalInstanceEditBPhotometryCtrl', function ($scope, $uibModalInstance, editBPhotometry) {
      $scope.ob = $scope.observations;
      $scope.editBPhotometry = editBPhotometry;
      var editBPhotometry2 = -1
      		var evaluatedOb = $scope.ob.length;
      		for( var i = 0; i < evaluatedOb; i++ ) {
      			if( $scope.ob[i].id === editBPhotometry ) {
      				editBPhotometry2 = i;
      				break;
      			}
      		}
      $scope.editBPhotometry = editBPhotometry2

      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };
    });

    astroApp.controller('ModalInstanceEditRPhotometryCtrl', function ($scope, $uibModalInstance, editRPhotometry) {
      $scope.ob = $scope.observations;
      $scope.editRPhotometry = editRPhotometry;
      var editRPhotometry2 = -1
      		var evaluatedOb = $scope.ob.length;
      		for( var i = 0; i < evaluatedOb; i++ ) {
      			if( $scope.ob[i].id === editRPhotometry ) {
      				editRPhotometry2 = i;
      				break;
      			}
      		}
      $scope.editRPhotometry = editRPhotometry2

      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };
    });

    astroApp.controller('ModalInstanceEditIPhotometryCtrl', function ($scope, $uibModalInstance, editIPhotometry) {
      $scope.ob = $scope.observations;
      $scope.editIPhotometry = editIPhotometry;
      var editIPhotometry2 = -1
      		var evaluatedOb = $scope.ob.length;
      		for( var i = 0; i < evaluatedOb; i++ ) {
      			if( $scope.ob[i].id === editIPhotometry ) {
      				editIPhotometry2 = i;
      				break;
      			}
      		}
      $scope.editIPhotometry = editIPhotometry2

      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };
    });

	astroApp.controller('ModalGenerateCtrl', ['$rootScope', '$scope', '$log', '$uibModalInstance', 'usSpinnerService', 'login', '$cookies', '$location',
	                             function ($rootScope, $scope, $log, $uibModalInstance, usSpinnerService, Login, $cookies, $location) {

      $rootScope.errorFlag = false
      //[Submit]
      $scope.generateCatalog = function(){

}
          //[Cancel]
          $scope.cancel = function () {
            $uibModalInstance.dismiss('cancel');
          };
        }]);


//---------------------------------------------------------Diagrams-----------------------------------------------------

	astroApp.controller('DiagramCtrl', function($scope) {
	});

    //lcDiagramCtrl
	astroApp.controller('lcDiagramCtrl', function($scope) {
	});

    //hrDiagramCtrl
	astroApp.controller('hrDiagramCtrl', function($scope) {
	});

    astroApp.controller("cmdCtrl", ['$rootScope', '$log', 'getObservationsBVDiagram', 'getObservationsBVDiagramRange',
                                     'getObservationsUBDiagram', 'getObservationsUBDiagramRange', 'getObservationsRIDiagram', 'getObservationsRIDiagramRange',
                                     'getObservationsVIDiagram', 'getObservationsVIDiagramRange',
                                  (function ($scope, $log, ObservationsBVDiagram, ObservationsBVDiagramRange, ObservationsUBDiagram, ObservationsUBDiagramRange,
                                  ObservationsRIDiagram, ObservationsRIDiagramRange,ObservationsVIDiagram, ObservationsVIDiagramRange) {

    $scope.HRTitle = true;
    $scope.hrDiagrams = ['B-V CMD', 'U-B CMD', 'R-I CMD', 'V-I CMD'];

    $scope.selectedDiagramValue = '';

    $scope.selectDiagram = function (value) {
      $scope.selectedDiagramValue = value;
      $scope.HRTitle = false;

      console.log($scope.selectedDiagramValue)
      var cutString = value.substring(0, 3);
      if (cutString == "B-V") {
         $scope.ob = ObservationsBVDiagram.query;
         $scope.obRange = ObservationsBVDiagramRange.query;
         var observationsHRDiagram = ObservationsBVDiagram;
      }
      else if (cutString == "U-B") {
         $scope.ob = ObservationsUBDiagram.query;
         $scope.obRange = ObservationsUBDiagramRange.query;
         var observationsHRDiagram = ObservationsUBDiagram;
      }
      else if (cutString == "R-I") {
         $scope.ob = ObservationsRIDiagram.query;
         $scope.obRange = ObservationsRIDiagramRange.query;
         var observationsHRDiagram = ObservationsRIDiagram;
      }
      else if (cutString == "V-I") {
         $scope.ob = ObservationsVIDiagram.query;
         $scope.obRange = ObservationsVIDiagramRange.query;
         var observationsHRDiagram = ObservationsVIDiagram;
      }

      $log.debug($scope.XMax)

      $scope.obRange(function(observationsDiagram) {
      $scope.XMax = 0;
      $scope.XMin = 0;
      $scope.YMax = 0;
      $scope.YMin = 0;
         //Range of data
         $scope.XMax = observationsDiagram[0].XMax;
         $scope.XMin = observationsDiagram[0].XMin;
         $scope.YMax = observationsDiagram[0].YMax;
         $scope.YMin = observationsDiagram[0].YMin;

         //Diagram options
         var myColors = ["#000000"];
         $scope.options = {
                    chart: {
                        type: 'scatterChart',
                        height: 550,
                        width: 600,
                        color: d3.scale.category10().range(myColors),
                        scatter: {
                            onlyCircles: true
                        },
                        showLegend: false,
                        showDistX: false,
                        showDistY: false,
                        showXAxis: true,
                        showYAxis: true,
                        yDomain: [$scope.YMax,$scope.YMin],
                        xDomain: [$scope.XMin,$scope.XMax],
                        tooltipContent: function(key) {
                            return '<h3>' + key + '</h3>';
                        },
                        duration: 350,
                        xAxis: {
                            axisLabel: cutString,
                            tickFormat: function(d){
                                return d3.format('.02f')(d);
                            },
                            ticks: 5
                        },
                        yAxis: {
                            axisLabel: cutString.substring(2,3),
                            tickFormat: function(d){
                                return d3.format('.02f')(d);
                            },
                            axisLabelDistance: -5,
                            ticks: 10
                        },
                        zoom: {
                            enabled: true,
                            scaleExtent: [1, 10],
                            useFixedDomain: false,
                            useNiceScale: false,
                            horizontalOff: false,
                            verticalOff: false,
                            unzoomEventType: 'dblclick.zoom'
                        }
                    }
                };
                return $scope.options

            });
         //The magic

         $scope.data = generateData();

         function generateData() {

             var data = [],
                  shapes = ['circle'],
                  random = d3.random.normal();
               $scope.ob(function(observationsHRDiagram) {

                     if (cutString == "B-V") {
                        $scope.starNames = observationsHRDiagram[0].starNames;
                        $scope.ObservationsDifference = observationsHRDiagram[0].bvObservationsDifference;
                        $scope.FilterObservations = observationsHRDiagram[0].vObservations;
                     }
                     else if (cutString == "U-B") {
                        $scope.starNames = observationsHRDiagram[0].starNames;
                        $scope.ObservationsDifference = observationsHRDiagram[0].ubObservationsDifference;
                        $scope.FilterObservations = observationsHRDiagram[0].bObservations;
                     }
                     else if (cutString == "R-I") {
                        $scope.starNames = observationsHRDiagram[0].starNames;
                        $scope.ObservationsDifference = observationsHRDiagram[0].riObservationsDifference;
                        $scope.FilterObservations = observationsHRDiagram[0].iObservations;
                     }
                     else if (cutString == "V-I") {
                        $scope.starNames = observationsHRDiagram[0].starNames;
                        $scope.ObservationsDifference = observationsHRDiagram[0].viObservationsDifference;
                        $scope.FilterObservations = observationsHRDiagram[0].iObservations;
                     }

               var i = 0
                        angular.forEach($scope.starNames, function(value, index){
                                data.push({
                                    key: value,
                                    values: []
                                });
                                data[i].values.push({
                                    x: $scope.ObservationsDifference[i]
                                    , y: $scope.FilterObservations[i]
                                    , size: 2
                                    , shape: shapes[1]
                                });
                                i++;
                         })
               return $scope.starNames, data;
             });
             return data;
         }
         $scope.exampleData = $scope.data;
     }})]);



//--------------------------------------------------------Admin Panel---------------------------------------------------

	astroApp.controller('adminCtrl', ['$rootScope', '$cookies', function($scope, $cookies) {
	   $scope.message = 'Admin Panel';
	   $scope.isUserLoggedIn = $cookies.get('cook');
	}]);

	astroApp.controller('processCtrl', ['$scope', 'usSpinnerService', '$rootScope', 'processData', 'getProcessedData', '$window', '$timeout', '$cookies',
      function($scope, usSpinnerService, $rootScope, ProcessData, GetProcessedData, $window, $timeout, $cookies) {
        $scope.message = 'Admin Panel';
        $scope.isUserLoggedIn = $cookies.get('cook');
        $scope.displayedObservations = [];
        //Call getProcessedData service
        $scope.observations = GetProcessedData.query();

        $scope.startSpin = function() {
          if (!$scope.spinneractive) {
            usSpinnerService.spin('spinner-1');

            //Call processData service
   		    ProcessData.query(function(response){
   		      $scope.message = response.message;
   		   });
          }

          $scope.successTextAlert = "Your request has been added to the queue. Results will be visible in few seconds!";
              $scope.showSuccessAlert = true;

              // switch flag
              $scope.switchBool = function (value) {
                  $scope[value] = !$scope[value];
              };

          $timeout(function(){
             $scope.showSuccessAlert = false;
             }, 15000);
          $timeout(function(){
             $window.location.reload();
             }, 25000);

        };

        $scope.spinneractive = false;

        $rootScope.$on('us-spinner:spin', function(event, key) {
          $scope.spinneractive = true;
        });

        $rootScope.$on('us-spinner:stop', function(event, key) {
          $scope.spinneractive = false;
        });
      }
    ]);


//--------------------------------------------------------Search Page---------------------------------------------------

	astroApp.controller('searchCtrl', ['$rootScope', '$cookies', function($scope, $cookies) {
	   $scope.message = 'Search';
	   $scope.isUserLoggedIn = $cookies.get('cook');
	   $scope.search = false
	   $scope.stars = false
       $scope.comets = false
       $scope.planetoids = false
	}]);

	astroApp.controller('searchDBCtrl', ['$scope', 'usSpinnerService', '$log', '$rootScope', 'searchData', '$window', '$timeout', '$cookies',
      function($scope, usSpinnerService, $log, $rootScope, SearchData, $window, $timeout, $cookies) {

        //Call getSearchData service

        $scope.startSpin = function() {

          if (!$scope.spinneractive) {
            usSpinnerService.spin('spinner-1');
            //Call searchData service
   		    SearchData.update({name:$scope.nam}, function(response){
   		    $rootScope.stars = false
   		    $rootScope.comets = false
   		    $rootScope.planetoids = false
   		    var object = response[Object.keys(response)[0]];
   		    console.log(object.type);
   		      if (object.type == "Star") {
                 $scope.Data = response
                 console.log($scope.Data);
   		         usSpinnerService.stop('spinner-1');
                 $rootScope.stars = true
              }
   		      else if (object.type == "Comet") {
                 $scope.Data = response
                 console.log($scope.Data);
   		         usSpinnerService.stop('spinner-1');
                 $rootScope.comets = true
              }
   		      else if (object.type == "Planetoid") {
                 $scope.Data = response
                 console.log($scope.Data);
   		         usSpinnerService.stop('spinner-1');
                 $rootScope.planetoids = true
              }
   		      else {
   		         usSpinnerService.stop('spinner-1');
              }
   		   });
        }};
      }
    ]);



//----------------------------------------------------------Login-------------------------------------------------------

    //loginCtrl
	astroApp.controller('loginCtrl', function($scope) {
	   $scope.message = 'Login';
	});

    astroApp.controller('logCtrl', ['$rootScope', '$scope', 'usSpinnerService', '$log', 'login', '$cookies', '$location',
    function ($rootScope, $scope, usSpinnerService, $log, Login, $cookies, $location) {
      $rootScope.errorFlag = false
      //[Submit]
      $scope.loginUser = function(){
          var password = sjcl.encrypt("password", $scope.password)

   		  Login.update({email:$scope.email,password:password}, function(response){
   		  $scope.message = response[Object.keys(response)[0]];
   		  $log.debug($scope.message)
          if($scope.message == "Wrong credentials"){
   		     $rootScope.isUserLoggedIn = false
   		     $rootScope.errorFlag = true
   		     }
   		  else {
             if (!$scope.spinneractive) {
               usSpinnerService.spin('spinner-1');
             };
   		     $cookies.put('cook', true);
   		     $rootScope.isUserLoggedIn = $cookies.get('cook');
   		     $rootScope.errorFlag = false
   		     $rootScope.loggedInUser = $scope.message
   		     $location.path("main");
   		     $scope.spinneractive = false;

   	         $rootScope.$on('us-spinner:spin', function(event, key) {
               $scope.spinneractive = true;
             });

             $rootScope.$on('us-spinner:stop', function(event, key) {
               $scope.spinneractive = false;
             });
   		     }
   		  });
      };
    }]);


    //registerCtrl
	astroApp.controller('registerCtrl', function($scope) {
	   $scope.message = 'Register';
	});

    astroApp.controller('regCtrl', ['$rootScope', '$scope', 'usSpinnerService', '$log', 'register', '$location',
    function ($rootScope, $scope, usSpinnerService, $log, Register, $location) {

      $rootScope.errorFlag = false
      //[Submit]
      $scope.addUser = function(){
          var password = sjcl.encrypt("password", $scope.password)

   		  Register.save({name:$scope.name,email:$scope.email,password:password}, function(response){
   		  $scope.message = response[Object.keys(response)[0]];
   		  $log.debug($scope.message)
          if($scope.message == "User exists"){
   		     $rootScope.errorFlag = true
   		     }
   		  else {
             if (!$scope.spinneractive) {
               usSpinnerService.spin('spinner-1');
             };

   		     $rootScope.errorFlag = false
   		     $location.path("login");

             $scope.spinneractive = false;
   	         $rootScope.$on('us-spinner:spin', function(event, key) {
               $scope.spinneractive = true;
             });

             $rootScope.$on('us-spinner:stop', function(event, key) {
               $scope.spinneractive = false;
             });
   		     }
   		  });
      };

    }]);

//----------------------------------------------------------Logout-------------------------------------------------------

    //logoutCtrl
	astroApp.controller('logoutCtrl', ['$rootScope', '$log', 'login', '$cookies', function ($scope, $log, Login, $cookies) {
	   $scope.message = 'Logout';
	   $cookies.remove("cook");
	}]);

    astroApp.controller('goodbyeCtrl', ['$rootScope', 'usSpinnerService', '$log', 'login', '$cookies', '$location',
    function ($scope, usSpinnerService, $log, Login, $cookies, $location) {
       $scope.isUserLoggedIn = false;
       console.log($scope.isUserLoggedIn);
             if (!$scope.spinneractive) {
               usSpinnerService.spin('spinner-1');
             };
             $scope.spinneractive = false;
       $location.path("main");
    }]);


//-----------------------------------------------------------Home-------------------------------------------------------

    //mainCtrl
	astroApp.controller('mainCtrl', ['$rootScope', '$scope', '$log', 'login', '$cookies', 'getStatistics', '$uibModal', 'subscribe',
	                       function ($rootScope, $scope, $log, Login, $cookies, Statistics, $uibModal, Subscribe) {
	   $rootScope.isUserLoggedIn = $cookies.get('cook');
       $scope.Statistics = Statistics.query();
       $log.debug($scope.Statistics);

              //Login Modal
              $scope.loginModal = function () {
                   var modalInstance = $uibModal.open({
                     animation: $scope.animationsEnabled,
                     templateUrl: 'loginModalContent.html',
                     controller: 'ModalLoginCtrl',
                   });
              };

              //Register Modal
              $scope.registerModal = function () {
                   var modalInstance = $uibModal.open({
                     animation: $scope.animationsEnabled,
                     templateUrl: 'registerModalContent.html',
                     controller: 'ModalRegisterCtrl',
                   });
              };

       $scope.addSubscriber = function(){
          $log.debug($scope.email)
      	  Subscribe.save({email:$scope.email}, function(response){
      	  $scope.message = response[Object.keys(response)[0]];
      	  });
       }
	}]);

	astroApp.controller('ModalLoginCtrl', ['$rootScope', '$scope', '$log', '$uibModalInstance', 'usSpinnerService', 'login', '$cookies', '$location',
	                             function ($rootScope, $scope, $log, $uibModalInstance, usSpinnerService, Login, $cookies, $location) {

      $rootScope.errorFlag = false
      //[Submit]
      $scope.loginUser = function(){
          var password = sjcl.encrypt("password", $scope.password)

   		  Login.update({email:$scope.email,password:password}, function(response){
   		  $scope.message = response[Object.keys(response)[0]];
   		  $log.debug($scope.message)
          if($scope.message == "Wrong credentials"){
   		     $rootScope.isUserLoggedIn = false
   		     $rootScope.errorFlag = true
   		     }
   		  else {
             if (!$scope.spinneractive) {
               usSpinnerService.spin('spinner-1');
             };
   		     $cookies.put('cook', true);
   		     $rootScope.isUserLoggedIn = $cookies.get('cook');
   		     $rootScope.errorFlag = false
   		     $rootScope.loggedInUser = $scope.message
   		     $location.path("main");
   		     $scope.spinneractive = false;

   	         $rootScope.$on('us-spinner:spin', function(event, key) {
               $scope.spinneractive = true;
             });

             $rootScope.$on('us-spinner:stop', function(event, key) {
               $scope.spinneractive = false;
             });
             $uibModalInstance.dismiss();
   		     }
   		  });
      };

          //[Cancel]
          $scope.cancel = function () {
            $uibModalInstance.dismiss('cancel');
          };
        }]);

      astroApp.controller('ModalRegisterCtrl', ['$rootScope', '$scope', '$log', '$uibModalInstance', 'usSpinnerService', 'register', '$cookies', '$location',
	                             function ($rootScope, $scope, $log, $uibModalInstance, usSpinnerService, Register, $cookies, $location) {

      $rootScope.errorFlag = false
      //[Submit]
      $scope.addUser = function(){
          var password = sjcl.encrypt("password", $scope.password)

   		  Register.save({name:$scope.name,email:$scope.email,password:password}, function(response){
   		  $scope.message = response[Object.keys(response)[0]];
   		  $log.debug($scope.message)
          if($scope.message == "User exists"){
   		     $rootScope.errorFlag = true
   		     }
   		  else {
             if (!$scope.spinneractive) {
               usSpinnerService.spin('spinner-1');
             };

   		     $rootScope.errorFlag = false
   		     $location.path("login");

             $scope.spinneractive = false;
   	         $rootScope.$on('us-spinner:spin', function(event, key) {
               $scope.spinneractive = true;
             });

             $rootScope.$on('us-spinner:stop', function(event, key) {
               $scope.spinneractive = false;
             });
             $uibModalInstance.dismiss();
   		     }
   		  });
      };

          //[Cancel]
          $scope.cancel = function () {
            $uibModalInstance.dismiss('cancel');
          };
        }]);

