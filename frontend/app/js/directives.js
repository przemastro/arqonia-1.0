
astroApp.directive('fileModel', ['$parse', function ($parse) {
                       return {
                          restrict: 'A',
                          link: function(scope, element, attrs) {
                             var model = $parse(attrs.fileModel);
                             var modelSetter = model.assign;

                             element.bind('change', function(){
                                scope.$apply(function(){
                                   modelSetter(scope, element[0].files[0]);
                                });
                             });
                          }
                       };
}]);

astroApp.directive('bindHtmlCompile', ['$compile', function ($compile) {
        return {
            restrict: 'A',
            link: function (scope, element, attrs) {
                scope.$watch(function () {
                    return scope.$eval(attrs.bindHtmlCompile);
                }, function (value) {
                    element.html(value);
                    $compile(element.contents())(scope);
                });
            }
        };
    }]);

astroApp.directive('ngFileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            var model = $parse(attrs.ngFileModel);
            var isMultiple = attrs.multiple;
            var modelSetter = model.assign;
            element.bind('change', function () {
                var values = [];
                angular.forEach(element[0].files, function (item) {
                    var value = {
                       // File Name
                        name: item.name,
                        //File Size
                        size: item.size,
                        //File URL to view
                        //url: URL.createObjectURL(item),
                        // File Input Value
                        _file: item
                    };
                    values.push(value);
                });
                scope.$apply(function () {
                    if (isMultiple) {
                        modelSetter(scope, values);
                    } else {
                        modelSetter(scope, values[0]);
                    }
                });
            });
        }
    };
}]);

astroApp.directive('dynamic', function ($compile) {
          return {
            restrict: 'A',
            replace: true,
            link: function (scope, ele, attrs) {
              scope.$watch(attrs.dynamic, function(html) {
                ele.html(html);
                $compile(ele.contents())(scope);
              });
            }
          };
        });