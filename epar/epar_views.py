from epar import app


from flask import request, session, abort, jsonify, json

from epar.epar import EvaluationCorr, Data, AttackCorr, AttackMean
from epar.object_module import ObjISbox

POWER = Data()
PLAIN = Data()
OBJECTIVE = ObjISbox()
ATTACKCORR = AttackCorr()
EVALUATIONCORR = EvaluationCorr()

ATTACKMEAN = AttackMean()

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != app.config['USERNAME']:
#             error = 'Invalid username'
#         elif request.form['password'] != app.config['PASSWORD']:
#             error = 'Invalid password'
#         else:
#             session['logged_in'] = True
#             flash('You were logged in')
#             return redirect(url_for('show_entries'))
#     return render_template('login.html', error=error)


# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     flash('You were logged out')
#     return redirect(url_for('show_entries'))


# @app.route('/readplain', methods=['POST'])
# def readplain():
#     if not session.get('logged_in'):
#         abort(401)
#     PLAIN.read_dir(request.form['dirname'], int, 1)
#     flash('明文数据载入完成!')
#     return redirect(url_for('show_entries'))


# @app.route('/readpower', methods=['POST'])
# def readpower():
#     if not session.get('logged_in'):
#         abort(401)
#     POWER.read_dir(request.form['dirname'], float, 400)
#     flash('功耗数据载入完成!')
#     return redirect(url_for('show_entries'))

# @app.route('/readplain', methods=['POST'])
# def readplain():
#     if not session.get('logged_in'):
#         abort(401)
#     PLAIN.read_dir(''.join([app.config['PRJDIR'], '/plain/']), int, 1)
#     flash('明文数据载入完成!')
#     return redirect(url_for('show_entries'))

@app.route('/_readplain')
def readplain():
    if not session.get('logged_in'):
        abort(401)
    PLAIN.read_dir(''.join([app.config['PRJDIR'], '/plain/']), int, 'c', 1)
    return jsonify(result="明文数据转入完成")


# @app.route('/readpower', methods=['POST'])
# def readpower():
#     if not session.get('logged_in'):
#         abort(401)
#     POWER.read_dir(''.join([app.config['PRJDIR'], '/power/']), float, 400)
#     flash('功耗数据载入完成!')
#     return redirect(url_for('show_entries'))

@app.route('/_readpower')
def readpower():
    if not session.get('logged_in'):
        abort(401)
    POWER.read_dir(''.join([app.config['PRJDIR'], '/power/']), float, 'c', 400)
    return jsonify(result="功耗数据载入完成")


# @app.route('/do_attack', methods=['POST'])
# def do_attack():
#     if not session.get('logged_in'):
#         abort(401)
#     samples = int(request.form['samples'])
#     ATTACK.do_attack(OBJECTIVE,
#                      PLAIN.data[:samples],
#                      POWER.data[:samples, :],
#                      256)
#     flash('攻击完成!')
#     flash(str(ATTACK._result))
#     return redirect(url_for('show_entries'))

@app.route('/_do_attack')
def do_attack():
    if not session.get('logged_in'):
        abort(401)
    samples = request.args.get('samples', 0, type=int)
    ATTACKCORR.do_attack(OBJECTIVE,
                         PLAIN.data[:samples],
                         POWER.data[:samples, :],
                         8)
    ATTACKMEAN.do_attack(OBJECTIVE,
                         PLAIN.data[:samples],
                         POWER.data[:samples, :],
                         8)
    # return jsonify(result=int(ATTACKCORR._result[0]))

    result_mean = dict(zip(range(5), ATTACKMEAN._result[0:5]))
    return jsonify(result_corr=str(ATTACKCORR._result[0]),
                   result_mean=result_mean)



# result_mean = dict(zip(range(5), ATTACKMEAN._result[0:5]))

    # return jsonify(result_corr=str(ATTACKCORR._result[0]),
    #                result_mean=result})

# result_attack_corr=int(ATTACKCORR._result),
                   # result_attack_mean=ATTACKMEAN._result)

# @app.route('/do_evaluation', methods=['POST'])
# def do_evaluation():
#     if not session.get('logged_in'):
#         abort(401)
#     EVALUATION.do_evaluation(ATTACK._mat_corr, int(request.form['truekey']))
#     flash('评估完成')
#     flash(EVALUATION._result['0.99'])
#     return redirect(url_for('show_entries'))

@app.route('/_do_evaluation')
def do_evaluation():
    if not session.get('logged_in'):
        abort(401)
    truekey = request.args.get('truekey', 0, type=int)
    EVALUATIONCORR.do_evaluation(ATTACKCORR._mat_corr, truekey)
    # json_data = json.dumps(EVALUATIONCORR._result)
    return jsonify(EVALUATIONCORR._result)

    # return jsonify(result=[1,2,3])


    # flash(EVALUATION._result['0.99'])
