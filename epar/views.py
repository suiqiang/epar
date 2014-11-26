from epar import app
from flask import request, session, g, redirect, url_for, \
     abort, render_template, flash

from epar.epar import EvaluationCorr, Data, AttackCorr
from epar.object_module import ObjISbox


POWER = Data()
PLAIN = Data()
OBJECTIVE = ObjISbox()
ATTACK = AttackCorr()
EVALUATION = EvaluationCorr()




@app.route('/')
def show_entries():
    return render_template('show_entries.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


@app.route('/readplain', methods=['POST'])
def readplain():
    if not session.get('logged_in'):
        abort(401)
    PLAIN.read_dir(request.form['dirname'], int, 1)
    flash('明文数据载入完成!')
    return redirect(url_for('show_entries'))


@app.route('/readpower', methods=['POST'])
def readpower():
    if not session.get('logged_in'):
        abort(401)
    POWER.read_dir(request.form['dirname'], float, 400)
    flash('功耗数据载入完成!')
    return redirect(url_for('show_entries'))


@app.route('/do_attack', methods=['POST'])
def do_attack():
    if not session.get('logged_in'):
        abort(401)
    samples = int(request.form['samples'])
    ATTACK.do_attack(OBJECTIVE,
                     PLAIN.data[:samples],
                     POWER.data[:samples, :],
                     256)
    flash('攻击完成!')
    flash(str(ATTACK._result))
    return redirect(url_for('show_entries'))


@app.route('/do_evaluation', methods=['POST'])
def do_evaluation():
    if not session.get('logged_in'):
        abort(401)
    EVALUATION.do_evaluation(ATTACK._mat_corr, int(request.form['truekey']))
    flash('评估完成')
    flash(EVALUATION._result['0.99'])
    return redirect(url_for('show_entries')) 