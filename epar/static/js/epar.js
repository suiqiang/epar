$(function() {
  var readplain = function(e) {
    $.getJSON($SCRIPT_ROOT + '/_readplain',
              function(data) {
                $('#notice').text(data.result);
              });
    return false;
  };

  $('button#btnreadplain').bind('click', readplain);
});


$(function() {
  var readpower = function(e) {
    $.getJSON($SCRIPT_ROOT + '/_readpower',
              function(data) {
                $('#notice').text(data.result);
              });
    return false;
  };

  $('button#btnreadpower').bind('click', readpower);
});

$(function() {
  var attack = function(e) {
    $.getJSON($SCRIPT_ROOT + '/_do_attack',
              { samples: $('input[name="samples"]').val() },
              function(data) {
                $('#notice').text(data.result);
              });
    return false;
  };

  $('button#btnattack').bind('click', attack);
});


$(function() {
  var evaluation = function(e) {
    $.getJSON($SCRIPT_ROOT + '/_do_evaluation',
              { truekey: $('input[name="truekey"]').val() },
              function(data) {
                $('#notice').text(data.result);
              });
    return false;
  };

  $('button#btnevaluation').bind('click', evaluation);
});
