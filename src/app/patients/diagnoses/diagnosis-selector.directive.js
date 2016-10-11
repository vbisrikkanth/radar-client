import _ from 'lodash';

import templateUrl from './diagnosis-selector.html';

/** User interface for choosing a diagnosis from a list. */
function diagnosisSelector(store) {
  return {
    require: 'ngModel',
    templateUrl: templateUrl,
    scope: {
      'patient': '='
    },
    link: function(scope, element, attrs, ngModel) {
      // Mapping between group id and secondary diagnoses
      var groupDiagnoses = {};

      // Currently selected group (all diagnoses are displayed when set to null)
      scope.group = null;

      // List of groups with at least one secondary diagnosis (displayed as tabs)
      scope.groups = [];

      // Currently selected diagnosis
      scope.diagnosis = null;

      // Currently displayed diagnoses
      scope.diagnoses = [];

      // True while the directive is loading
      scope.loading = true;

      // Add functions to scope
      scope.setGroup = setGroup;
      scope.isActive = isActive;
      scope.use = use;
      scope.drop = drop;

      /** Called when the model is updated outside of the directive. */
      ngModel.$render = function() {
        scope.diagnosis = ngModel.$viewValue;
      };

      load();

      /** Get the list of diagnoses for this group. */
      function getDiagnoses(group) {
        var key = group === null ? null : group.id;
        return groupDiagnoses[key] || [];
      }

      /** Set the current group (triggered by clicking a tab). */
      function setGroup(group) {
        scope.group = group;
        scope.diagnoses = getDiagnoses(group);
      }

      /** Returns true if the group is selected. */
      function isActive(group) {
        return scope.group === group;
      }

      /** Update the selected diagnosis. */
      function update(diagnosis) {
        scope.diagnosis = diagnosis;

        // Update the model
        ngModel.$setViewValue(diagnosis);
      }

      /** Select a diagnosis. */
      function use(diagnosis) {
        update(diagnosis);
      }

      /** Deselect the diagnosis. */
      function drop() {
        update(null);
      }

      /** Add a diagnosis to the mapping */
      function add(group, diagnosis) {
        var key = group === null ? null : group.id;

        if (groupDiagnoses[key] === undefined) {
          groupDiagnoses[key] = [];
        }

        // Diagnoses are sorted by weight by default. The diagnosis name is used if two diagnoses
        // have the same weight.
        var weight = group === null ? diagnosis.name : [diagnosis.getWeight(group.id), diagnosis.name];

        groupDiagnoses[key].push({
          diagnosis: diagnosis,
          edtaCode: diagnosis.getEdtaCode(),
          weight: weight
        });
      }

      /** Load the list of diagnoses. */
      function load() {
        store.findMany('diagnoses').then(function(diagnoses) {
          _.forEach(diagnoses, function(diagnosis) {
            // Add the diagnosis to the all list
            add(null, diagnosis);

            // Add the diagnosis to each of its groups
            _.forEach(diagnosis.groups, function(group) {
              if (group.type.id === 'SECONDARY') {
                // Add the diagnosis to the group list
                add(group.group, diagnosis);
              }
            });
          });

          // Get the patient's groups sorted by name
          scope.groups = _.sortBy(scope.patient.getGroups(), 'shortName');

          // Remove groups that don't have any diagnoses
          scope.groups = _.filter(scope.groups, function(group) {
            return getDiagnoses(group).length > 0;
          });

          // Select the first group with diagnoses (otherwise all)
          if (scope.groups.length > 0) {
            setGroup(scope.groups[0]);
          } else {
            setGroup(null);
          }

          // Finished loading
          scope.loading = false;
        });
      }
    }
  };
}

diagnosisSelector.$inject = ['store'];

export default diagnosisSelector;
