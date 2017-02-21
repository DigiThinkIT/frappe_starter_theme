
var _old_get_query_params = get_query_params;
var get_query_params = function(query_string) {
  var result = _old_get_query_params(query_string)
  result = Object.assign(result, get_query_params.overrides);
  return result;
}
