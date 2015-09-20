(function() {
  'use strict';

  var app = angular.module('radar.patients.aliases');

  app.factory('PatientAliasPermission', ['PatientRadarObjectPermission', function(PatientRadarObjectPermission) {
    return PatientRadarObjectPermission;
  }]);

  app.factory('PatientAliasesController', ['ListDetailController', 'PatientAliasPermission', 'firstPromise','getRadarDataSource', '$injector', 'store', function(ListDetailController, PatientAliasPermission, firstPromise, getRadarDataSource, $injector, store) {
    function PatientAliasesController($scope) {
      var self = this;

      $injector.invoke(ListDetailController, self, {
        $scope: $scope,
        params: {
          permission: new PatientAliasPermission($scope.patient)
        }
      });

      self.load(firstPromise([
        store.findMany('patient-aliases', {patient: $scope.patient.id}),
        getRadarDataSource().then(function(dataSource) {
          $scope.dataSource = dataSource;
        })
      ]));

      $scope.create = function() {
        var item = store.create('patient-aliases', {
          patient: $scope.patient.id,
          dataSource: $scope.dataSource
        });
        self.edit(item);
      };
    }

    PatientAliasesController.$inject = ['$scope'];
    PatientAliasesController.prototype = Object.create(ListDetailController.prototype);

    return PatientAliasesController;
  }]);

  app.directive('patientAliasesComponent', ['PatientAliasesController', function(PatientAliasesController) {
    return {
      scope: {
        patient: '='
      },
      controller: PatientAliasesController,
      templateUrl: 'app/patients/aliases/aliases-component.html'
    };
  }]);
})();
