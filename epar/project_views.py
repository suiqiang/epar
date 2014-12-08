"""与工程管理相关的视图
"""
from epar import app, db, Project
import os
import shutil

from flask import request, session, abort, jsonify

# import sqlite3
# from contextlib import closing



# def connect_db():
#     """连接数据库
#     """
#     return sqlite3.connect(app.config['DATABASE'])


# def init_db():
#     """初始化数据库函数，建立数据库
#     """
#     with closing(connect_db()) as db:
#         with app.open_resource('schema.sql', mode='r') as f:
#             db.cursor().executescript(f.read())
#         db.commit()

# @app.before_request
# def before_request():
#     """请求数据之前连接数据库
#     """
#     g.db = connect_db()

# @app.teardown_request
# def teardown_request(exception):
#     db = getattr(g, 'db', None)
#     if db is not None:
#         db.close()
#     g.db.close()



# @app.route('/add', methods=['POST'])
# def add_prj():
#     """增加工程
#     """
#     if not session.get('logged_in'):
#         abort(401)
#     prj_name = request.form['prjname']
#     description = request.form['description']
#     if  Project.query.filter_by(prjname=prj_name).first():
#         flash(''.join(['工程: "', prj_name, '" 已经存在']))
#         return redirect(url_for('show_entries'))
#     project = Project(prj_name, description)
#     db.session.add(project)
#     db.session.commit()
#     os.mkdir(''.join(['./tmp/', prj_name]))
#     os.mkdir(''.join(['./tmp/', prj_name, '/plain']))
#     os.mkdir(''.join(['./tmp/', prj_name, '/power']))
#     flash(''.join(['工程: "', prj_name, '" 建立完成']))
#     return redirect(url_for('show_entries'))
@app.route('/_add_project')
def add_project():
    """增加工程
    """
    if not session.get('logged_in'):
        abort(401)
    project_name = request.args.get('project_name', 0, type=str)
    description = request.args.get('description', 0, type=str)
    if  Project.query.filter_by(project_name=project_name).first():
        return jsonify(result=''.join(['工程: "', project_name, '" 已经存在']))
    project = Project(project_name, description)
    db.session.add(project)
    db.session.commit()
    os.mkdir(''.join(['./tmp/', project_name]))
    os.mkdir(''.join(['./tmp/', project_name, '/plain']))
    os.mkdir(''.join(['./tmp/', project_name, '/power']))
    return jsonify(result=''.join(['工程: "', project_name, '" 建立完成']))


# @app.route('/remove', methods=['POST'])
# def remove_project():
#     """删除工程
#     """
#     if not session.get('logged_in'):
#         abort(401)
#     project_name = request.form['projectname']
#     project =  Project.query.filter_by(projectname=project_name).first()
#     if  project:
#         db.session.delete(project)
#         db.session.commit()
#         if os.path.isdir(''.join(['tmp/', project_name])):
#             shutil.rmtree(''.join(['tmp/', project_name]))
#         flash(''.join(['工程: "', project_name, '" 被删除']))
#         return redirect(url_for('show_entries'))


#     flash(''.join(['工程: "', project_name, '" 不存在']))
#     return redirect(url_for('show_entries'))

@app.route('/_remove_project')
def remove_project():
    """删除工程
    """
    if not session.get('logged_in'):
        abort(401)
    project_name = request.args.get('project_name_remove', 0, type=str)
    project = Project.query.filter_by(project_name=project_name).first()
    if  project:
        db.session.delete(project)
        db.session.commit()
        if os.path.isdir(''.join(['tmp/', project_name])):
            shutil.rmtree(''.join(['tmp/', project_name]))
        return jsonify(result=''.join(['工程: "', project_name, '" 被删除']))
    return jsonify(result=''.join(['工程: "', project_name, '" 不存在']))

    # if projectname in entries:
    #     """增加从数据库中删除工程的代码
    #     """
    #     # g.db.execute('insert into entries (projectname, projectdir) values (?, ?)',
    #     #              [projectname, projectdir])
    #     # g.db.commit()
    #     if os.path.isdir(''.join(['tmp/', projectdir])):
    #         shutil.rmtree(''.join(['tmp/', projectdir]))
    #         flash(''.join(['工程: "', projectname, '" 被删除']))
    #         return redirect(url_for('show_entries'))

    # flash(''.join(['工程: "', projectname, '" 不存在']))
    # return redirect(url_for('show_entries'))


# @app.route('/set', methods=['POST'])
# def set_project():
#     """设置当前工程
#     """
#     if not session.get('logged_in'):
#         abort(401)
#     project_name = request.form['projectname']
#     if  Project.query.filter_by(projectname=project_name).first():
#         if os.path.isdir(''.join(['tmp/', project_name])):
#             app.config['PROJECTDIR'] = ''.join(['tmp/', project_name])
#             flash(''.join(['当前工程设置为: "', project_name, '"']))
#             return redirect(url_for('show_entries'))

#     flash(''.join(['工程: "', project_name, '" 不存在']))
#     return redirect(url_for('show_entries'))

@app.route('/_set_project')
def set_project():
    """设置当前工程
    """
    if not session.get('logged_in'):
        abort(401)
    project_name = request.args.get('project_name_set', 0, type=str)
    if  Project.query.filter_by(project_name=project_name).first():
        if os.path.isdir(''.join(['tmp/', project_name])):
            app.config['PRJDIR'] = ''.join(['tmp/', project_name])
            return jsonify(result=''.join(['当前工程设置为: "', project_name, '"']))
    return jsonify(result=''.join(['工程: "', project_name, '" 不存在']))
