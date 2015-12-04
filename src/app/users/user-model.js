(function() {
  'use strict';

  var app = angular.module('radar.users');

  app.factory('UserModel', ['Model', 'store', '_', function(Model, store, _) {
    function UserModel(modelName, data) {
      var i;

      if (data === undefined) {
        data = {};
      }

      if (data.cohorts === undefined) {
        data.cohorts = [];
      } else {
        var cohorts = [];

        for (i = 0; i < data.cohorts.length; i++) {
          var rawCohort = data.cohorts[i];
          cohorts.push(store.pushToStore(store.create('cohort-users', rawCohort)));
        }

        data.cohorts = cohorts;
      }

      if (data.organisations === undefined) {
        data.organisations = [];
      } else {
        var organisations = [];

        for (i = 0; i < data.organisations.length; i++) {
          var rawOrganisation = data.organisations[i];
          organisations.push(store.pushToStore(store.create('organisation-users', rawOrganisation)));
        }

        data.organisations = organisations;
      }

      Model.call(this, modelName, data);
    }

    UserModel.prototype = Object.create(Model.prototype);

    UserModel.prototype.getUnits = function() {
      return _.filter(this.organisations, function(x) {
        return x.organisation.type === 'UNIT';
      });
    };

    return UserModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('users', 'UserModel');
  }]);
})();
