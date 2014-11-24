# all the imports

import sqlite3
import numpy as np



from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

from object_module import ObjISbox
from epar import EvaluationCorr, Data, AttackCorr



# configuration
DATABASE = './tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


# create our little application :)
app = Flask(__name__)
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
    g.db.close()


@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


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



if __name__ == '__main__':
    POWER = Data()
    PLAIN = Data()
    OBJECTIVE = ObjISbox()
    ATTACK = AttackCorr()
    EVALUATION = EvaluationCorr()
    app.run()
