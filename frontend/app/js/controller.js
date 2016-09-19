'use strict';


    //var __env = {};

    //if(window){
    //  Object.assign(__env, window.__env);
    //}

var astroApp = angular.module('astroApp.controller', ['ngResource', 'ngAnimate', 'ui.bootstrap', 'smart-table',
 'angularModalService', 'angularSpinner', 'nvd3', 'ngCookies', 'ngAnimate', 'ngSanitize', 'ngCsv', 'angular-bind-html-compile']);

    // Register environment in AngularJS as constant
    astroApp.constant('__env', __env);



//-------------------------------------------------Observations---------------------------------------------------------

    //------------------------------------------------Table List--------------------------------------------------------
    //tableListCtrl
	astroApp.controller('tableListCtrl', function($scope, $window) {
	});

    //tableCtrl
    astroApp.controller('tableCtrl', ['$rootScope', '$routeParams', 'getObservations', 'getUserObservations', '$cookies',
                                     function($scope, $routeParams, Observations, UserObservations, $cookies) {

       //Just to clear table when new user is logged in
       $scope.displayedObservations = [];
       $scope.observations = [];

       //Get the cookies of logged in user
       $scope.loggedInUser = $cookies.get('name');
       $scope.isUserLoggedIn = $cookies.get('cook');
       $scope.loggedInUserEmail = $cookies.get('email');
       $scope.isAdminLoggedIn = $cookies.get('admin');

       //Verify who has logged in and populate table with appropriate data
       if(!$scope.isUserLoggedIn) { //nobody is logged in
       //Get data
          $scope.displayedObservations = [];
          $scope.observations = Observations.query();
       }
       else if ($scope.isAdminLoggedIn==='true') { //Admin
          $scope.displayedObservations = [];
          $scope.observations = Observations.query();
       }
       else if($scope.isUserLoggedIn) { //User
   		  UserObservations.update({email:$scope.loggedInUserEmail}, function(response){
   		     var globalObject = [];
             var len = response.length;
             for(var i = 0; i < len; i++) {
                var newObject = {}
                angular.forEach(response[Object.keys(response)[i]], function(value, key){
                     newObject[key] = value;
                 });
                 globalObject.push(newObject);
             }
   		  $scope.message = response[Object.keys(response)];
          $scope.displayedObservations = [];
          $scope.observations = globalObject;
          })
       }

       //Add some animation to the table
       $scope.toggleAnimation = function () {
          $scope.animationsEnabled = !$scope.animationsEnabled;
          $scope.itemsByPage=15
       };
       //$scope.isUserLoggedIn = $cookies.get('cook');
    }]);

    //-------------------------------------Edit, Remove, New modal windows initialization-------------------------------
    //ModalCtrl
    astroApp.controller('ModalCtrl', ['$scope', 'usSpinnerService', '$uibModal', 'processUserData', '$window', '$timeout', '$cookies',
                       function ($scope, usSpinnerService, $uibModal, ProcessUserData, $window, $timeout, $cookies) {

       //Get the cookies of a logged in user
       $scope.animationsEnabled = true;
       $scope.loggedInUser = $cookies.get('name');
       $scope.isUserLoggedIn = $cookies.get('cook');
       $scope.loggedInUserEmail = $cookies.get('email');

       //Process Data
       $scope.startSpin = function() {
         if (!$scope.spinneractive) {
           usSpinnerService.spin('spinner-1');
           //Call processData service
   	       ProcessUserData.update({email:$scope.loggedInUserEmail}, function(response){
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
            }, 15000);
       };

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

       //Generate Catalog Modal
       $scope.generateModal = function () {
            var modalInstance = $uibModal.open({
              animation: $scope.animationsEnabled,
              templateUrl: 'generateModalContent.html',
              controller: 'ModalGenerateCtrl',
            });
       };
    }]);

    //--------------------------------------------New Observation modal's details---------------------------------------
    astroApp.controller('ModalInstanceCtrl', ['$rootScope', '$scope', '$uibModalInstance', 'postObservation', 'fileUpload', '$uibModal', '$window', '$timeout', '$cookies',
                                     function ($rootScope, $scope, $uibModalInstance, NewObservation, fileUpload, $uibModal, $window, $timeout, $cookies) {


        //DatePicker - don't ask me how it works
        $scope.inlineOptions = {
          customClass: getDayClass,
          minDate: new Date(),
          showWeeks: true
        };

        $scope.dateOptions = {
          formatYear: 'yyyy',
          maxDate: new Date(2020, 5, 22),
          minDate: new Date(),
          startingDay: 1
        };

        $scope.toggleMin = function() {
          $scope.inlineOptions.minDate = $scope.inlineOptions.minDate ? null : new Date();
          $scope.dateOptions.minDate = $scope.inlineOptions.minDate;
        };

        $scope.toggleMin();

        $scope.open1 = function() {
          $scope.popup1.opened = true;
        };

        $scope.open2 = function() {
          $scope.popup2.opened = true;
        };

        $scope.setDate = function(year, month, day) {
          $scope.endDate = new Date(year, month, day);
        };

        $scope.setDate = function(year, month, day) {
          $scope.startDate = new Date(year, month, day);
        };

        $scope.formats = ['yyyy-MM-dd HH:mm:ss Z'];
        $scope.format = $scope.formats[0];
        $scope.altInputFormats = ['M!/d!/yyyy'];

        $scope.popup1 = {
          opened: false
        };

        $scope.popup2 = {
          opened: false
        };

        var tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        var afterTomorrow = new Date();
        afterTomorrow.setDate(tomorrow.getDate() + 1);
        $scope.events = [
          {
            date: tomorrow,
            status: 'full'
          },
          {
            date: afterTomorrow,
            status: 'partially'
          }
        ];

        function getDayClass(data) {
          var date = data.date,
            mode = data.mode;
          if (mode === 'day') {
            var dayToCheck = new Date(date).setHours(0,0,0,0);

            for (var i = 0; i < $scope.events.length; i++) {
              var currentDay = new Date($scope.events[i].date).setHours(0,0,0,0);

              if (dayToCheck === currentDay) {
                return $scope.events[i].status;
              }
            }
          }
          return '';
        }

      //[Submit]
      $scope.addRow = function(){

          //Firstly part responsible for uploading/posting files
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
   		                     rFileName:file4.name,iFileName:file5.name,objectType:$scope.objectValue,
   		                     verified:$scope.radioValue,email:$scope.loggedInUserEmail}, function(response){
   		  $scope.message = response.message;
   		  });
   		  //...and close modal
   		  $uibModalInstance.dismiss();
   		  $rootScope.successTextAlert = "New observation has been added to the staging area.";
              $rootScope.showSuccessAlert = true;
              // switch flag
              $rootScope.switchBool = function (value) {
                  $rootScope[value] = !$rootScope[value];
              };
          $timeout(function(){
             $rootScope.showSuccessAlert = false;
             }, 5000);
      };
      //[Cancel]
      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };
    }]);

    //-------------------------------------------Remove Observation modal's details-------------------------------------
    astroApp.controller('ModalInstanceRemoveCtrl', ['$rootScope', '$scope', '$uibModalInstance', 'removeObservation', 'removePhotometry', '$uibModal', '$window', '$timeout', '$cookies',
                                           function ($rootScope, $scope, $uibModalInstance, RemoveObservation, removePhotometry, $uibModal, $window, $timeout, $cookies) {

      $scope.ob = $scope.observations;

      //[Cancel]
      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };

      //Just to get appropriate object name to be removed
      angular.forEach($scope.ob, function(value, key){
         if(value.id === removePhotometry) {
            $scope.removePhotometryName = value.name;
         }
      });

      //[Yes] - remove
      $scope.remove = function () {
        //remove photometry is an observation.id so I can keep the correct index of an observation in table list
        $scope.removePhotometry = removePhotometry;
        //Call removeObservation service
        RemoveObservation.save({id:removePhotometry,email:$scope.loggedInUserEmail,name:$scope.removePhotometryName}, function(response){
           $scope.message = response.message;
        });
        //...and close modal
        $uibModalInstance.dismiss();
        $rootScope.successTextAlert = "Observation has been soft deleted from the staging area.";
               $rootScope.showSuccessAlert = true;
               // switch flag
               $rootScope.switchBool = function (value) {
                   $rootScope[value] = !$rootScope[value];
               };
           $timeout(function(){
              $rootScope.showSuccessAlert = false;
              }, 5000);
        return true;
      };
    }]);

    //-------------------------------------------Edit Observation modal's details---------------------------------------
    astroApp.controller('ModalInstanceEditCtrl', ['$rootScope', '$scope', '$uibModalInstance', 'updateObservation', 'editPhotometry', 'fileUpload', '$uibModal', '$window', '$timeout', '$cookies',
                                         function ($rootScope, $scope, $uibModalInstance, UpdateObservation, editPhotometry, fileUpload, $uibModal, $window, $timeout, $cookies) {


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
      				$scope.name = $scope.ob[editPhotometry2].name;
      				$scope.startDate = $scope.ob[editPhotometry2].startDate;
      				$scope.endDate = $scope.ob[editPhotometry2].endDate;
      				break;
      			}
      		}

      //DatePicker again

       $scope.startDate = new Date($scope.startDate);
       $scope.endDate = new Date($scope.endDate);

        $scope.inlineOptions = {
          customClass: getDayClass,
          minDate: new Date(),
          showWeeks: true
        };

        $scope.dateOptions = {
          formatYear: 'yyyy',
          maxDate: new Date(2020, 5, 22),
          minDate: new Date(),
          startingDay: 1
        };


        $scope.toggleMin = function() {
          $scope.inlineOptions.minDate = $scope.inlineOptions.minDate ? null : new Date();
          $scope.dateOptions.minDate = $scope.inlineOptions.minDate;
        };

        $scope.toggleMin();

        $scope.open1 = function() {
          $scope.popup1.opened = true;
        };

        $scope.open2 = function() {
          $scope.popup2.opened = true;
        };

        $scope.setDate = function(year, month, day) {
          $scope.endDate = new Date(year, month, day);
        };

        $scope.setDate = function(year, month, day) {
          $scope.startDate = new Date(year, month, day);
        };

        $scope.formats = ['yyyy-MM-dd HH:mm:ss Z'];
        $scope.format = $scope.formats[0];
        $scope.altInputFormats = ['M!/d!/yyyy'];

        $scope.popup1 = {
          opened: false
        };

        $scope.popup2 = {
          opened: false
        };

        var tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        var afterTomorrow = new Date();
        afterTomorrow.setDate(tomorrow.getDate() + 1);
        $scope.events = [
          {
            date: tomorrow,
            status: 'full'
          },
          {
            date: afterTomorrow,
            status: 'partially'
          }
        ];

        function getDayClass(data) {
          var date = data.date,
            mode = data.mode;
          if (mode === 'day') {
            var dayToCheck = new Date(date).setHours(0,0,0,0);

            for (var i = 0; i < $scope.events.length; i++) {
              var currentDay = new Date($scope.events[i].date).setHours(0,0,0,0);

              if (dayToCheck === currentDay) {
                return $scope.events[i].status;
              }
            }
          }
          return '';
        }

      //[Submit]
      $scope.updateRow = function(){

          //Again part responsible for uploading files
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
   		                            rFileName:file4.name,iFileName:file5.name,objectType:$scope.objectValue,
                                    verified:$scope.radioValue,email:$scope.loggedInUserEmail}, function(response){
   		  $scope.message = response.message;
   		  });
   		  //...and close modal
   		  $uibModalInstance.dismiss();
          $rootScope.successTextAlert = "Observation has been updated in the staging area.";
               $rootScope.showSuccessAlert = true;
               // switch flag
               $rootScope.switchBool = function (value) {
                   $rootScope[value] = !$rootScope[value];
               };
           $timeout(function(){
              $rootScope.showSuccessAlert = false;
              }, 5000);
       };

      //[Cancel]
      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };

      $scope.editPhotometry = editPhotometry2
    }]);

    //-------------------------------------------Edit UPhotometry modal's details---------------------------------------
    astroApp.controller('ModalInstanceEditUPhotometryCtrl',  ['$scope', '$uibModalInstance', 'editUPhotometry', function ($scope, $uibModalInstance, editUPhotometry) {

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

    //-------------------------------------------Edit VPhotometry modal's details---------------------------------------
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

    //-------------------------------------------Edit BPhotometry modal's details---------------------------------------
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

    //-------------------------------------------Edit RPhotometry modal's details---------------------------------------
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

    //-------------------------------------------Edit IPhotometry modal's details---------------------------------------
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

    //-------------------------------------------Generate Catalog modal's details---------------------------------------
	astroApp.controller('ModalGenerateCtrl', ['$rootScope', '$scope', '$uibModalInstance', 'usSpinnerService', 'login', '$cookies', '$location', 'searchCatalogData',
	                             function ($rootScope, $scope, $uibModalInstance, usSpinnerService, Login, $cookies, $location, SearchCatalogData) {

      //Get the cookies of a user firstly
      $rootScope.errorFlag = false;
      $scope.loadFlag = false;
      $scope.generateFlag = true;


      //Load data from DB when clicking [Load Data] button
      $scope.loadData = function() {

          if (!$scope.spinneractive) {
            usSpinnerService.spin('spinner-1');
            //Call searchCatalogData service
   		    SearchCatalogData.update({objectType:$scope.objectValue, abbreviation: $scope.abbreviation, email:$scope.loggedInUserEmail}, function(response){
   		      var globalObject = [];
   		          if(response.length==2) {
   		             var len = 1;
   		          }
   		          else {
   		             var len = response.length;
   		          }
                  for(var i = 0; i < len; i++) {
                  var newObject = {}
                          angular.forEach(response[Object.keys(response)[i]], function(value, key){
                                  newObject[key] = value;
                           });
                           globalObject.push(newObject);
                     }

            $scope.loadFlag = true;
            $scope.getArray = globalObject;
            //Check what type of object data was returned and generate catalogs headers
            if ($scope.objectValue == "Star" && response != null) {
                $scope.getHeader = function () {
                      return ["Catalog Number", "Object Name", "U", "V", "B", "R", "I", "B-V", "U-B", "R-I", "V-I"]
                      };
                $scope.generateFlag = false;
            }
            else if (($scope.objectValue == "Comet" || $scope.objectValue == "Planetoid") && response != null){
                $scope.getHeader = function () {
                      return ["Catalog Number", "Object Name", "U", "V", "B", "R", "I"]
                      };
                $scope.generateFlag = false;
            }
            else {
                $scope.getHeader = function () {
                      return ["Catalog Number", "Object Name", "U", "V", "B", "R", "I"]
                      };
                $scope.generateFlag = true;
            }
            usSpinnerService.stop('spinner-1');
   		   });
        };



      }

      //[Generate]
      $scope.generate = function(){
             $uibModalInstance.dismiss();
      };

      //[Cancel]
      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };
    }]);


//---------------------------------------------------------Diagrams-----------------------------------------------------

	astroApp.controller('DiagramCtrl', function($scope) {
	});

    //-----------------------------------------------------Light Curves-------------------------------------------------
    //lcDiagramCtrl
	astroApp.controller('lcDiagramCtrl', function($scope) {
	});


    astroApp.controller("lcCtrl", ['$rootScope', 'getObservationsLCUDiagramRange', 'getObservationsLCUDiagram',
                                   'getObservationsLCVDiagramRange', 'getObservationsLCVDiagram','getObservationsLCBDiagramRange', 'getObservationsLCBDiagram',
                                   'getObservationsLCRDiagramRange', 'getObservationsLCRDiagram','getObservationsLCIDiagramRange', 'getObservationsLCIDiagram',
                                   'getPesronalizedLCDiagramRange','getPesronalizedLCDiagram','$cookies',
                                  (function ($scope, ObservationsLCUDiagramRange, ObservationsLCUDiagram, ObservationsLCVDiagramRange, ObservationsLCVDiagram,
                                  ObservationsLCBDiagramRange, ObservationsLCBDiagram, ObservationsLCRDiagramRange, ObservationsLCRDiagram,
                                  ObservationsLCIDiagramRange, ObservationsLCIDiagram, PesronalizedLCDiagramRange, PesronalizedLCDiagram, $cookies) {

       //Get the user's cookies
       $scope.loggedInUser = $cookies.get('name');
       $scope.isUserLoggedIn = $cookies.get('cook');
       $scope.loggedInUserEmail = $cookies.get('email');
       $scope.isAdminLoggedIn = $cookies.get('admin');


       $scope.LCTitle = true;
       $scope.lcFilters = ['U Photometry', 'V Photometry', 'B Photometry', 'R Photometry', 'I Photometry'];

       $scope.selectedFilterValue = '';
       $scope.selectedFilter = false;

       //select filter from drop down
       $scope.selectFilter = function (filter) {
          $scope.LCTitle = true;
          $scope.selectedFilterValue = filter;

          $scope.cutString = filter.substring(0, 1);
          //For global data or admin
          if($scope.isUserLoggedIn!='true' || $scope.isAdminLoggedIn==='true') {
             if ($scope.cutString == "U") {
                $scope.obRange = ObservationsLCUDiagramRange.query;
                $scope.selectedFilter = true;
                $scope.obRange(function(observationsDiagram) {
                    $scope.starNames = observationsDiagram[0].StarNames;
                });
             }
             else if ($scope.cutString == "V") {
                $scope.obRange = ObservationsLCVDiagramRange.query;
                $scope.selectedFilter = true;
                $scope.obRange(function(observationsDiagram) {
                    $scope.starNames = observationsDiagram[0].StarNames;
                });
             }
             else if ($scope.cutString == "B") {
                $scope.obRange = ObservationsLCBDiagramRange.query;
                $scope.selectedFilter = true;
                $scope.obRange(function(observationsDiagram) {
                    $scope.starNames = observationsDiagram[0].StarNames;
                });
             }
             else if ($scope.cutString == "R") {
                $scope.obRange = ObservationsLCRDiagramRange.query;
                $scope.selectedFilter = true;
                $scope.obRange(function(observationsDiagram) {
                    $scope.starNames = observationsDiagram[0].StarNames;
                });
             }
             else if ($scope.cutString == "I") {
                $scope.obRange = ObservationsLCIDiagramRange.query;
                $scope.selectedFilter = true;
                $scope.obRange(function(observationsDiagram) {
                    $scope.starNames = observationsDiagram[0].StarNames;
                });
             }
          }
          //For logged in gentleman
          else {
             PesronalizedLCDiagramRange.update({filter:$scope.cutString, email:$scope.loggedInUserEmail}, function(response){
                     for(var i = 0; i < response.length; i++) {
                        var j = 0
                        var tab = {}
                        angular.forEach(response[Object.keys(response)[i]], function(value, key){
                                tab[j] = value;
                                j++;
                        });
                     }
                     $scope.starNames = tab[4];
                     $scope.selectedFilter = true;
             })
          }
       }
      $scope.selectedObjectValue = '';

      //select object from drop down for selected filter
      $scope.selectObject = function (object) {
        $scope.LCTitle = false;
        $scope.selectedObjectValue = object;
        //Again global data firstly
        if($scope.isUserLoggedIn!='true' || $scope.isAdminLoggedIn==='true') {
           if ($scope.cutString == "U") {
              $scope.ob = ObservationsLCUDiagram.query;
              $scope.obRange = ObservationsLCUDiagramRange.query;
           }
           else if ($scope.cutString == "V") {
              $scope.ob = ObservationsLCVDiagram.query;
              $scope.obRange = ObservationsLCVDiagramRange.query;
           }
           else if ($scope.cutString == "B") {
              $scope.ob = ObservationsLCBDiagram.query;
              $scope.obRange = ObservationsLCBDiagramRange.query;
           }
           else if ($scope.cutString == "R") {
              $scope.ob = ObservationsLCRDiagram.query;
              $scope.obRange = ObservationsLCRDiagramRange.query;
           }
           else if ($scope.cutString == "I") {
              $scope.ob = ObservationsLCIDiagram.query;
              $scope.obRange = ObservationsLCIDiagramRange.query;
           }

           //set range of data
           $scope.obRange(function(observationsDiagram) {
               $scope.XMaxAll = observationsDiagram[0].XMax;
               $scope.XMinAll = observationsDiagram[0].XMin;
               $scope.YMaxAll = observationsDiagram[0].YMax;
               $scope.YMinAll = observationsDiagram[0].YMin;

               $scope.starNames = observationsDiagram[0].StarNames;
               var i = 0;
               angular.forEach($scope.starNames, function(value, index){
                 if(value == $scope.selectedObjectValue) {
                   $scope.XMax = $scope.XMaxAll[i];
                   $scope.XMin = $scope.XMinAll[i];
                   $scope.YMax = $scope.YMaxAll[i];
                   $scope.YMin = $scope.YMinAll[i];
                 }
                 i++;
               });
               //Diagram options
               var myColors = ["#000000"];
               $scope.options = {
                   chart: {
                       type: 'scatterChart',height: 450,width: 850,color: d3.scale.category10().range(myColors),scatter: {onlyCircles: true},
                       showLegend: false,showDistX: false,showDistY: false,showXAxis: true,showYAxis: true,
                       yDomain: [$scope.YMax,$scope.YMin],xDomain: [$scope.XMin,$scope.XMax],tooltipContent: function(key) {return '<h3>' + key + '</h3>';},duration: 350,
                       xAxis: {axisLabel: 'Julian Date',tickFormat: function(d){return d3.format('.02f')(d);},ticks: 7},
                       yAxis: {axisLabel: 'Flux '+$scope.cutString+' (mag)',tickFormat: function(d){return d3.format('.02f')(d);},axisLabelDistance: -5,ticks: 6},
                       zoom: {enabled: true,scaleExtent: [1, 10],useFixedDomain: false,useNiceScale: false,horizontalOff: false,verticalOff: false,unzoomEventType: 'dblclick.zoom'}
                   }
               };
               return $scope.option
           });

           //The magic to populate data with data
           $scope.data = generateData();
           function generateData() {
               var data = [],
               shapes = ['circle'],
               random = d3.random.normal();

               $scope.ob(function(observationsLCDiagram) {
                     if ($scope.cutString == "U") {
                        $scope.starNames = observationsLCDiagram[0].starNames;
                        $scope.ObservationsTimes = observationsLCDiagram[0].uTimes;
                        $scope.Observations = observationsLCDiagram[0].uObservations;
                     }
                     else if ($scope.cutString == "V") {
                        $scope.starNames = observationsLCDiagram[0].starNames;
                        $scope.ObservationsTimes = observationsLCDiagram[0].vTimes;
                        $scope.Observations = observationsLCDiagram[0].vObservations;
                     }
                     else if ($scope.cutString == "B") {
                        $scope.starNames = observationsLCDiagram[0].starNames;
                        $scope.ObservationsTimes = observationsLCDiagram[0].bTimes;
                        $scope.Observations = observationsLCDiagram[0].bObservations;
                     }
                     else if ($scope.cutString == "R") {
                        $scope.starNames = observationsLCDiagram[0].starNames;
                        $scope.ObservationsTimes = observationsLCDiagram[0].rTimes;
                        $scope.Observations = observationsLCDiagram[0].rObservations;
                     }
                     else if ($scope.cutString == "I") {
                        $scope.starNames = observationsLCDiagram[0].starNames;
                        $scope.ObservationsTimes = observationsLCDiagram[0].iTimes;
                        $scope.Observations = observationsLCDiagram[0].iObservations;
                     }
                     var i = 0
                     var j = 0
                     angular.forEach($scope.starNames, function(value, index){
                             if(value == $scope.selectedObjectValue) {
                                data.push({
                                    key: index,values: []
                                });
                                data[i].values.push({
                                    x: $scope.ObservationsTimes[j], y: $scope.Observations[j], size: 2, shape: shapes[1]
                                });
                                $scope.starName = value;
                                i++;
                                j++;
                             }
                             else {
                                j++;
                             }
                     })
                     $scope.obRange(function(observationsDiagram) {
                        $scope.starNames = observationsDiagram[0].StarNames;
                     });
                     return $scope.starNames, data;
               });
               return data;
           }
           $scope.exampleData = $scope.data;
        }
        //And for logged in user
        else {
           PesronalizedLCDiagramRange.update({filter:$scope.cutString, email:$scope.loggedInUserEmail}, function(response){
                   for(var i = 0; i < response.length; i++) {
                      var j = 0
                      var tab = {}
                      angular.forEach(response[Object.keys(response)[i]], function(value, key){
                              tab[j] = value;
                              j++;
                      });
                   }
               $scope.XMaxAll = tab[0];
               $scope.XMinAll = tab[1];
               $scope.YMaxAll = tab[2];
               $scope.YMinAll = tab[3];


               $scope.starNames = tab[4];
               var i = 0;
               angular.forEach($scope.starNames, function(value, index){
                 if(value == $scope.selectedObjectValue) {
                   $scope.XMax = $scope.XMaxAll[i];
                   $scope.XMin = $scope.XMinAll[i];
                   $scope.YMax = $scope.YMaxAll[i];
                   $scope.YMin = $scope.YMinAll[i];
                 }
                 i++;
               });
               //Diagram options
               var myColors = ["#000000"];
               $scope.options = {
                   chart: {
                       type: 'scatterChart',height: 450,width: 850,color: d3.scale.category10().range(myColors),scatter: {onlyCircles: true},
                       showLegend: false,showDistX: false,showDistY: false,showXAxis: true,showYAxis: true,
                       yDomain: [$scope.YMax,$scope.YMin],xDomain: [$scope.XMin,$scope.XMax],tooltipContent: function(key) {return '<h3>' + key + '</h3>';},duration: 350,
                       xAxis: {axisLabel: 'Julian Date',tickFormat: function(d){return d3.format('.02f')(d);},ticks: 7},
                       yAxis: {axisLabel: 'Flux '+$scope.cutString+' (mag)',tickFormat: function(d){return d3.format('.02f')(d);},axisLabelDistance: -5,ticks: 6},
                       zoom: {enabled: true,scaleExtent: [1, 10],useFixedDomain: false,useNiceScale: false,horizontalOff: false,verticalOff: false,unzoomEventType: 'dblclick.zoom'}
                   }
               };
               return $scope.option
           })
           PesronalizedLCDiagram.update({filter:$scope.cutString, email:$scope.loggedInUserEmail}, function(response){
            //The magic to populate data with data
                   $scope.data = generateData();
                   function generateData() {
                      var data = [],
                      shapes = ['circle'],
                      random = d3.random.normal();
                      for(var i = 0; i < response.length; i++) {
                         var j = 0
                         var tab = {}
                         angular.forEach(response[Object.keys(response)[i]], function(value, key){
                                 tab[j] = value;
                                 j++;
                         });
                      };
                      $scope.starNames = tab[2];
                      $scope.ObservationsTimes = tab[1];
                      $scope.Observations = tab[0];


                             var i = 0
                             var j = 0
                             angular.forEach($scope.starNames, function(value, index){
                                     if(value == $scope.selectedObjectValue) {
                                        data.push({
                                            key: index,values: []
                                        });
                                        data[i].values.push({
                                            x: $scope.ObservationsTimes[j], y: $scope.Observations[j], size: 2, shape: shapes[1]
                                        });
                                        $scope.starName = value;
                                        i++;
                                        j++;
                                     }
                                     else {
                                        j++;
                                     }
                             })
                             return $scope.starNames, data;
                   }
                   $scope.exampleData = $scope.data;
        })
        }
     }})]);


    //------------------------------------------------------HR Diagrams-------------------------------------------------
    //hrDiagramCtrl
	astroApp.controller('hrDiagramCtrl', function($scope) {

	});

    astroApp.controller("cmdCtrl", ['$rootScope', 'getObservationsBVDiagram', 'getObservationsBVDiagramRange',
                                     'getObservationsUBDiagram', 'getObservationsUBDiagramRange', 'getObservationsRIDiagram', 'getObservationsRIDiagramRange',
                                     'getObservationsVIDiagram', 'getObservationsVIDiagramRange', 'getPesronalizedObservationsDiagram',
                                     'getPesronalizedObservationsDiagramRange', '$cookies',
                                  (function ($scope, ObservationsBVDiagram, ObservationsBVDiagramRange, ObservationsUBDiagram, ObservationsUBDiagramRange,
                                  ObservationsRIDiagram, ObservationsRIDiagramRange,ObservationsVIDiagram, ObservationsVIDiagramRange, PesronalizedObservationsDiagram,
                                  PesronalizedObservationsDiagramRange, $cookies) {

       $scope.loggedInUser = $cookies.get('name');
       $scope.isUserLoggedIn = $cookies.get('cook');
       $scope.loggedInUserEmail = $cookies.get('email');
       $scope.isAdminLoggedIn = $cookies.get('admin');


       function sleep (time) {
           return new Promise((resolve) => setTimeout(resolve, time));
       }

       $scope.HRTitle = true;
       $scope.hrDiagrams = ['B-V CMD', 'U-B CMD', 'R-I CMD', 'V-I CMD'];

       $scope.selectedDiagramValue = '';
       $scope.obRange = [];
       $scope.ob = [];

       //select HR diagram type
       $scope.selectDiagram = function (value) {
         $scope.selectedDiagramValue = value;
         $scope.HRTitle = false;

         var cutString = value.substring(0, 3);

                 //Get global data Range
                 if($scope.isUserLoggedIn!='true' || $scope.isAdminLoggedIn==='true') {
                    if (cutString == "B-V") {
                       $scope.ob = ObservationsBVDiagram.query;
                       $scope.obRange = ObservationsBVDiagramRange.query;
                    }
                    else if (cutString == "U-B") {
                       $scope.ob = ObservationsUBDiagram.query;
                       $scope.obRange = ObservationsUBDiagramRange.query;
                    }
                    else if (cutString == "R-I") {
                       $scope.ob = ObservationsRIDiagram.query;
                       $scope.obRange = ObservationsRIDiagramRange.query;
                    }
                    else if (cutString == "V-I") {
                       $scope.ob = ObservationsVIDiagram.query;
                       $scope.obRange = ObservationsVIDiagramRange.query;
                    }

                    $scope.obRange(function(observationsDiagram) {
                       $scope.XMax = observationsDiagram[0].XMax;
                       $scope.XMin = observationsDiagram[0].XMin;
                       $scope.YMax = observationsDiagram[0].YMax;
                       $scope.YMin = observationsDiagram[0].YMin;
                       //Diagram options
                       var myColors = ["black"];
                       $scope.options = {
                           chart: {
                               type: 'scatterChart', height: 550, width: 600, color: d3.scale.category10().range(myColors), scatter: { onlyCircles: true},
                               showLegend: false, showDistX: false, showDistY: false, showXAxis: true, showYAxis: true,
                               yDomain: [$scope.YMax,$scope.YMin], xDomain: [$scope.XMin,$scope.XMax], tooltipContent: function(key) {return '<h3>' + key + '</h3>';},duration: 350,
                               xAxis: {axisLabel: 'Color '+cutString,tickFormat: function(d){return d3.format('.02f')(d);},ticks: 8},
                               yAxis: {axisLabel: 'Absolute Magnitude '+cutString.substring(2,3)+' (mag)',tickFormat: function(d){return d3.format('.02f')(d);},axisLabelDistance: -5,ticks: 10},
                               zoom: {enabled: false,scaleExtent: [1, 10],useFixedDomain: false,useNiceScale: false,horizontalOff: false,verticalOff: false,unzoomEventType: 'dblclick.zoom'
                               }
                           }
                       };
                       return $scope.options
                    });
                 }
                 //Get personalized data Range
                 else {
             		  PesronalizedObservationsDiagramRange.update({hrDiagramType:cutString, email:$scope.loggedInUserEmail}, function(response){
                         for(var i = 0; i < response.length; i++) {
                            var j = 0
                            var tab = {}
                            angular.forEach(response[Object.keys(response)[i]], function(value, key){
                                    tab[j] = value;
                                    j++;
                            });
                         }
                         $scope.XMax = tab[0];
                         $scope.XMin = tab[1];
                         $scope.YMax = tab[2];
                         $scope.YMin = tab[3];
                         //Diagram options
                         var myColors = ["black"];
                         $scope.options = {
                             chart: {
                                 type: 'scatterChart', height: 550, width: 600, color: d3.scale.category10().range(myColors), scatter: { onlyCircles: true},
                                 showLegend: false, showDistX: false, showDistY: false, showXAxis: true, showYAxis: true,
                                 yDomain: [$scope.YMax,$scope.YMin], xDomain: [$scope.XMin,$scope.XMax], tooltipContent: function(key) {return '<h3>' + key + '</h3>';},duration: 350,
                                 xAxis: {axisLabel: 'Color '+cutString,tickFormat: function(d){return d3.format('.02f')(d);},ticks: 8},
                                 yAxis: {axisLabel: 'Absolute Magnitude '+cutString.substring(2,3)+' (mag)',tickFormat: function(d){return d3.format('.02f')(d);},axisLabelDistance: -5,ticks: 10},
                                 zoom: {enabled: false,scaleExtent: [1, 10],useFixedDomain: false,useNiceScale: false,horizontalOff: false,verticalOff: false,unzoomEventType: 'dblclick.zoom'
                                 }
                             }
                         };
                         return $scope.options
                    })
                 }

         //The magic to populate data with data
         $scope.data = [];

         function generateData() {
              var data = [],
              shapes = ['circle'],
              random = d3.random.normal();
              //Get full data
              if($scope.isUserLoggedIn!='true' || $scope.isAdminLoggedIn==='true') {
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
                                 key: value,values: []
                             });
                             data[i].values.push({
                                 x: $scope.ObservationsDifference[i], y: $scope.FilterObservations[i], size: 2, shape: shapes[1]
                             });
                             i++;
                     })
                     return $scope.starNames, data;
                 });
                 return data;
              }
              //Get personalized data
              else {
             	  PesronalizedObservationsDiagram.update({hrDiagramType:cutString, email:$scope.loggedInUserEmail}, function(response){
                      for(var i = 0; i < response.length; i++) {
                         var j = 0
                         var tab = {}
                         angular.forEach(response[Object.keys(response)[i]], function(value, key){
                                 tab[j] = value;
                                 j++;
                         });
                      };
                      $scope.starNames = tab[1];
                      $scope.ObservationsDifference = tab[0];
                      $scope.FilterObservations = tab[2];
                      var i = 0
                      angular.forEach($scope.starNames, function(value, index){
                              data.push({
                                  key: value,values: []
                              });
                              data[i].values.push({
                                  x: $scope.ObservationsDifference[i], y: $scope.FilterObservations[i], size: 2, shape: shapes[1]
                              });
                              i++;
                      })
                      return $scope.starNames, data;
                  })
                  return data;
              }
         }
         $scope.data = generateData();
         $scope.exampleData = $scope.data;
     }})]);



//--------------------------------------------------------Admin Panel---------------------------------------------------

	astroApp.controller('adminCtrl', ['$rootScope', '$cookies', function($scope, $cookies) {
	   $scope.message = 'Admin Panel';
	   $scope.isAdminLoggedIn = $cookies.get('admin');
	}]);

	astroApp.controller('processCtrl', ['$scope', 'usSpinnerService', '$rootScope', 'processData', 'getProcessedData', '$window', '$timeout', '$cookies',
      function($scope, usSpinnerService, $rootScope, ProcessData, GetProcessedData, $window, $timeout, $cookies) {

        $scope.message = 'Admin Panel';
        $scope.isAdminLoggedIn = $cookies.get('admin');
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
             }, 15000);

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
	   $scope.isAdminLoggedIn = $cookies.get('admin');
	   $scope.search = false
	   $scope.stars = false
       $scope.comets = false
       $scope.planetoids = false
	}]);

	astroApp.controller('searchDBCtrl', ['$scope', 'usSpinnerService', '$rootScope', 'searchData', '$window', '$timeout', '$cookies',
      function($scope, usSpinnerService, $rootScope, SearchData, $window, $timeout, $cookies) {

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
   		      if (object.type == "Star") {
                 $scope.Data = response
   		         usSpinnerService.stop('spinner-1');
                 $rootScope.stars = true
              }
   		      else if (object.type == "Comet") {
                 $scope.Data = response
   		         usSpinnerService.stop('spinner-1');
                 $rootScope.comets = true
              }
   		      else if (object.type == "Planetoid") {
                 $scope.Data = response
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



//----------------------------------------------------------Logout-------------------------------------------------------

    //logoutCtrl
	astroApp.controller('logoutCtrl', ['$rootScope', 'login', '$cookies', function ($scope, Login, $cookies) {
	   //put the cookie down
	   $scope.message = 'Logout';
	   $cookies.remove("cook");
	   $cookies.remove("admin");
	   $cookies.remove("name");
	   $cookies.remove("email");
	}]);

    astroApp.controller('goodbyeCtrl', ['$rootScope', 'usSpinnerService', 'login', '$cookies', '$location',
    function ($scope, usSpinnerService, Login, $cookies, $location) {
       $scope.isUserLoggedIn = false;
       $scope.isAdminLoggedIn = false;
             if (!$scope.spinneractive) {
               usSpinnerService.spin('spinner-1');
             };
             $scope.spinneractive = false;
             usSpinnerService.stop('spinner-1');
       $location.path("main");
    }]);


//-----------------------------------------------------------Home-------------------------------------------------------

    //mainCtrl
	astroApp.controller('mainCtrl', ['$rootScope', '$scope', 'login', '$cookies', 'getStatistics', '$uibModal', 'subscribe', '$window', '$timeout',
	                       function ($rootScope, $scope, Login, $cookies, Statistics, $uibModal, Subscribe, $window, $timeout) {
	   $rootScope.isUserLoggedIn = $cookies.get('cook');
	   $rootScope.isAdminLoggedIn = $cookies.get('admin');
	   $rootScope.loggedInUser = $cookies.get('name');
       $scope.Statistics = Statistics.query();

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
      	  Subscribe.save({email:$scope.email}, function(response){
      	  $scope.message = response[Object.keys(response)[0]];
      	           $scope.successTextAlert = "Your email has been added to the subscribe list";
                       $scope.showSuccessAlert = true;
                       // switch flag
                       $scope.switchBool = function (value) {
                           $scope[value] = !$scope[value];
                       };

                    $timeout(function(){
                       $scope.showSuccessAlert = false;
                       }, 5000);
      	  });
       }
	}]);


//----------------------------------------------------------Login-------------------------------------------------------

    //loginCtrl
	astroApp.controller('loginCtrl', function($scope) {
	   $scope.message = 'Login';
	});
	astroApp.controller('ModalLoginCtrl', ['$rootScope', '$scope', '$uibModalInstance', 'usSpinnerService', 'login', '$cookies', '$location', '$uibModal',
	                             function ($rootScope, $scope, $uibModalInstance, usSpinnerService, Login, $cookies, $location, $uibModal) {

      $rootScope.errorFlag = false
      //[Submit]
      $scope.loginUser = function(){
          var password = sjcl.encrypt("password", $scope.password)

   		  Login.update({email:$scope.email,password:password}, function(response){
   		  $scope.message = response[Object.keys(response)[0]];
          if($scope.message == "Wrong credentials"){
   		     $rootScope.isUserLoggedIn = false;
   		     $rootScope.isAdminLoggedIn = false;
   		     $rootScope.errorFlag = true;
   		     }
   		  else if(($scope.message != "Wrong credentials") && ($scope.email != "admin@arqonia.com")){
             if (!$scope.spinneractive) {
               usSpinnerService.spin('spinner-1');
             };
             $cookies.put('email', $scope.email);
             $cookies.put('name', $scope.message);
   		     $cookies.put('cook', true);
   		     $cookies.put('admin', false);
   		     $rootScope.isUserLoggedIn = $cookies.get('cook');
   		     $rootScope.isAdminLoggedIn = $cookies.get('admin');
   		     $rootScope.errorFlag = false;
   		     $rootScope.loggedInUser = $cookies.get('name');
   		     $location.path("main");
   		     $scope.spinneractive = false;
             usSpinnerService.stop('spinner-1');
             $uibModalInstance.dismiss();
   		     }
   		  else {
             if (!$scope.spinneractive) {
               usSpinnerService.spin('spinner-1');
             };
   		     $cookies.put('cook', true);
   		     $cookies.put('admin', true);
   		     $cookies.put('name', $scope.message);
   		     $rootScope.isUserLoggedIn = $cookies.get('cook');
   		     $rootScope.isAdminLoggedIn = $cookies.get('admin');
   		     $rootScope.errorFlag = false;
   		     $rootScope.loggedInUser = $cookies.get('name');
   		     //$rootScope.loggedInUser = $scope.message
   		     $location.path("main");
   		     $scope.spinneractive = false;
             usSpinnerService.stop('spinner-1');
             $uibModalInstance.dismiss();
   		     }
   		  });
      };

          //[Cancel]
          $scope.cancel = function () {
            $uibModalInstance.dismiss('cancel');
          };


                  //Reminder Modal
                  $scope.reminderModal = function () {
                       $uibModalInstance.dismiss();
                       var modalInstance = $uibModal.open({
                         animation: $scope.animationsEnabled,
                         templateUrl: 'reminderModalContent.html',
                         controller: 'PasswordReminderCtrl',
                       });
                  };
    }]);


//-----------------------------------------------------Password Reminder------------------------------------------------

    //loginCtrl
	astroApp.controller('reminderCtrl', function($scope) {
	});

   astroApp.controller('PasswordReminderCtrl', ['$rootScope', '$scope', '$uibModalInstance', 'usSpinnerService', 'reminder', '$cookies', '$location',
	                             function ($rootScope, $scope, $uibModalInstance, usSpinnerService, Reminder, $cookies, $location) {

      $rootScope.errorFlag = false
      //[Send]
      $scope.sendPassword = function(){
   		  Reminder.save({email:$scope.email}, function(response){
             if (!$scope.spinneractive) {
               usSpinnerService.spin('spinner-1');
             };

   		     $rootScope.errorFlag = false
   		     $location.path("login");

             $scope.spinneractive = false;
             usSpinnerService.stop('spinner-1');
             $uibModalInstance.dismiss();
   		     })
      };

          //[Cancel]
          $scope.cancel = function () {
            $uibModalInstance.dismiss('cancel');
          };
     }]);


//--------------------------------------------------------Register------------------------------------------------------

	astroApp.controller('registerCtrl', function($scope) {
	   $scope.message = 'Register';
	});

    astroApp.controller('ModalRegisterCtrl', ['$rootScope', '$scope', '$uibModalInstance', 'usSpinnerService', 'register', '$cookies', '$location',
	                             function ($rootScope, $scope, $uibModalInstance, usSpinnerService, Register, $cookies, $location) {

      $rootScope.errorFlag = false
      //[Submit]
      $scope.addUser = function(){
          var password = sjcl.encrypt("password", $scope.password)

   		  Register.save({name:$scope.name,email:$scope.email,password:password}, function(response){
   		  $scope.message = response[Object.keys(response)[0]];
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
             usSpinnerService.stop('spinner-1');
             $uibModalInstance.dismiss();
   		     }
   		  });
      };

          //[Cancel]
          $scope.cancel = function () {
            $uibModalInstance.dismiss('cancel');
          };
     }]);



//-----------------------------------------------------Reduction--------------------------------------------------------

	astroApp.controller('reductionCtrl', function($scope) {
	});

    astroApp.controller("dataReductionCtrl", ['$rootScope', '$scope', '$timeout', '$window', '$sce', '$compile', '$location', '$route',
                        (function ($rootScope, $scope, $timeout, $window, $sce, $compile, $location, $route) {

        $scope.uploadFlag = true;
                $rootScope.mySync2 = angular.element( document.querySelector( '#sync2' ) );
                $rootScope.mySync2.empty();   //removes element

                $rootScope.mySync1 = angular.element( document.querySelector( '#sync1' ) );
                $rootScope.mySync1.empty();   //removes element


        $scope.imageTypes = ['Raw Images', 'Dark Frames', 'Flat Fields', 'Bias Frames', 'Processed Images'];

        $rootScope.selectType = "SELECT IMAGE TYPE";


      //$scope.loadFiles = function(){

          var file = $scope.myFile;
          if(file) {
             var uploadUrl = __env.apiUrl+"/fileUpload";
             fileUpload.uploadFileToUrl(file, uploadUrl);
             }
          else {
             var file = 'No file';
             }

       //}

        $rootScope.carouselFlag = false;
        $rootScope.selectImageType = function (value) {
          $rootScope.carouselFlag = true;
          $scope.selectedImageType = value;

          if($scope.selectedImageType == "Dark Frames") {
            $scope.uploadFlag = false;
                $rootScope.selectType = "DARK FRAMES";

          }

          if($scope.selectedImageType == "Flat Fields") {
                $rootScope.selectType = "FLAT FIELDS";
                $rootScope.images = ['1', '2'];

                $scope.sync2Content = '<div ng-repeat="image in images"><div style="width:80px;height:81px;margin: 1px auto;" class="owl-items"><div style="padding:1px;padding-right: 1px" class="item"><img width="68" height="80" src="input_fits/vega.jpg" alt="..." style="opacity: 0.5;"></div></div></div>';
                $scope.sync1Content = '<div ng-repeat="image in images"><div style="width:500px;height:490px;margin: 0px;" class="owl-items"><div style="padding:0px;padding-right: 0px;" class="item"><img width="530px" height="460px" src="input_fits/vega.jpg" alt="..."></div></div></div>';


                $scope.uploadFlag = false;

          }

          if($scope.selectedImageType == "Raw Images") {
                $rootScope.selectType = "RAW IMAGES";


                //$rootScope.mySync2.empty();   //removes element
                //$rootScope.mySync1.empty();   //removes element

                $rootScope.images = ['1','2','3'];

                $scope.sync2Content = '<div ng-repeat="image in images"><div style="width:80px;height:81px;margin: 1px auto;" class="owl-items"><div style="padding:1px;padding-right: 1px" class="item"><img width="68" height="80" src="input_fits/vega.jpg" alt="..." style="opacity: 0.5;"></div></div></div>';
                $scope.sync1Content = '<div ng-repeat="image in images"><div style="width:500px;height:490px;margin: 0px;" class="owl-items"><div style="padding:0px;padding-right: 0px;" class="item"><img width="530px" height="460px" src="input_fits/vega.jpg" alt="..."></div></div></div>';

                $scope.uploadFlag = false;

          }

          if($scope.selectedImageType == "Bias Frames") {
                $rootScope.selectType = "BIAS FRAMES";

                                var mySync2 = angular.element( document.querySelector( '#sync2' ) );
                                mySync2.empty();   //removes element

                                var mySync1 = angular.element( document.querySelector( '#sync1' ) );
                                mySync1.empty();   //removes element
                $scope.uploadFlag = false;

          }

          if($scope.selectedImageType == "Processed Images") {
                $rootScope.selectType = "PROCESSED IMAGES";

                                var mySync2 = angular.element( document.querySelector( '#sync2' ) );
                                mySync2.empty();   //removes element

                                var mySync1 = angular.element( document.querySelector( '#sync1' ) );
                                mySync1.empty();   //removes element
                $scope.uploadFlag = true;

          }


        $(document).ready(function() {

              var sync1 = $("#sync1");
              var sync2 = $("#sync2");

              sync1.owlCarousel({
                singleItem : true,
                slideSpeed : 1000,
                navigation: true,
                pagination:false,
                afterAction : syncPosition,
                responsiveRefreshRate : 200,
              });

              sync2.owlCarousel({
                items : 15,
                itemsDesktop      : [1199,10],
                itemsDesktopSmall     : [979,10],
                itemsTablet       : [768,8],
                itemsMobile       : [479,4],
                pagination:false,
                responsiveRefreshRate : 100,
                afterInit : function(el){
                  el.find(".owl-item").eq(0).addClass("synced");
                }
              });

              function syncPosition(el){
                var current = this.currentItem;
                $("#sync2")
                  .find(".owl-item")
                  .removeClass("synced")
                  .eq(current)
                  .addClass("synced")
                if($("#sync2").data("owlCarousel") !== undefined){
                  center(current)
                }
              }

              $("#sync2").on("click", ".owl-item", function(e){
                e.preventDefault();
                var number = $(this).data("owlItem");
                sync1.trigger("owl.goTo",number);
              });

              function center(number){
                var sync2visible = sync2.data("owlCarousel").owl.visibleItems;
                var num = number;
                var found = false;
                for(var i in sync2visible){
                  if(num === sync2visible[i]){
                    var found = true;
                  }
                }

                if(found===false){
                  if(num>sync2visible[sync2visible.length-1]){
                    sync2.trigger("owl.goTo", num - sync2visible.length+2)
                  }else{
                    if(num - 1 === -1){
                      num = 0;
                    }
                    sync2.trigger("owl.goTo", num);
                  }
                } else if(num === sync2visible[sync2visible.length-1]){
                  sync2.trigger("owl.goTo", sync2visible[1])
                } else if(num === sync2visible[0]){
                  sync2.trigger("owl.goTo", num-1)
                }

              }

            });
        }
     })]);


//----------------------------------------------------Photometry--------------------------------------------------------

	astroApp.controller('photometryCtrl', function($scope) {
	});


    astroApp.controller("processPhotometryCtrl", ['$rootScope', '$scope', '$timeout', '$window', '$sce', '$compile', '$location', '$route',
                        (function ($rootScope, $scope, $timeout, $window, $sce, $compile, $location, $route) {

    })]);