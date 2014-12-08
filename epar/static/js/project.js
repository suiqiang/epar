$(function() {
  var add_project = function(e) {
    $.getJSON($SCRIPT_ROOT + '/_add_project',
              { project_name: $('input[name="project_name_add"]').val(),
                description: $('input[name="description"]').val() },
              function(data) {
                $('#notice').text(data.result);
              });
    return false;
  };

  $('button#btn_add_project').bind('click', add_project);
});



$(function() {
  var remove_project = function(e) {
    $.getJSON($SCRIPT_ROOT + '/_remove_project',
              { project_name_remove: $('input[name="project_name_remove"]').val() },
              function(data) {
                $('#notice').text(data.result);
              });
    return false;
  };

  $('button#btn_remove_project').bind('click', remove_project);
});



$(function() {
  var set_project = function(e) {
    $.getJSON($SCRIPT_ROOT + '/_set_project',
              { project_name_set: $('input[name="project_name_set"]').val() },
              function(data) {
                $('#notice').text(data.result);
              });
    return false;
  };

  $('button#btn_set_project').bind('click', set_project);
});
