'use strict';


    //var __env = {};

    //if(window){
    //  Object.assign(__env, window.__env);
    //}

 angular.module('astroApp.controller', ['ngResource', 'ngAnimate', 'ui.bootstrap', 'smart-table',
 'angularModalService', 'angularSpinner', 'nvd3', 'ngCookies', 'ngAnimate', 'ngSanitize', 'ngCsv', 'angular-bind-html-compile']);

    // Register environment in AngularJS as constant
    astroApp.constant('__env', __env);



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
                                   'getPesronalizedLCDiagramRange','getPesronalizedLCDiagram','$cookies', 'usSpinnerService',
                                  (function ($scope, ObservationsLCUDiagramRange, ObservationsLCUDiagram, ObservationsLCVDiagramRange, ObservationsLCVDiagram,
                                  ObservationsLCBDiagramRange, ObservationsLCBDiagram, ObservationsLCRDiagramRange, ObservationsLCRDiagram,
                                  ObservationsLCIDiagramRange, ObservationsLCIDiagram, PesronalizedLCDiagramRange, PesronalizedLCDiagram, $cookies, usSpinnerService) {

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
                          if (!$scope.spinneractive) {
                            usSpinnerService.spin('spinner-1');
                          };

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
                                                     $scope.spinneractive = false;
                                                     usSpinnerService.stop('spinner-1');
                });
             }
             else if ($scope.cutString == "V") {
                $scope.obRange = ObservationsLCVDiagramRange.query;
                $scope.selectedFilter = true;
                $scope.obRange(function(observationsDiagram) {
                    $scope.starNames = observationsDiagram[0].StarNames;
                                                     $scope.spinneractive = false;
                                                     usSpinnerService.stop('spinner-1');
                });
             }
             else if ($scope.cutString == "B") {
                $scope.obRange = ObservationsLCBDiagramRange.query;
                $scope.selectedFilter = true;
                $scope.obRange(function(observationsDiagram) {
                    $scope.starNames = observationsDiagram[0].StarNames;
                                                     $scope.spinneractive = false;
                                                     usSpinnerService.stop('spinner-1');
                });
             }
             else if ($scope.cutString == "R") {
                $scope.obRange = ObservationsLCRDiagramRange.query;
                $scope.selectedFilter = true;
                $scope.obRange(function(observationsDiagram) {
                    $scope.starNames = observationsDiagram[0].StarNames;
                                                     $scope.spinneractive = false;
                                                     usSpinnerService.stop('spinner-1');
                });
             }
             else if ($scope.cutString == "I") {
                $scope.obRange = ObservationsLCIDiagramRange.query;
                $scope.selectedFilter = true;
                $scope.obRange(function(observationsDiagram) {
                    $scope.starNames = observationsDiagram[0].StarNames;
                                                     $scope.spinneractive = false;
                                                     usSpinnerService.stop('spinner-1');
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
                                                      $scope.spinneractive = false;
                                                      usSpinnerService.stop('spinner-1');
             })
          }
       }
      $scope.selectedObjectValue = '';

      //select object from drop down for selected filter
      $scope.selectObject = function (object) {
                                if (!$scope.spinneractive) {
                                  usSpinnerService.spin('spinner-1');
                                };
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
                               $scope.spinneractive = false;
                               usSpinnerService.stop('spinner-1');
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
                               $scope.spinneractive = false;
                               usSpinnerService.stop('spinner-1');
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
                                     'getPesronalizedObservationsDiagramRange', '$cookies', 'usSpinnerService',
                                  (function ($scope, ObservationsBVDiagram, ObservationsBVDiagramRange, ObservationsUBDiagram, ObservationsUBDiagramRange,
                                  ObservationsRIDiagram, ObservationsRIDiagramRange,ObservationsVIDiagram, ObservationsVIDiagramRange, PesronalizedObservationsDiagram,
                                  PesronalizedObservationsDiagramRange, $cookies, usSpinnerService) {

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
              $scope.selectedDiagramValue = '';
              $scope.obRange = [];
              $scope.ob = [];
                       $scope.data = [];
                       $scope.exampleData = [];
                                       if (!$scope.spinneractive) {
                                         usSpinnerService.spin('spinner-1');
                                       };
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
                               noData: '',
                               yDomain: [$scope.YMax,$scope.YMin], xDomain: [$scope.XMin,$scope.XMax], tooltipContent: function(key) {return '<h3>' + key + '</h3>';},duration: 350,
                               xAxis: {axisLabel: 'Color '+cutString,tickFormat: function(d){return d3.format('.02f')(d);},ticks: 8},
                               yAxis: {axisLabel: 'Absolute Magnitude '+cutString.substring(2,3)+' (mag)',tickFormat: function(d){return d3.format('.02f')(d);},axisLabelDistance: -5,ticks: 10},
                               zoom: {enabled: true,scaleExtent: [1, 10],useFixedDomain: false,useNiceScale: false,horizontalOff: false,verticalOff: false,unzoomEventType: 'dblclick.zoom'
                               }
                           }
                       };
                                                      $scope.spinneractive = false;
                                                      usSpinnerService.stop('spinner-1');
                       return $scope.options
                    });
                 }
                 //Get personalized data Range
                 else {
                      $scope.XMax = [];
                      $scope.XMin = [];
                      $scope.YMax = [];
                      $scope.YMin = [];
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
                                 noData: '',
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
         $scope.exampleData = [];

         function generateData() {
              $scope.starNames = [];
              $scope.ObservationsDifference = [];
              $scope.FilterObservations = [];
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
                  $scope.starNames = [];
                  $scope.ObservationsDifference = [];
                  $scope.FilterObservations = [];
                  data = [];

             	  PesronalizedObservationsDiagram.update({hrDiagramType:cutString, email:$scope.loggedInUserEmail}, function(response){
             	                                                          $scope.spinneractive = false;
                                                                          usSpinnerService.stop('spinner-1');
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
