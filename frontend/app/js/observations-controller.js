'use strict';


    //var __env = {};

    //if(window){
    //  Object.assign(__env, window.__env);
    //}

 angular.module('astroApp.controller', ['ngResource', 'ngAnimate', 'ui.bootstrap', 'smart-table',
 'angularModalService', 'angularSpinner', 'nvd3', 'ngCookies', 'ngAnimate', 'ngSanitize', 'ngCsv', 'angular-bind-html-compile']);

    // Register environment in AngularJS as constant
    astroApp.constant('__env', __env);



//-------------------------------------------------Observations---------------------------------------------------------

    //------------------------------------------------Table List--------------------------------------------------------
    //tableListCtrl
	astroApp.controller('tableListCtrl', function($scope, $window) {
	});

    //tableCtrl
    astroApp.controller('tableCtrl', ['$rootScope', '$routeParams', 'getObservations', 'getUserObservations', '$cookies', 'usSpinnerService',
                                     function($scope, $routeParams, Observations, UserObservations, $cookies, usSpinnerService) {

       //Just to clear table when new user is logged in
       $scope.displayedObservations = [];
       $scope.observations = [];

       //Get the cookies of logged in user
       $scope.loggedInUser = $cookies.get('name');
       $scope.isUserLoggedIn = $cookies.get('cook');
       $scope.loggedInUserEmail = $cookies.get('email');
       $scope.isAdminLoggedIn = $cookies.get('admin');
       $scope.sessionID = $cookies.get('sessionID');

       //Verify who has logged in and populate table with appropriate data
       if(!$scope.isUserLoggedIn) { //nobody is logged in
       //Get data
                                       if (!$scope.spinneractive) {
                                         usSpinnerService.spin('spinner-1');
                                       };
          $scope.displayedObservations = [];
          $scope.observations = Observations.query();
          //console.log($scope.undefined);
                                         $scope.spinneractive = false;
                                         usSpinnerService.stop('spinner-1');
       }
       else if ($scope.isAdminLoggedIn==='true') { //Admin
                                              if (!$scope.spinneractive) {
                                                usSpinnerService.spin('spinner-1');
                                              };
          $scope.displayedObservations = [];
          $scope.observations = Observations.query();
                                                   $scope.spinneractive = false;
                                                   usSpinnerService.stop('spinner-1');
       }
       else if($scope.isUserLoggedIn) { //User
                                                     if (!$scope.spinneractive) {
                                                       usSpinnerService.spin('spinner-1');
                                                     };
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
           $scope.spinneractive = false;
           usSpinnerService.stop('spinner-1');
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
       $scope.sessionID = $cookies.get('sessionID');

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
            }, 5000);
         $timeout(function(){
            $window.location.reload();
            }, 5000);
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


        $scope.objectValue = 'Star';
        $scope.radioValue = 'Yes';

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
          console.log(file);

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
   		  console.log(file);
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
    astroApp.controller('ModalInstanceRemoveCtrl', ['$rootScope', '$scope', '$uibModalInstance', 'removeObservation', 'removePhotometry', '$uibModal', '$window', '$timeout', '$cookies', 'usSpinnerService', 'getObservations', 'getUserObservations',
                                           function ($rootScope, $scope, $uibModalInstance, RemoveObservation, removePhotometry, $uibModal, $window, $timeout, $cookies, usSpinnerService, Observations, UserObservations) {

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
        $rootScope.displayedObservations = [];
        $rootScope.observations = [];
        RemoveObservation.save({id:removePhotometry,email:$scope.loggedInUserEmail,name:$scope.removePhotometryName}, function(response){
           $scope.message = response.message;

        });

                  if (!$scope.spinneractive) {
                    usSpinnerService.spin('spinner-1');
                  };
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
                  $rootScope.displayedObservations = [];
                  $rootScope.observations = globalObject;
                  console.log($rootScope.observations);
                   $scope.spinneractive = false;
                   usSpinnerService.stop('spinner-1');
                  })

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
    astroApp.controller('ModalInstanceEditCtrl', ['$rootScope', '$scope', '$uibModalInstance', 'updateObservation', 'editPhotometry', 'fileUpload', '$uibModal', '$window', '$timeout', '$cookies', 'usSpinnerService', 'getObservations', 'getUserObservations',
                                         function ($rootScope, $scope, $uibModalInstance, UpdateObservation, editPhotometry, fileUpload, $uibModal, $window, $timeout, $cookies, usSpinnerService, Observations, UserObservations) {


      $scope.ob = $scope.observations;
      //editPhotometry is an observation.id so I can keep the correct index of an observation in table list
      $scope.editPhotometry = editPhotometry;

     //Pre-populated radio buttons
      var len = $scope.ob.length;
      for(var i = 0; i < len; i++) {
         if($scope.ob[i].id == editPhotometry) {
            $scope.objectTypeFlag = $scope.ob[i].objectType;
            $scope.objectVerifiedFlag = $scope.ob[i].objectVerified;
            $scope.objectValue = $scope.objectTypeFlag;
            $scope.radioValue = $scope.objectVerifiedFlag;
         }
      }

      $rootScope.starFlag = 'false';
      $rootScope.planetoidFlag = 'false';
      $rootScope.cometFlag = 'false';
      $rootScope.verifiedTrueFlag = 'false';
      $rootScope.verifiedFalseFlag = 'false';

      if($scope.objectTypeFlag == 'Star') {
         $rootScope.starFlag = 'true';
      }
      else if ($scope.objectTypeFlag == 'Planetoid') {
         $rootScope.planetoidFlag = 'true';
      }
      else if ($scope.objectTypeFlag == 'Comet') {
         $rootScope.cometFlag = 'true';
      }


      if($scope.objectVerifiedFlag == 'True') {
         $rootScope.verifiedTrueFlag = 'true';
      }
      else if($scope.objectVerifiedFlag == 'False') {
         $rootScope.verifiedFalseFlag = 'true';
      }

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
      console.log($scope.objectValue);
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
                            $rootScope.displayedObservations = [];
                            $rootScope.observations = [];

          //Call updateObservation service...
   		  UpdateObservation.update({id:$scope.ob[editPhotometry2].id,name:$scope.name,startDate:$scope.startDate,
   		                            endDate:$scope.endDate,
   		                            uFileName:file.name,vFileName:file2.name,bFileName:file3.name,
   		                            rFileName:file4.name,iFileName:file5.name,objectType:$scope.objectValue,
                                    verified:$scope.radioValue,email:$scope.loggedInUserEmail}, function(response){
   		  $scope.message = response.message;
   		  });

   		                    if (!$scope.spinneractive) {
                              usSpinnerService.spin('spinner-1');
                            };
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
                            $rootScope.displayedObservations = [];
                            $rootScope.observations = globalObject;
                            console.log($rootScope.observations);
                             $scope.spinneractive = false;
                             usSpinnerService.stop('spinner-1');
                            })

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