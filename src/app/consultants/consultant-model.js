(function() {
  'use strict';

  var app = angular.module('radar.consultants');

  app.factory('ConsultantModel', ['Model', function(Model) {
    function ConsultantModel(modelName, data) {
      if (data.groups === undefined) {
        data.groups = [];
      }

      Model.call(this, modelName, data);
    }

    ConsultantModel.prototype = Object.create(Model.prototype);

    ConsultantModel.prototype.toString = function() {
      return this.firstName + ' ' + this.lastName;
    };

    return ConsultantModel;
  }]);

  app.config(['storeProvider', function(storeProvider) {
    storeProvider.registerModel('consultants', 'ConsultantModel');
  }]);
})();
