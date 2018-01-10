import templateUrl from './checkbox-field.html';

function frmCheckboxField() {
  return {
    restrict: 'A',
    scope: {
      model: '=',
      disabled: '=',
      checked: '='
    },
    transclude: true,
    templateUrl: templateUrl
  };
}

export default frmCheckboxField;
