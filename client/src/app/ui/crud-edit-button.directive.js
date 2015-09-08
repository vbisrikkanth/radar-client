(function() {
  'use strict';

  var app = angular.module('radar.ui');

  app.directive('crudEditButton', function() {
    return {
      scope: {
        item: '='
      },
      template: '<button ng-click="action()" ng-if="permission" ng-disabled="!enabled" type="button" class="btn btn-primary">Edit</button>',
      link: function(scope) {
        scope.action = function() {
          scope.$parent.edit(scope.item);
        };

        scope.$watch(function() {
          return scope.$parent.editEnabled(scope.item);
        }, function(value) {
          scope.enabled = value;
        });

        scope.$watch(function() {
          return scope.$parent.editPermission(scope.item);
        }, function(value) {
          scope.permission = value;
        });
      }
    };
  });
})();