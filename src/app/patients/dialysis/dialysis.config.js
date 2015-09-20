(function() {
  'use strict';

  var app = angular.module('radar.patients.dialysis');

  app.config(['$stateProvider', function($stateProvider) {
    $stateProvider.state('patient.dialysis', {
      url: '/dialysis',
      templateUrl: 'app/patients/dialysis/dialysis.html'
    });
  }]);
})();
