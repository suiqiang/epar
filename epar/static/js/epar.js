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
                $('#notice').text("攻击完成，请查看结果");
                $('#result_attack_corr').append('相关系数攻击结果:');
                $('#result_attack_corr').append('<dt>'+data.result_corr+'</dt>');
                $('#result_attack_corr').append('均值差攻击结果:');
                $('#result_attack_corr').append('<dt>'+data.result_mean[0]+'</dt>');
                $('#result_attack_corr').append('<dt>'+data.result_mean[1]+'</dt>');
                $('#result_attack_corr').append('<dt>'+data.result_mean[2]+'</dt>');
                $('#result_attack_corr').append('<dt>'+data.result_mean[3]+'</dt>');
                $('#result_attack_corr').append('<dt>'+data.result_mean[4]+'</dt>');
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
                $('#notice').text("评估完成，请查看结果");
                $('#result_evaluation_corr').append('相关系数评估结果：');
                $('#result_evaluation_corr').append('<dt>α=0.99: n='+data['0.99']+'</dt>');
                $('#result_evaluation_corr').append('<dt>α=0.98: n='+data['0.98']+'</dt>');
                $('#result_evaluation_corr').append('<dt>α=0.97: n='+data['0.97']+'</dt>');
                $('#result_evaluation_corr').append('<dt>α=0.96: n='+data['0.96']+'</dt>');
                $('#result_evaluation_corr').append('<dt>α=0.95: n='+data['0.95']+'</dt>');
                $('#result_evaluation_corr').append('<dt>α=0.90: n='+data['0.90']+'</dt>');
                $('#result_evaluation_corr').append('<dt>α=0.85: n='+data['0.85']+'</dt>');
                $('#result_evaluation_corr').append('<dt>α=0.80: n='+data['0.80']+'</dt>');
              });
    return false;
  };

  $('button#btnevaluation').bind('click', evaluation);
});
