from epar import app

from flask import request, session, render_template, flash

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
            return render_template('main.html')
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return render_template('main.html')


@app.route('/')
def main():
    return render_template('main.html')

# @app.route('/')
# def show_entries():
#     # cur = g.db.execute('select prjname, prjdir from entries order by id desc')
#     # entries = [dict(prjname=row[0], prjdir=row[1]) for row in cur.fetchall()]
#     entries = 'todo'
#     return render_template('main.html', entries=entries)
