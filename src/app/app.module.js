(function() {
  'use strict';

  angular.module('radar', [
    'LocalStorageModule',
    'ui.router',
    'radar.account',
    'radar.auth',
    'radar.cohorts',
    'radar.controllers',
    'radar.core',
    'radar.crud',
    'radar.dataSources',
    'radar.filters',
    'radar.forms',
    'radar.home',
    'radar.logs',
    'radar.notifications',
    'radar.organisations',
    'radar.patients',
    'radar.permissions',
    'radar.posts',
    'radar.recruitPatient',
    'radar.resultSpecs',
    'radar.sessions',
    'radar.store',
    'radar.ui',
    'radar.units',
    'radar.users',
    'radar.utils',
    'radar.validators'
  ]);
})();
