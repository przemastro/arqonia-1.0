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

    astroApp.controller("dataReductionCtrl", ['$rootScope', '$scope', '$timeout', '$window', '$sce', '$compile', '$location', '$route', 'fileUpload', '$cookies', '$element',
                        (function ($rootScope, $scope, $timeout, $window, $sce, $compile, $location, $route, fileUpload, $cookies, $element) {

        //cookies
        $scope.loggedInUser = $cookies.get('name');
        $scope.isUserLoggedIn = $cookies.get('cook');
        $scope.loggedInUserEmail = $cookies.get('email');
        $scope.sessionID = $cookies.get('sessionID');


        //Flags
        $scope.imageTypeFlag = false;
        $scope.processFlag = false;
        $scope.linearFlag = 'true';

        $scope.imageTypes = ['Raw Images', 'Dark Frames', 'Flat Fields', 'Bias Frames', 'Processed Images'];

        $rootScope.selectType = "SELECT IMAGE TYPE";


        //Process Data
        $scope.processFiles = function(){
                                    var files = $scope.files;

                                    //use fileUpload service only if file has been uploaded
                                    if(files) {
                                       var uploadUrl = __env.apiUrl+"/inputFits";
                                       fileUpload.uploadFileToUrl(files, uploadUrl);
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

        //Multiple Load Data - to be done
      //$scope.loadFiles = function(){
/*
          var file = $scope.myFile;
          if(file) {
             var uploadUrl = __env.apiUrl+"/fileUpload";
             fileUpload.uploadFileToUrl(file, uploadUrl);
             }
          else {
             var file = 'No file';
             }
*/
       //}


        $rootScope.carouselFlag = false;

        $rootScope.selectImageType = function (value) {
          $rootScope.carouselFlag = true;
          $scope.selectedImageType = value;
          $scope.helpDescription = "";

          //Dark Frames selected
          if($scope.selectedImageType == "Dark Frames") {
                $rootScope.selectType = "DARK FRAMES";
                $scope.imageTypeFlag = true;
          }

          //Flat Fields selected
          if($scope.selectedImageType == "Flat Fields") {
                $rootScope.selectType = "FLAT FIELDS";
                $scope.imageTypeFlag = true;
           }

          //Raw Images selected
          if($scope.selectedImageType == "Raw Images") {
                console.log($scope.processFlag);
                $rootScope.selectType = "RAW IMAGES";
                $scope.imageTypeFlag = true;
                $scope.helpDescription = "You have selected Raw Images option. Please upload files and then click [Convert] button to see your FITS files. If you just want to Process data skip 'Convert' step.";

                $scope.convert = function(){
                                    var files = $scope.files;
                                    $scope.helpDescription = "Great! Go ahead and Process your data";

                                    //use fileUpload service only if file has been uploaded
                                    if(files) {
                                       var uploadUrl = __env.apiUrl+"/inputFits";
                                       fileUpload.uploadFileToUrl(files, uploadUrl);
                                       $scope.filesNumber = files.length;
                                       console.log('test');
                                       console.log($scope.filesNumber);
                                       }
                                    else {
                                       files = 'No file';
                                       console.log(files);
                                       }
                                    console.log(files);
                             $rootScope.images = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'];

                             $rootScope.sync2Content = '<div ng-repeat="image in images"><div style="width:80px;height:81px;margin: 1px auto;" class="owl-items"><div style="padding:1px;padding-right: 1px" class="item"><img width="68" height="80" src="input_fits/linear.jpg" alt="..." style="opacity: 0.5;"></div></div></div>';
                             $rootScope.sync1Content = '<div ng-repeat="image in images"><div style="width:500px;height:540px;margin: 0px;" class="owl-items"><div style="padding:0px;padding-right: 0px;width:630px" class="item"><img width="630px" height="540px" src="input_fits/linear.jpg" alt="..."></div></div></div>';

                           //Carousel binding
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
          }

          //Bias Frames
          if($scope.selectedImageType == "Bias Frames") {
                $rootScope.selectType = "BIAS FRAMES";
                $scope.imageTypeFlag = true;
          }

          //Processed Images
          if($scope.selectedImageType == "Processed Images") {
                $rootScope.selectType = "PROCESSED IMAGES";
                $scope.imageTypeFlag = true;
          }

        }
     })]);