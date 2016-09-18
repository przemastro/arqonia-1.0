
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

