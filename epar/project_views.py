"""与工程管理相关的视图
"""

from epar import app
import os
import shutil
from flask import request, session, g, redirect, url_for, \
     abort, render_template, flash

import sqlite3
from contextlib import closing



def connect_db():
    """连接数据库
    """
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    """初始化数据库函数，建立数据库
    """
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    """请求数据之前连接数据库
    """
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
    g.db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select prjname, prjdir from entries order by id desc')
    entries = [dict(prjname=row[0], prjdir=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_prj():
    """增加工程
    """
    if not session.get('logged_in'):
        abort(401)
    cur = g.db.execute('select prjname, prjdir from entries order by id desc')
    entries = dict([(row[0], row[1]) for row in cur.fetchall()])
    prjname = request.form['prjname']
    prjdir = request.form['prjdir']

    if prjname in entries:
        flash(''.join(['工程: "', prjname, '" 已经存在']))
        return redirect(url_for('show_entries'))

    g.db.execute('insert into entries (prjname, prjdir) values (?, ?)',
                 [prjname, prjdir])
    g.db.commit()
    os.mkdir(''.join(['./tmp/', prjdir]))
    os.mkdir(''.join(['./tmp/', prjdir, '/plain']))
    os.mkdir(''.join(['./tmp/', prjdir, '/power']))
    flash(''.join(['工程: "', prjname, '" 建立完成']))
    return redirect(url_for('show_entries'))


@app.route('/remove', methods=['POST'])
def remove_prj():
    """删除工程
    """
    if not session.get('logged_in'):
        abort(401)
    cur = g.db.execute('select prjname, prjdir from entries order by id desc')
    entries = dict([(row[0], row[1]) for row in cur.fetchall()])
    prjname = request.form['prjname']
    prjdir = request.form['prjdir']

    if prjname in entries:
        """增加从数据库中删除工程的代码
        """
        # g.db.execute('insert into entries (prjname, prjdir) values (?, ?)',
        #              [prjname, prjdir])
        # g.db.commit()
        if os.path.isdir(''.join(['tmp/', prjdir])):
            shutil.rmtree(''.join(['tmp/', prjdir]))
            flash(''.join(['工程: "', prjname, '" 被删除']))
            return redirect(url_for('show_entries'))

    flash(''.join(['工程: "', prjname, '" 不存在']))
    return redirect(url_for('show_entries'))


@app.route('/set', methods=['POST'])
def set_prj():
    """设置当前工程
    """
    if not session.get('logged_in'):
        abort(401)
    cur = g.db.execute('select prjname, prjdir from entries order by id desc')
    entries = dict([(row[0], row[1]) for row in cur.fetchall()])
    prjname = request.form['prjname']
    prjdir = request.form['prjdir']

    if prjname in entries:
        if os.path.isdir(''.join(['tmp/', prjdir])):
            app.config['PRJDIR'] = ''.join(['tmp/', prjdir])
            flash(''.join(['当前工程设置为: "', prjname, '"']))
            return redirect(url_for('show_entries'))

    flash(''.join(['工程: "', prjname, '" 不存在']))
    return redirect(url_for('show_entries'))
