import _ from 'lodash';

/**
 * Flattens any child objects into just their id.
 *
 * @param {*} data - the value to flatten.
 * @param {integer|undefined} depth - internal value to keep track of recursion depth.
 * @returns {*} - the flattened value.
 */
function flattenRelationships(data, depth) {
  if (depth === undefined) {
    depth = 0;
  }

  var newData;

  if (_.isArray(data)) { // Array
    newData = [];

    // Recurse into each value in the array
    _.each(data, function(value) {
      newData.push(flattenRelationships(value, depth + 1));
    });
  } else if (_.isObject(data)) { // Object
    // Flatten any child objects with an id property
    if (depth > 0 && data.id !== undefined) {
      newData = data.id;
    } else {
      newData = {};

      // Recuse into each value of the object
      _.each(data, function(value, key) {
        newData[key] = flattenRelationships(value, depth + 1);
      });
    }
  } else { // Primitive
    newData = data;
  }

  return newData;
}

export default flattenRelationships;
