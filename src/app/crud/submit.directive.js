(function() {
  'use strict';

  var app = angular.module('radar.crud');

  app.directive('crudSubmit', ['$parse', function($parse) {
    return {
      require: 'form',
      link: function(scope, element, attrs, formCtrl) {
        element.on('submit', function(event) {
          event.preventDefault();

          scope.$apply(function() {
            var promise = $parse(attrs.crudSubmit)(scope);

            promise.then(function() {
              formCtrl.$setPristine(true);
            });
          });
        });
      }
    };
  }]);
})();

