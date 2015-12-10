(function() {
  'use strict';

  var app = angular.module('radar.auth');

  /** Service for authorization actions */
  function authService(
    session,
    $q,
    store,
    adapter
  ) {
    return {
      login: login,
      logout: logout,
      forgotUsername: forgotUsername,
      forgotPassword: forgotPassword,
      resetPassword: resetPassword
    };

    function errorHandler(promise) {
      if (promise === undefined) {
        promise = $q;
      }

      return function(response) {
        if (response.status === 422) {
          return promise.reject(response.data.errors);
        } else {
          return promise.reject();
        }
      };
    }

    /** Log the user in */
    function login(credentials) {
      var deferred = $q.defer();

      adapter.post('/login', {}, credentials)
        .then(function(response) {
          var userId = response.data.userId;
          var token = response.data.token;

          session.setToken(token);

          return store.findOne('users', userId)
            .then(function(user) {
              session.login(user);
              deferred.resolve(user);
            })
            ['catch'](function() {
              deferred.reject();
            });
        })
        ['catch'](errorHandler(deferred));

      return deferred.promise;
    }

    /** Log the user out */
    function logout() {
      var deferred = $q.defer();

      if (session.isAuthenticated) {
        adapter.post('/logout')['finally'](function() {
          session.logout();
          deferred.resolve();
        });
      } else {
        deferred.resolve();
      }

      return deferred.promise;
    }

    /** Request a username reminder */
    function forgotUsername(email) {
      return adapter.post('/forgot-username', {}, {email: email})['catch'](errorHandler());
    }

    /** Request a reset password link */
    function forgotPassword(username, email) {
      return adapter.post('/forgot-password', {}, {username: username, email: email})['catch'](errorHandler());
    }

    /** Reset a password */
    function resetPassword(token, username, password) {
      var data = {
        token: token,
        username: username,
        password: password
      };

      return adapter.post('/reset-password', {}, data)['catch'](errorHandler());
    }
  }

  authService.$inject = [
    'session',
    '$q',
    'store',
    'adapter'
  ];

  app.factory('authService', authService);
})();
