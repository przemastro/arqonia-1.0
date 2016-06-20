'use strict';


var astroApp = angular.module('astroApp.controller', ['ngResource', 'ngAnimate', 'ui.bootstrap', 'smart-table',
'angularjs-datetime-picker', 'angularModalService', 'chart.js', 'angularSpinner', 'nvd3']);

    astroApp.config(['$httpProvider', function ($httpProvider) {
                $httpProvider.defaults.useXDomain = true;
                delete $httpProvider.defaults.headers.common['X-Requested-With'];
            }]);

//---------------------------------------------------Table List---------------------------------------------------------
    //tableListCtrl
	astroApp.controller('tableListCtrl', function($scope) {
	});

    //tableCtrl
    astroApp.controller('tableCtrl', ['$rootScope', '$log', '$routeParams', 'getObservations',
                                     function($scope, $log, $routeParams, Observations) {
       $scope.displayedObservations = [];
       $scope.observations = Observations.query();
       $log.debug($scope.observations);

       $scope.toggleAnimation = function () {
       $scope.animationsEnabled = !$scope.animationsEnabled;

       scope.itemsByPage=15
       };

    }]);

    astroApp.controller('ModalCtrl', ['$scope', '$uibModal', function ($scope, $uibModal) {

       $scope.animationsEnabled = true;


       $scope.addObservation = function () {
            var modalInstance = $uibModal.open({
              animation: $scope.animationsEnabled,
              templateUrl: 'newModalContent.html',
              controller: 'ModalInstanceCtrl',
            });
       };

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
    }]);

    astroApp.controller('ModalInstanceCtrl', ['$scope', '$log', '$uibModalInstance', 'postObservation', function ($scope, $log, $uibModalInstance, NewObservation) {
      $log.debug($scope.name);

      $scope.setFile = function(element) {
                        $scope.$apply(function($scope) {
                            $scope.fileName = element.files[0];
                            $scope.fileType = element.files[0];
                        });

                };

      $scope.addRow = function(){
   		  NewObservation.save({name:$scope.name,startDate:$scope.startDate,endDate:$scope.endDate,
   		                     uFileName:$scope.uFileName,vPhotometry:$scope.vPhotometry,bPhotometry:$scope.bPhotometry}, function(response){
   		  $scope.message = response.message;
   		   });
   		   $log.debug($scope.name);
   		  $uibModalInstance.dismiss();
       };

       $scope.cancel = function () {
         $uibModalInstance.dismiss('cancel');
       };
    }]);

    astroApp.controller('ModalInstanceRemoveCtrl', ['$scope', '$log', '$uibModalInstance', 'removeObservation', 'removePhotometry', function ($scope, $log, $uibModalInstance, RemoveObservation, removePhotometry) {
      $log.debug(removePhotometry);
      $scope.ob = $scope.observations;
      var removePhotometry = parseInt(removePhotometry);

      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };

      $scope.remove = function () {
        //$scope.observations.splice(removePhotometry, 1);
        $scope.removePhotometry = removePhotometry;
        RemoveObservation.save({id:$scope.ob[removePhotometry].id}, function(response){
           $scope.message = response.message;
        });
        $scope.isDisabled = true;
        $uibModalInstance.dismiss();
        return false;
      };
    }]);

    astroApp.controller('ModalInstanceEditCtrl', ['$scope', '$log', '$uibModalInstance', 'updateObservation', 'editPhotometry', function ($scope, $log, $uibModalInstance, UpdateObservation, editPhotometry) {
      $log.debug($scope.name);
      $scope.ob = $scope.observations;
      $scope.editPhotometry = editPhotometry;

      $scope.updateRow = function(){
   		  UpdateObservation.update({id:$scope.ob[editPhotometry].id,name:$scope.name,startDate:$scope.ob[editPhotometry].startDate,endDate:$scope.ob[editPhotometry].endDate,
   		                     uPhotometry:$scope.uPhotometry,vPhotometry:$scope.vPhotometry,bPhotometry:$scope.bPhotometry}, function(response){
   		  $scope.message = response.message;
   		   });
   		   $log.debug($scope.name);
   		  $uibModalInstance.dismiss();
       };
      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };
    }]);

    astroApp.controller('ModalInstanceEditUPhotometryCtrl',  ['$scope', '$log', '$uibModalInstance', 'editUPhotometry', function ($scope, $log, $uibModalInstance, editUPhotometry) {
      $log.debug(editUPhotometry);
      $scope.ob = $scope.observations;
      $scope.editUPhotometry = editUPhotometry;
      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };
    }]);

    astroApp.controller('ModalInstanceEditVPhotometryCtrl', function ($scope, $uibModalInstance, editVPhotometry) {
      $scope.ob = $scope.observations;
      $scope.editVPhotometry = editVPhotometry;
      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };
    });

    astroApp.controller('ModalInstanceEditBPhotometryCtrl', function ($scope, $uibModalInstance, editBPhotometry) {
      $scope.ob = $scope.observations;
      $scope.editBPhotometry = editBPhotometry;
      $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
      };
    });

//---------------------------------------------------------Diagrams-----------------------------------------------------
    //hrDiagramCtrl
	astroApp.controller('hrDiagramCtrl', function($scope) {
	});

	astroApp.controller("observationsCtrl", ['$scope', '$log', 'getObservationsDiagram', function ($scope, $log, ObservationsDiagram)
     {

      $scope.labels = ObservationsDiagram.query(function(observationsDiagram) {
        $scope.labels = observationsDiagram[0].dates;
        return $scope.labels;
      });
      $scope.data = ObservationsDiagram.query(function(observationsDiagram) {
        $scope.data = [observationsDiagram[0].data];
        return $scope.data;
      });
      $log.debug($scope.labels);
              $scope.series = ['Series A'];
              $scope.onClick = function (points, evt) {
                console.log(points, evt);
              };

    }]);

    astroApp.controller("hrCtrl", ['$scope', '$log', 'getObservationsHRDiagram', function ($scope, $log, ObservationsHRDiagram)
     {
      $scope.labels = ObservationsHRDiagram.query(function(observationsHRDiagram) {
        $scope.labels = observationsHRDiagram[0].bvObservationsDifference;
        return $scope.labels;
      });
      $scope.data = ObservationsHRDiagram.query(function(observationsHRDiagram) {
        $scope.data = [observationsHRDiagram[0].vObservations];
        return $scope.data;
      });
              $scope.colours = [{ // default
                "fillColor": "rgba(0, 0, 0, 0)",
                "strokeColor": "rgba(0, 0, 0, 0)",
                "pointColor": "rgba(220,220,220,1)",
                "pointStrokeColor": "#ffffff",
                "pointHighlightFill": "#ffffff",
                "pointHighlightStroke": "rgba(151,187,205,0.8)"}];
              $scope.options = [{"showHorizontalLines" : "false",
                                 "scaleGridLineColor" : "rgba(0,0,0,0)"}];
      $scope.onClick = function (points, evt) {
        console.log(points, evt);
      };
    }]);


    astroApp.controller("cmdCtrl", ['$scope', '$log', 'getObservationsHRDiagram', (function ($scope, $log, ObservationsHRDiagram) {


     ObservationsHRDiagram.query(function(observationsHRDiagram) {
         $scope.XMax = observationsHRDiagram[0].XMax;
         $scope.XMin = observationsHRDiagram[0].XMin;
         $scope.YMax = observationsHRDiagram[0].YMax;
         $scope.YMin = observationsHRDiagram[0].YMin;
         $log.debug($scope.XMax);


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
                               axisLabel: 'B - V',
                               tickFormat: function(d){
                                   return d3.format('.02f')(d);
                               },
                               ticks: 5
                           },
                           yAxis: {
                               axisLabel: 'V',
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
                               $scope.data = generateData();


                           function generateData() {
                                                          var data = [],
                                                              shapes = ['circle'],
                                                              random = d3.random.normal();
                                                         $scope.observations = ObservationsHRDiagram.query(function(observationsHRDiagram) {
                                                           var i = 0
                                                           $scope.starNames = observationsHRDiagram[0].starNames;
                                                           $scope.bvObservationsDifference = observationsHRDiagram[0].bvObservationsDifference;
                                                           $scope.vObservations = observationsHRDiagram[0].vObservations;
                                                                    angular.forEach($scope.starNames, function(value, index){
                                                                            $log.debug(value);
                                                                                  data.push({
                                                                                      key: value,
                                                                                      values: []
                                                                                  });

                                                                                  data[i].values.push({
                                                                                      x: $scope.bvObservationsDifference[i]
                                                                                      , y: $scope.vObservations[i]
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
                                   })]);



//--------------------------------------------------------Admin Panel---------------------------------------------------

	astroApp.controller('adminCtrl', function($scope) {
	   $scope.message = 'Admin Panel';
	});

	astroApp.controller('processCtrl', ['$scope', 'usSpinnerService', '$rootScope', 'processData', 'getProcessedData', '$window', '$timeout',
      function($scope, usSpinnerService, $rootScope, ProcessData, GetProcessedData, $window, $timeout) {
        $scope.message = 'Admin Panel';

        $scope.displayedObservations = [];
        $scope.observations = GetProcessedData.query();

        $scope.startSpin = function() {
          if (!$scope.spinneractive) {
            usSpinnerService.spin('spinner-1');
   		    ProcessData.query(function(response){
   		      $scope.message = response.message;
   		   });
          }
          $timeout(function(){
             $window.location.reload();
             }, 5000);

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
//-----------------------------------------------------------Home-------------------------------------------------------

    //mainCtrl
	astroApp.controller('mainCtrl', function($scope) {
	   $scope.message = 'Home made HR diagram';
	});