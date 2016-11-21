'use strict';


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
                                              'postProcessImages', 'postSaveImages', 'deleteReductionImages',
                        (function ($rootScope, $scope, $timeout, $window, $sce, $compile, $location, $route, multipleFileUpload, $cookies,
                                   $element, ReductionImages, usSpinnerService, $q, buttonConfig, ProcessImages, SaveImages, DeleteReductionImages) {

        //cookies
        $scope.loggedInUser = $cookies.get('name');
        $scope.isUserLoggedIn = $cookies.get('cook');
        $scope.loggedInUserEmail = $cookies.get('email');
        $rootScope.sessionID = $cookies.get('sessionID');


        //Flags
        $scope.imageTypeFlag = false;
        $scope.processedFlag = false;
        $scope.clickProcessFlag = false;
        $scope.formFlag = false;
        $scope.linearFlag = 'true';

        $scope.imageTypeText = '';

        $scope.objectValue = 'Linear';

        $scope.imageTypes = ['Raw Images', 'Dark Frames', 'Flat Fields', 'Bias Frames', 'Processed Images'];
        $rootScope.selectType = "SELECT IMAGE TYPE";



        $rootScope.carouselFlag = false;

        $rootScope.selectImageType = function (value) {
          $rootScope.carouselFlag = true;
          $scope.selectedImageType = value;
          $scope.helpDescription = "";

          //Dark Frames selected
          if($scope.selectedImageType == "Dark Frames") {
                $rootScope.selectType = "DARK FRAMES";
                $rootScope.textStep = 'uploaded';
                $scope.imageTypeFlag = true;
                $scope.imageType = 'Dark';
                $scope.clickProcessFlag = false;
                $scope.formFlag = true;
                $scope.processedFlag = false;
                $rootScope.numberOfFilesUploaded = $cookies.get('numberOfDarkFilesUploaded');
                if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Dark Frame';} else {$scope.imageTypeText = 'Dark Frames';}
                $scope.helpDescription = "You have selected Dark Frames option. Please upload files and then click [LOAD] button to see your FITS files. If you just want to Process data skip 'Load' step.";

                      $scope.setFiles = function(element) {
                       $scope.$apply(function($scope) {
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
                               names.push($scope.files[i].name);
                           }

                   var uploadUrl = __env.apiUrl+"/inputFits"
                           var fd = new FormData()
                           for (var i in $scope.files) {
                               fd.append("files", $scope.files[i]);
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
                                                          conversionType:$scope.objectValue, imageType:$scope.imageType, sessionId:$cookies.get('sessionID')});
                    $q.all([
                        $scope.reductionImages.$promise
                    ]).then(function(response) {
                       $rootScope.images = response[Object.keys(response)].fileNames;
                       $rootScope.sync2Content = '<div ng-repeat="image in images"><div style="width:80px;height:81px;margin: 1px auto;" class="owl-items"><div style="padding:1px;padding-right: 1px" class="item"><img width="70" height="80" ng-src="inputFits/{{image}}" style="opacity: 0.5;"></div></div></div>';
                       $rootScope.sync1Content = '<div ng-repeat="image in images"><div style="width:530px;height:530px;margin: 0px;margin-left:-45px" class="owl-items"><div align="center" style="padding:0px;padding-right: 0px;width:650px" class="item"><img width="auto" height="540px" ng-src="inputFits/{{image}}"></div></div></div>';
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

                $scope.deleteFiles = function(){
                   //Delete Images
                      		           if (!$scope.spinneractive) {
                                        usSpinnerService.spin('spinner-1');
                                      };
                    $scope.deleteReductionImages = DeleteReductionImages.save({email:$scope.loggedInUserEmail, imageType:$scope.imageType, sessionId:$cookies.get('sessionID')});
                    $q.all([
                        $scope.deleteReductionImages.$promise
                    ]).then(function(response) {
                       $scope.spinneractive = false;
                       usSpinnerService.stop('spinner-1');
                       $cookies.put('numberOfDarkFilesUploaded', 0);
                       $rootScope.numberOfFilesUploaded = $cookies.get('numberOfDarkFilesUploaded')
                       if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Dark Frame';} else {$scope.imageTypeText = 'Dark Frames';}
                       $scope.helpDescription = "Great! Go ahead and Process your data.";
                       });
                }
          }

          //Flat Fields selected
          if($scope.selectedImageType == "Flat Fields") {
                $rootScope.selectType = "FLAT FIELDS";
                $rootScope.textStep = 'uploaded';
                $scope.imageTypeFlag = true;
                $scope.imageType = 'Flat';
                $scope.clickProcessFlag = false;
                $scope.formFlag = true;
                $scope.processedFlag = false;
                $rootScope.numberOfFilesUploaded = $cookies.get('numberOfFlatFilesUploaded');
                if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Flat Field';} else {$scope.imageTypeText = 'Flat Fields';}
                $scope.helpDescription = "You have selected Flat Fields option. Please upload files and then click [LOAD] button to see your FITS files. If you just want to Process data skip 'Load' step.";

                      $scope.setFiles = function(element) {
                       $scope.$apply(function($scope) {
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
                               names.push($scope.files[i].name);
                           }

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
                                                          conversionType:$scope.objectValue, imageType:$scope.imageType, sessionId:$cookies.get('sessionID')});
                    $q.all([
                        $scope.reductionImages.$promise
                    ]).then(function(response) {
                       $rootScope.images = response[Object.keys(response)].fileNames;
                       $rootScope.sync2Content = '<div ng-repeat="image in images"><div style="width:80px;height:81px;margin: 1px auto;" class="owl-items"><div style="padding:1px;padding-right: 1px" class="item"><img width="70" height="80" ng-src="inputFits/{{image}}" style="opacity: 0.5;"></div></div></div>';
                       $rootScope.sync1Content = '<div ng-repeat="image in images"><div style="width:530px;height:530px;margin: 0px;margin-left:-45px" class="owl-items"><div align="center" style="padding:0px;padding-right: 0px;width:650px" class="item"><img width="auto" height="540px" ng-src="inputFits/{{image}}"></div></div></div>';
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

                $scope.deleteFiles = function(){
                   //Delete Images
                      		           if (!$scope.spinneractive) {
                                        usSpinnerService.spin('spinner-1');
                                      };
                    $scope.deleteReductionImages = DeleteReductionImages.save({email:$scope.loggedInUserEmail, imageType:$scope.imageType, sessionId:$cookies.get('sessionID')});
                    $q.all([
                        $scope.deleteReductionImages.$promise
                    ]).then(function(response) {
                       $scope.spinneractive = false;
                       usSpinnerService.stop('spinner-1');
                       $cookies.put('numberOfDarkFilesUploaded', 0);
                       $rootScope.numberOfFilesUploaded = $cookies.get('numberOfDarkFilesUploaded')
                       if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Dark Frame';} else {$scope.imageTypeText = 'Dark Frames';}
                       $scope.helpDescription = "Great! Go ahead and Process your data.";
                       });
                }
           }

          //Raw Images selected
          if($scope.selectedImageType == "Raw Images") {
                $rootScope.selectType = "RAW IMAGES";
                $rootScope.textStep = 'uploaded';
                $scope.imageTypeFlag = true;
                $scope.imageType = 'Raw';
                $scope.clickProcessFlag = false;
                $scope.formFlag = true;
                $scope.processedFlag = false;
                $rootScope.numberOfFilesUploaded = $cookies.get('numberOfRawFilesUploaded');
                if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Raw Image';} else {$scope.imageTypeText = 'Raw Images';}
                $scope.helpDescription = "You have selected Raw Images option. Please upload files and then click [LOAD] button to see your FITS files. If you just want to Process data skip 'Load' step.";

                      $scope.setFiles = function(element) {
                       $scope.$apply(function($scope) {
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
                               names.push($scope.files[i].name);
                           }

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
                                                          conversionType:$scope.objectValue, imageType:$scope.imageType, sessionId:$cookies.get('sessionID')});
                    $q.all([
                        $scope.reductionImages.$promise
                    ]).then(function(response) {
                       $rootScope.images = response[Object.keys(response)].fileNames;
                       $rootScope.sync2Content = '<div ng-repeat="image in images"><div style="width:80px;height:81px;margin: 1px auto;" class="owl-items"><div style="padding:1px;padding-right: 1px" class="item"><img width="70" height="80" ng-src="inputFits/{{image}}" style="opacity: 0.5;"></div></div></div>';
                       $rootScope.sync1Content = '<div ng-repeat="image in images"><div style="width:530px;height:530px;margin: 0px;margin-left:-60px" class="owl-items"><div align="center" style="padding:0px;padding-right: 0px;width:650px" class="item"><img width="auto" height="540px" ng-src="inputFits/{{image}}"></div></div></div>';
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

                $scope.deleteFiles = function(){
                   //Delete Images
                      		           if (!$scope.spinneractive) {
                                        usSpinnerService.spin('spinner-1');
                                      };
                    $scope.deleteReductionImages = DeleteReductionImages.save({email:$scope.loggedInUserEmail, imageType:$scope.imageType, sessionId:$cookies.get('sessionID')});
                    $q.all([
                        $scope.deleteReductionImages.$promise
                    ]).then(function(response) {
                       $scope.spinneractive = false;
                       usSpinnerService.stop('spinner-1');
                       $cookies.put('numberOfDarkFilesUploaded', 0);
                       $rootScope.numberOfFilesUploaded = $cookies.get('numberOfDarkFilesUploaded')
                       if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Dark Frame';} else {$scope.imageTypeText = 'Dark Frames';}
                       $scope.helpDescription = "Great! Go ahead and Process your data.";
                       });
                }
          }

          //Bias Frames
          if($scope.selectedImageType == "Bias Frames") {
                $rootScope.selectType = "BIAS FRAMES";
                $rootScope.textStep = 'uploaded';
                $scope.imageTypeFlag = true;
                $scope.imageType = 'Bias';
                $scope.clickProcessFlag = false;
                $scope.formFlag = true;
                $scope.processedFlag = false;
                $rootScope.numberOfFilesUploaded = $cookies.get('numberOfBiasFilesUploaded');
                if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Bias Frame';} else {$scope.imageTypeText = 'Bias Frames';}
                $scope.helpDescription = "You have selected Bias Frames option. Please upload files and then click [LOAD] button to see your FITS files. If you just want to Process data skip 'Load' step.";

                      $scope.setFiles = function(element) {
                       $scope.$apply(function($scope) {
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
                               names.push($scope.files[i].name);
                           }

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
                                                          conversionType:$scope.objectValue, imageType:$scope.imageType, sessionId:$cookies.get('sessionID')});
                    $q.all([
                        $scope.reductionImages.$promise
                    ]).then(function(response) {
                       $rootScope.images = response[Object.keys(response)].fileNames;
                       $rootScope.sync2Content = '<div ng-repeat="image in images"><div style="width:80px;height:81px;margin: 1px auto;" class="owl-items"><div style="padding:1px;padding-right: 1px" class="item"><img width="70" height="80" ng-src="inputFits/{{image}}" style="opacity: 0.5;"></div></div></div>';
                       $rootScope.sync1Content = '<div ng-repeat="image in images"><div style="width:530px;height:530px;margin: 0px;margin-left:-45px" class="owl-items"><div align="center" style="padding:0px;padding-right: 0px;width:650px" class="item"><img width="auto" height="540px" ng-src="inputFits/{{image}}"></div></div></div>';
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

                $scope.deleteFiles = function(){
                   //Delete Images
                      		           if (!$scope.spinneractive) {
                                        usSpinnerService.spin('spinner-1');
                                      };
                    $scope.deleteReductionImages = DeleteReductionImages.save({email:$scope.loggedInUserEmail, imageType:$scope.imageType, sessionId:$cookies.get('sessionID')});
                    $q.all([
                        $scope.deleteReductionImages.$promise
                    ]).then(function(response) {
                       $scope.spinneractive = false;
                       usSpinnerService.stop('spinner-1');
                       $cookies.put('numberOfDarkFilesUploaded', 0);
                       $rootScope.numberOfFilesUploaded = $cookies.get('numberOfDarkFilesUploaded')
                       if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Dark Frame';} else {$scope.imageTypeText = 'Dark Frames';}
                       $scope.helpDescription = "Great! Go ahead and Process your data.";
                       });
                }
          }

          //Processed Images
          if($scope.selectedImageType == "Processed Images") {
                $rootScope.selectType = "PROCESSED IMAGES";
                $rootScope.textStep = 'processed';
                $scope.imageTypeFlag = true;
                $scope.imageType = 'Processed';
                $scope.clickProcessFlag = true;
                $scope.formFlag = false;
                $rootScope.numberOfFilesUploaded = $cookies.get('numberOfProcessedFiles')
                if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Image';} else {$scope.imageTypeText = 'Images';}
                $scope.helpDescription = "You have selected Processed Images option. Click [PROCESS] button to perform data reduction.";

                //Process Data
                $scope.processFiles = function(){
           		   if (!$scope.spinneractive) {
                     usSpinnerService.spin('spinner-1');
                   };

                   //Call
                    $scope.processImages = ProcessImages.save({email:$scope.loggedInUserEmail, sessionId:$cookies.get('sessionID')});
                    $q.all([
                        $scope.processImages.$promise
                    ]).then(function(response) {
                       $rootScope.images = response[Object.keys(response)].fileNames;
                       $rootScope.sync2Content = '<div ng-repeat="image in images"><div style="width:80px;height:81px;margin: 1px auto;" class="owl-items"><div style="padding:1px;padding-right: 1px" class="item"><img width="70" height="80" ng-src="inputFits/{{image}}" style="opacity: 0.5;"></div></div></div>';
                       $rootScope.sync1Content = '<div ng-repeat="image in images"><div style="width:530px;height:530px;margin: 0px;margin-left:-45px" class="owl-items"><div align="center" style="padding:0px;padding-right: 0px;width:650px" class="item"><img width="auto" height="540px" ng-src="inputFits/{{image}}"></div></div></div>';
                       $scope.spinneractive = false;
                       usSpinnerService.stop('spinner-1');
                       //Bind Data for Carousel
                       bindData();
                       $cookies.put('numberOfProcessedFiles', response[Object.keys(response)].fileNames.length);
                       $rootScope.numberOfFilesUploaded = $cookies.get('numberOfProcessedFiles')
                       if($rootScope.numberOfFilesUploaded == 1) {$scope.imageTypeText = 'Image';} else {$scope.imageTypeText = 'Images';}
                       $scope.helpDescription = "Perfect! Processing is done. You can now Save your processed frames.";
                       });

                   $scope.processedFlag = true;
                }

                //Save Data
                $scope.saveFiles = function(){
           		   if (!$scope.spinneractive) {
                     usSpinnerService.spin('spinner-1');
                   };

                   //Call
                    $scope.saveImages = SaveImages.save({email:$scope.loggedInUserEmail, sessionId:$cookies.get('sessionID')});
                    $q.all([
                        $scope.saveImages.$promise
                    ]).then(function(response) {

                       $scope.spinneractive = false;
                       usSpinnerService.stop('spinner-1');
                       $window.open("outputFits/"+$rootScope.sessionID+"_ProcessedImages.zip")

                       });
                }

          }

        }

                                        //Carousel binding
                                    function bindData() {
                                         var $carousel = $(".owl-carousel");

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