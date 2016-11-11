'use strict';


    //var __env = {};

    //if(window){
    //  Object.assign(__env, window.__env);
    //}

 angular.module('astroApp.controller', ['ngResource', 'ngAnimate', 'ui.bootstrap', 'smart-table',
 'angularModalService', 'angularSpinner', 'nvd3', 'ngCookies', 'ngAnimate', 'ngSanitize', 'ngCsv',
 'angular-bind-html-compile', 'angularFileUpload']);

    // Register environment in AngularJS as constant
    astroApp.constant('__env', __env);


//----------------------------------------------------Photometry--------------------------------------------------------

	astroApp.controller('photometryCtrl', function($scope) {
	});


    astroApp.controller("processPhotometryCtrl", ['$rootScope', '$scope', '$timeout', '$window', '$sce', '$compile', '$location', '$route',
                                                  'multipleFileUpload', '$cookies', '$element', 'postReductionImages', 'usSpinnerService',
                                                  '$q', 'uibButtonConfig', '$uibModal',
                        (function ($rootScope, $scope, $timeout, $window, $sce, $compile, $location, $route, multipleFileUpload, $cookies,
                                                                      $element, ReductionImages, usSpinnerService, $q, buttonConfig, $uibModal) {

        //cookies
        $scope.loggedInUser = $cookies.get('name');
        $scope.isUserLoggedIn = $cookies.get('cook');
        $scope.loggedInUserEmail = $cookies.get('email');
        $rootScope.sessionID = $cookies.get('sessionID');

        //Flags
        $scope.photometryTypeFlag = false;
        $scope.convertFlag = false;
        $scope.processFlag = false;
        $scope.linearFlag = 'true';
        $rootScope.textStep = 'uploaded';
        $scope.imageTypeText = '';

        $scope.objectValue = 'Linear';

        $scope.photometryTypes = ['APERTURE PHOTOMETRY'];
        $rootScope.selectType = "SELECT PHOTOMETRY TYPE";


        $rootScope.carouselFlag = false;

        $rootScope.selectPhotometryType = function (value) {
          console.log(value)
          $rootScope.carouselFlag = true;
          $scope.selectedPhotometryType = value;
          $scope.helpDescription = "";

          if($scope.selectedPhotometryType == "APERTURE PHOTOMETRY") {


                $rootScope.selectType = "APERTURE PHOTOMETRY";

                $scope.photometryTypeFlag = true;
                console.log($scope.photometryTypeFlag);
                $scope.photometryType = 'Aperture';
                $rootScope.numberOfFilesUploaded = $cookies.get('numberOfProcessedFiles');
                if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Images';} else {$scope.imageTypeText = 'Images';}
                $scope.helpDescription = "You have selected Aperture Photometry option. Please upload files and then click [CONVERT] button to see your FITS files.";

                      $scope.setFiles = function(element) {
                       $scope.$apply(function($scope) {
                         console.log('files:', element.files);
                         // Turn the FileList object into an Array
                           $scope.files = []
                           for (var i = 0; i < element.files.length; i++) {
                             $scope.files.push(element.files[i])
                           }
                         });
                       };

                $scope.convert = function(){
                   var names = [];
                           for (var i in $scope.files) {
                               console.log(i);
                               console.log($scope.files[i].name);
                               names.push($scope.files[i].name);
                           }
                   console.log(names);

                   var uploadUrl = __env.apiUrl+"/inputFits"
                           var fd = new FormData()
                           for (var i in $scope.files) {
                               fd.append("files", $scope.files[i])
                           }
                           var xhr = new XMLHttpRequest()
                           xhr.open("POST", uploadUrl)
                           xhr.setRequestHeader('Email', $scope.loggedInUserEmail);
                           xhr.setRequestHeader('SessionId', $cookies.get('sessionID'));
                           xhr.send(fd)

   		           if (!$scope.spinneractive) {
                     usSpinnerService.spin('spinner-1');
                   };

                   //Call postObservation service...
                    $scope.reductionImages = ReductionImages.save({sessionId:$rootScope.sessionID,files:names,email:$scope.loggedInUserEmail,
                                                          conversionType:$scope.objectValue, imageType:'Processed', sessionId:$cookies.get('sessionID')});
                    $q.all([
                        $scope.reductionImages.$promise
                    ]).then(function(response) {
                       $rootScope.images = response[Object.keys(response)].fileNames;
                       console.log()
                       $rootScope.sync2Content = '<div ng-repeat="image in images"><div style="width:80px;height:81px;margin: 1px auto;" class="owl-items"><div style="padding:1px;padding-right: 1px" class="item"><img width="68" height="80" ng-src="inputFits/{{image}}" style="opacity: 0.5; "></div></div></div>';
                       $rootScope.sync1Content = '<div ng-repeat="image in images"><div style="width:530px;height:540px;margin: 0px;margin-left:-60px" class="owl-items"><div style="padding:0px;padding-right: 0px;width:650px" class="item"><img width="530px" height="540px" ng-src="inputFits/{{image}}"></div></div></div>';
                       $scope.spinneractive = false;
                       usSpinnerService.stop('spinner-1');
                       //Bind Data for Carousel
                       bindData();
                       $cookies.put('numberOfProcessedFiles', response[Object.keys(response)].fileNames.length);
                       $rootScope.numberOfProcessedFiles = $cookies.get('numberOfProcessedFiles')
                       if($rootScope.numberOfProcessedFiles == 1) {$scope.imageTypeText = 'Image';} else {$scope.imageTypeText = 'Images';}
                       $scope.helpDescription = "Great! Go ahead and Measure Photometry.";
                       $scope.convertFlag = true;
                       });
                }

                 //Measure Photometry Modal
                 $scope.measure = function () {
                      var modalInstance = $uibModal.open({
                        animation: $scope.animationsEnabled,
                        templateUrl: 'measureContent.html',
                        controller: 'MeasureCtrl',
                      });
                 };

          }

        }


                                        //Carousel binding
                                    function bindData() {    $(document).ready(function() {

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


    //---------------------------------------------------Measure modal's details--------------------------------------------
        astroApp.controller('MeasureCtrl', ['$rootScope', '$scope', '$uibModalInstance', 'postPhotometry', '$uibModal', '$window', '$timeout', '$cookies', 'usSpinnerService', '$q',
                                         function ($rootScope, $scope, $uibModalInstance, NewPhotometry, $uibModal, $window, $timeout, $cookies, usSpinnerService, $q) {


            //Measure Photometry
            $scope.processFiles = function(){

               $rootScope.textStep = 'processed'
                                 if (!$scope.spinneractive) {
                                   usSpinnerService.spin('spinner-1');
                                 };

              console.log('credentials');
              $scope.newPhotometry = NewPhotometry.save({ref1:$scope.ref1,ref2:$scope.ref2,object:$scope.object,
                                julianDate:$scope.julianDate,shift:$scope.shift,email:$cookies.get('email'), sessionId:$cookies.get('sessionID')});

                $q.all([
                        $scope.newPhotometry.$promise
                    ]).then(function(response) {
       		              $scope.message = response.message;
       		              console.log('response');
       		              console.log(response.message);
           		          var globalObject = [];
                          var len = response.length;
                          console.log('len');
                          console.log(len);
                          for(var i = 0; i < len; i++) {
                             var newObject = {}
                             angular.forEach(response[Object.keys(response)[i]], function(value, key){
                                  newObject[key] = value;
                                  console.log(value);
                              });
                              globalObject.push(newObject);
                          }
                          $scope.spinneractive = false;
                          usSpinnerService.stop('spinner-1');
                       });

               $scope.helpDescription = "Perfect! Photometry has been calculated. You can now save your results.";
               $scope.processFlag = true;
               console.log($scope.processFlag);

       		  //...and close modal
       		  $uibModalInstance.dismiss();

                  // switch flag
                  $rootScope.switchBool = function (value) {
                      $rootScope[value] = !$rootScope[value];
                  };
              $timeout(function(){
                 $rootScope.showSuccessAlert = false;
                 }, 5000);
            }
          //[Cancel]
          $scope.cancel = function () {
            $uibModalInstance.dismiss('cancel');
          };
        }]);