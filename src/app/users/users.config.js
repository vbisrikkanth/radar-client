(function() {
  'use strict';

  var app = angular.module('radar.users');

  app.config(function($stateProvider) {
    $stateProvider.state('users', {
      url: '/users',
      templateUrl: 'app/users/user-list.html',
      controller: function($scope, $controller, UserListController) {
        $controller(UserListController, {$scope: $scope});
      }
    });

    $stateProvider.state('user', {
      url: '/users/:userId',
      templateUrl: 'app/users/user-detail.html',
      controller: function($scope, user) {
        $scope.user = user;
      },
      resolve: {
        user: function($stateParams, store) {
          return store.findOne('users', $stateParams.userId);
        }
      }
    });
  });
})();

