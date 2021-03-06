import _ from 'lodash';

import sortGroups from '../../groups/sort-groups';

import templateUrl from './patient-navigation.html';

function patientNavigation() {
  return {
    scope: {
      patient: '=',
    },
    templateUrl: templateUrl,
    link: function(scope) {
      scope.$watchCollection(function() {
        return scope.patient.getSystems();
      }, function(systems) {
        // Sort the systems by name
        scope.systems = _.sortBy(systems, 'name');
      });

      scope.$watchCollection(function() {
        // Only show current cohorts in the navigation
        return scope.patient.getCurrentCohorts();
      }, function(cohorts) {
        // Sort the cohorts by name
        scope.cohorts = sortGroups(cohorts);
      });
    }
  };
}

export default patientNavigation;
