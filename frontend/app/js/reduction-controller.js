'use strict';


    //var __env = {};

    //if(window){
    //  Object.assign(__env, window.__env);
    //}

 angular.module('astroApp.controller', ['ngResource', 'ngAnimate', 'ui.bootstrap', 'smart-table',
 'angularModalService', 'angularSpinner', 'nvd3', 'ngCookies', 'ngAnimate', 'ngSanitize', 'ngCsv', 'angular-bind-html-compile']);

    // Register environment in AngularJS as constant
    astroApp.constant('__env', __env);




//-----------------------------------------------------Reduction--------------------------------------------------------

	astroApp.controller('reductionCtrl', function($scope) {
	});

    astroApp.controller("dataReductionCtrl", ['$rootScope', '$scope', '$timeout', '$window', '$sce', '$compile', '$location', '$route', 'fileUpload',
                        (function ($rootScope, $scope, $timeout, $window, $sce, $compile, $location, $route, fileUpload) {

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

                var file = $scope.myFile;
                //use fileUpload service only if file has been uploaded in modal
                if(file) {
                   var uploadUrl = __env.apiUrl+"/input_fits";
                   fileUpload.uploadFileToUrl(file, uploadUrl);
                   }
                else {
                   var file = 'No file';
                   }
                console.log(file);
                //$rootScope.mySync2.empty();   //removes element
                //$rootScope.mySync1.empty();   //removes element

                $rootScope.images = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'];

                $scope.sync2Content = '<div ng-repeat="image in images"><div style="width:80px;height:81px;margin: 1px auto;" class="owl-items"><div style="padding:1px;padding-right: 1px" class="item"><img width="68" height="80" src="input_fits/linear.png" alt="..." style="opacity: 0.5;"></div></div></div>';
                $scope.sync1Content = '<div ng-repeat="image in images"><div style="width:500px;height:540px;margin: 0px;" class="owl-items"><div style="padding:0px;padding-right: 0px;width:630px" class="item"><img width="630px" height="540px" src="input_fits/linear.png" alt="..."></div></div></div>';

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