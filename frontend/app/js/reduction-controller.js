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




//-----------------------------------------------------Reduction--------------------------------------------------------

	astroApp.controller('reductionCtrl', function($scope) {
	});

    astroApp.controller("dataReductionCtrl", ['$rootScope', '$scope', '$timeout', '$window', '$sce', '$compile', '$location', '$route',
                                              'multipleFileUpload', '$cookies', '$element', 'postReductionImages', 'usSpinnerService', '$q', 'uibButtonConfig',
                        (function ($rootScope, $scope, $timeout, $window, $sce, $compile, $location, $route, multipleFileUpload, $cookies,
                                   $element, ReductionImages, usSpinnerService, $q, buttonConfig) {

        //cookies
        $scope.loggedInUser = $cookies.get('name');
        $scope.isUserLoggedIn = $cookies.get('cook');
        $scope.loggedInUserEmail = $cookies.get('email');
        $rootScope.sessionID = $cookies.get('sessionID');


        //Flags
        $scope.imageTypeFlag = false;
        $scope.processFlag = false;
        $scope.linearFlag = 'true';
        $rootScope.textStep = 'uploaded';
        $scope.imageTypeText = '';

        $scope.objectValue = 'Linear';

        $scope.imageTypes = ['Raw Images', 'Dark Frames', 'Flat Fields', 'Bias Frames', 'Processed Images'];
        $rootScope.selectType = "SELECT IMAGE TYPE";


        //Process Data
        $scope.processFiles = function(){
                                    $rootScope.textStep = 'processed'
                                    var files = $scope.files;

                                    //use fileUpload service only if file has been uploaded
                                    if(files) {
                                       var uploadUrl = __env.apiUrl+"/inputFits";
                                       multipleFileUpload.uploadFileToUrl(files, uploadUrl);
                                       $scope.filesNumber = files.length;
                                       console.log($scope.filesNumber);
                                       }
                                    else {
                                       files = 'No file';
                                       console.log(files);
                                       }
                                    console.log(files);
           $scope.helpDescription = "Perfect! Processing is done. You can now select 'Processed Images' from drop down list or Save your processed frames.";
           $scope.processFlag = true;
           console.log($scope.processFlag);
        }


        $rootScope.carouselFlag = false;

        $rootScope.selectImageType = function (value) {
          $rootScope.carouselFlag = true;
          $scope.selectedImageType = value;
          $scope.helpDescription = "";

          //Dark Frames selected
          if($scope.selectedImageType == "Dark Frames") {
                $rootScope.selectType = "DARK FRAMES";
                $scope.imageTypeFlag = true;
                $scope.imageType = 'Dark';
                $rootScope.numberOfFilesUploaded = $cookies.get('numberOfDarkFilesUploaded');
                if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Dark Frame';} else {$scope.imageTypeText = 'Dark Frames';}
                $scope.helpDescription = "You have selected Dark Frames option. Please upload files and then click [CONVERT] button to see your FITS files. If you just want to Process data skip 'Convert' step.";

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
                           xhr.send(fd)

   		           if (!$scope.spinneractive) {
                     usSpinnerService.spin('spinner-1');
                   };

                   //Call postObservation service...
                    $scope.reductionImages = ReductionImages.save({sessionId:$rootScope.sessionID,files:names,email:$scope.loggedInUserEmail,
                                                          conversionType:$scope.objectValue, imageType:$scope.imageType});
                    $q.all([
                        $scope.reductionImages.$promise
                    ]).then(function(response) {
                       $rootScope.images = response[Object.keys(response)].fileNames;
                       $rootScope.sync2Content = '<div ng-repeat="image in images"><div style="width:80px;height:81px;margin: 1px auto;" class="owl-items"><div style="padding:1px;padding-right: 1px" class="item"><img width="68" height="80" ng-src="inputFits/{{image}}" alt="..." style="opacity: 0.5; " class="rotate180"></div></div></div>';
                       $rootScope.sync1Content = '<div ng-repeat="image in images"><div style="width:500px;height:540px;margin: 0px;" class="owl-items"><div style="padding:0px;padding-right: 0px;width:630px" class="item"><img width="630px" height="540px" ng-src="inputFits/{{image}}" alt="..." class="rotate180"></div></div></div>';
                       $scope.spinneractive = false;
                       usSpinnerService.stop('spinner-1');
                       //Bind Data for Carousel
                       bindData();
                       $cookies.put('numberOfDarkFilesUploaded', response[Object.keys(response)].fileNames.length);
                       $rootScope.numberOfFilesUploaded = $cookies.get('numberOfDarkFilesUploaded')
                       if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Dark Frame';} else {$scope.imageTypeText = 'Dark Frames';}
                       $scope.helpDescription = "Great! Go ahead and Process your data.";
                       });
                }
          }

          //Flat Fields selected
          if($scope.selectedImageType == "Flat Fields") {
                $rootScope.selectType = "FLAT FIELDS";
                $scope.imageTypeFlag = true;
                $scope.imageType = 'Flat';
                $rootScope.numberOfFilesUploaded = $cookies.get('numberOfFlatFilesUploaded');
                if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Flat Field';} else {$scope.imageTypeText = 'Flat Fields';}
                $scope.helpDescription = "You have selected Flat Fields option. Please upload files and then click [CONVERT] button to see your FITS files. If you just want to Process data skip 'Convert' step.";

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
                           xhr.send(fd)

   		           if (!$scope.spinneractive) {
                     usSpinnerService.spin('spinner-1');
                   };
                   //Call postObservation service...
                    $scope.reductionImages = ReductionImages.save({sessionId:$rootScope.sessionID,files:names,email:$scope.loggedInUserEmail,
                                                          conversionType:$scope.objectValue, imageType:$scope.imageType});
                    $q.all([
                        $scope.reductionImages.$promise
                    ]).then(function(response) {
                       $rootScope.images = response[Object.keys(response)].fileNames;
                       $rootScope.sync2Content = '<div ng-repeat="image in images"><div style="width:80px;height:81px;margin: 1px auto;" class="owl-items"><div style="padding:1px;padding-right: 1px" class="item"><img width="68" height="80" ng-src="inputFits/{{image}}" alt="..." style="opacity: 0.5;"></div></div></div>';
                       $rootScope.sync1Content = '<div ng-repeat="image in images"><div style="width:500px;height:540px;margin: 0px;" class="owl-items"><div style="padding:0px;padding-right: 0px;width:630px" class="item"><img width="630px" height="540px" ng-src="inputFits/{{image}}" alt="..."></div></div></div>';
                       $scope.spinneractive = false;
                       usSpinnerService.stop('spinner-1');
                       //Bind Data for Carousel
                       bindData();
                       $cookies.put('numberOfFlatFilesUploaded', response[Object.keys(response)].fileNames.length);
                       $rootScope.numberOfFilesUploaded = $cookies.get('numberOfFlatFilesUploaded')
                       if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Flat Field';} else {$scope.imageTypeText = 'Flat Fields';}
                       $scope.helpDescription = "Great! Go ahead and Process your data.";
                       });
                }
           }

          //Raw Images selected
          if($scope.selectedImageType == "Raw Images") {
                $rootScope.selectType = "RAW IMAGES";
                $scope.imageTypeFlag = true;
                $scope.imageType = 'Raw';
                $rootScope.numberOfFilesUploaded = $cookies.get('numberOfRawFilesUploaded');
                if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Raw Image';} else {$scope.imageTypeText = 'Raw Images';}
                $scope.helpDescription = "You have selected Raw Images option. Please upload files and then click [CONVERT] button to see your FITS files. If you just want to Process data skip 'Convert' step.";

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
                           xhr.send(fd)

   		           if (!$scope.spinneractive) {
                     usSpinnerService.spin('spinner-1');
                   };
                   //Call postObservation service...
                    $scope.reductionImages = ReductionImages.save({sessionId:$rootScope.sessionID,files:names,email:$scope.loggedInUserEmail,
                                                          conversionType:$scope.objectValue, imageType:$scope.imageType});
                    $q.all([
                        $scope.reductionImages.$promise
                    ]).then(function(response) {
                       $rootScope.images = response[Object.keys(response)].fileNames;
                       $rootScope.sync2Content = '<div ng-repeat="image in images"><div style="width:80px;height:81px;margin: 1px auto;" class="owl-items"><div style="padding:1px;padding-right: 1px" class="item"><img width="68" height="80" ng-src="inputFits/{{image}}" alt="..." style="opacity: 0.5;"></div></div></div>';
                       $rootScope.sync1Content = '<div ng-repeat="image in images"><div style="width:500px;height:540px;margin: 0px;" class="owl-items"><div style="padding:0px;padding-right: 0px;width:630px" class="item"><img width="630px" height="540px" ng-src="inputFits/{{image}}" alt="..."></div></div></div>';
                       $scope.spinneractive = false;
                       usSpinnerService.stop('spinner-1');
                       //Bind Data for Carousel
                       bindData();
                       $cookies.put('numberOfRawFilesUploaded', response[Object.keys(response)].fileNames.length);
                       $rootScope.numberOfFilesUploaded = $cookies.get('numberOfRawFilesUploaded')
                       if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Raw Image';} else {$scope.imageTypeText = 'Raw Images';}
                       $scope.helpDescription = "Great! Go ahead and Process your data.";
                       });
                }
          }

          //Bias Frames
          if($scope.selectedImageType == "Bias Frames") {
                $rootScope.selectType = "BIAS FRAMES";
                $scope.imageTypeFlag = true;
                $scope.imageType = 'Bias';
                $rootScope.numberOfFilesUploaded = $cookies.get('numberOfBiasFilesUploaded');
                if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Bias Frame';} else {$scope.imageTypeText = 'Bias Frames';}
                $scope.helpDescription = "You have selected Bias Frames option. Please upload files and then click [CONVERT] button to see your FITS files. If you just want to Process data skip 'Convert' step.";

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
                           xhr.send(fd)



   		           if (!$scope.spinneractive) {
                     usSpinnerService.spin('spinner-1');
                   };
                   //Call postObservation service...
                    $scope.reductionImages = ReductionImages.save({sessionId:$rootScope.sessionID,files:names,email:$scope.loggedInUserEmail,
                                                          conversionType:$scope.objectValue, imageType:$scope.imageType});
                    $q.all([
                        $scope.reductionImages.$promise
                    ]).then(function(response) {
                       $rootScope.images = response[Object.keys(response)].fileNames;
                       $rootScope.sync2Content = '<div ng-repeat="image in images"><div style="width:80px;height:81px;margin: 1px auto;" class="owl-items"><div style="padding:1px;padding-right: 1px" class="item"><img width="68" height="80" ng-src="inputFits/{{image}}" alt="..." style="opacity: 0.5;"></div></div></div>';
                       $rootScope.sync1Content = '<div ng-repeat="image in images"><div style="width:500px;height:540px;margin: 0px;" class="owl-items"><div style="padding:0px;padding-right: 0px;width:630px" class="item"><img width="630px" height="540px" ng-src="inputFits/{{image}}" alt="..."></div></div></div>';
                       $scope.spinneractive = false;
                       usSpinnerService.stop('spinner-1');
                       //Bind Data for Carousel
                       bindData();
                       $cookies.put('numberOfBiasFilesUploaded', response[Object.keys(response)].fileNames.length);
                       $rootScope.numberOfFilesUploaded = $cookies.get('numberOfBiasFilesUploaded')
                       if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Bias Frame';} else {$scope.imageTypeText = 'Bias Frames';}
                       $scope.helpDescription = "Great! Go ahead and Process your data.";
                       });
                }
          }

          //Processed Images
          if($scope.selectedImageType == "Processed Images") {
                $rootScope.selectType = "PROCESSED IMAGES";
                $scope.imageTypeFlag = true;
                $scope.imageType = 'Processed';
                $scope.helpDescription = "You have selected Processed Images option. You can now Save All processed FITS files.";

                $scope.convert = function(){
                   var files = $scope.files;
                   $scope.helpDescription = "Great! Go ahead and Save your data";
                   //use multipleFileUpload service only if file has been uploaded

   		           if (!$scope.spinneractive) {
                     usSpinnerService.spin('spinner-1');
                   };
                   //Call postObservation service...
                    $scope.reductionImages = ReductionImages.save({sessionId:$rootScope.sessionID,files:files.name,email:$scope.loggedInUserEmail,
                                                          conversionType:$scope.objectValue, imageType:$scope.imageType});
                    $q.all([
                        $scope.reductionImages.$promise
                    ]).then(function(response) {
                       $rootScope.images = response[Object.keys(response)].fileNames;
                       $rootScope.sync2Content = '<div ng-repeat="image in images"><div style="width:80px;height:81px;margin: 1px auto;" class="owl-items"><div style="padding:1px;padding-right: 1px" class="item"><img width="68" height="80" ng-src="inputFits/{{image}}" alt="..." style="opacity: 0.5;"></div></div></div>';
                       $rootScope.sync1Content = '<div ng-repeat="image in images"><div style="width:500px;height:540px;margin: 0px;" class="owl-items"><div style="padding:0px;padding-right: 0px;width:630px" class="item"><img width="630px" height="540px" ng-src="inputFits/{{image}}" alt="..."></div></div></div>';
                       $scope.spinneractive = false;
                       usSpinnerService.stop('spinner-1');
                       //Bind Data for Carousel
                       bindData();
                       });
                }
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