(function() {
  'use strict';

  var app = angular.module('radar.patients.genetics');

  app.factory('GeneticsPermission', ['PatientObjectPermission', function(PatientObjectPermission) {
    return PatientObjectPermission;
  }]);

  function controllerFactory(
    ModelDetailController,
    GeneticsPermission,
    $injector,
    store,
    firstPromise
  ) {
    function GeneticsController($scope) {
      var self = this;

      $injector.invoke(ModelDetailController, self, {
        $scope: $scope,
        params: {
          permission: new GeneticsPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findFirst('genetics', {patient: $scope.patient.id, cohort: $scope.cohort.id}),
        store.findMany('genetics-karyotypes').then(function(karyotypes) {
          $scope.karyotypes = karyotypes;
        })
      ])).then(function() {
        self.view();
      });

      $scope.create = function() {
        var item = store.create('genetics', {patient: $scope.patient.id, cohort: $scope.cohort});
        self.edit(item);
      };
    }

    GeneticsController.$inject = ['$scope'];
    GeneticsController.prototype = Object.create(ModelDetailController.prototype);

    return GeneticsController;
  }

  controllerFactory.$inject = [
    'ModelDetailController',
    'GeneticsPermission',
    '$injector',
    'store',
    'firstPromise'
  ];

  app.factory('GeneticsController', controllerFactory);

  app.directive('geneticsComponent', ['GeneticsController', function(GeneticsController) {
    return {
      scope: {
        patient: '=',
        cohort: '='
      },
      controller: GeneticsController,
      templateUrl: 'app/patients/genetics/genetics-component.html'
    };
  }]);
})();
