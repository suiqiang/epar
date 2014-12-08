"""与工程管理相关的视图
"""

from epar import app
import os
import shutil
from flask import request, session, redirect, url_for, \
     abort, render_template, flash



@app.route('/')
def show_entries():
    # cur = g.db.execute('select prjname, prjdir from entries order by id desc')
    # entries = [dict(prjname=row[0], prjdir=row[1]) for row in cur.fetchall()]
    entries = 'todo'
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_prj():
    """增加工程
    """
    if not session.get('logged_in'):
        abort(401)
    prj_name = request.form['prjname']
    description = request.form['description']
    if  Project.query.filter_by(prjname=prj_name).first():
        flash(''.join(['工程: "', prj_name, '" 已经存在']))
        return redirect(url_for('show_entries'))
    project = Project(prj_name, description)
    db.session.add(project)
    db.session.commit()
    os.mkdir(''.join(['./tmp/', prj_name]))
    os.mkdir(''.join(['./tmp/', prj_name, '/plain']))
    os.mkdir(''.join(['./tmp/', prj_name, '/power']))
    flash(''.join(['工程: "', prj_name, '" 建立完成']))
    return redirect(url_for('show_entries'))


@app.route('/remove', methods=['POST'])
def remove_prj():
    """删除工程
    """
    if not session.get('logged_in'):
        abort(401)
    prj_name = request.form['prjname']
    project =  Project.query.filter_by(prjname=prj_name).first()
    if  project:
        db.session.delete(project)
        db.session.commit()
        if os.path.isdir(''.join(['tmp/', prj_name])):
            shutil.rmtree(''.join(['tmp/', prj_name]))
        flash(''.join(['工程: "', prj_name, '" 被删除']))
        return redirect(url_for('show_entries'))


    flash(''.join(['工程: "', prj_name, '" 不存在']))
    return redirect(url_for('show_entries'))

    # if prjname in entries:
    #     """增加从数据库中删除工程的代码
    #     """
    #     # g.db.execute('insert into entries (prjname, prjdir) values (?, ?)',
    #     #              [prjname, prjdir])
    #     # g.db.commit()
    #     if os.path.isdir(''.join(['tmp/', prjdir])):
    #         shutil.rmtree(''.join(['tmp/', prjdir]))
    #         flash(''.join(['工程: "', prjname, '" 被删除']))
    #         return redirect(url_for('show_entries'))

    # flash(''.join(['工程: "', prjname, '" 不存在']))
    # return redirect(url_for('show_entries'))


@app.route('/set', methods=['POST'])
def set_prj():
    """设置当前工程
    """
    if not session.get('logged_in'):
        abort(401)
    prj_name = request.form['prjname']
    if  Project.query.filter_by(prjname=prj_name).first():
        if os.path.isdir(''.join(['tmp/', prj_name])):
            app.config['PRJDIR'] = ''.join(['tmp/', prj_name])
            flash(''.join(['当前工程设置为: "', prj_name, '"']))
            return redirect(url_for('show_entries'))

    flash(''.join(['工程: "', prj_name, '" 不存在']))
    return redirect(url_for('show_entries'))
