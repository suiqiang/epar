# all the imports

import numpy as np
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime


#,request, session, g, redirect, url_for, \
#     abort, render_template, flash

#from contextlib import closing


#from object_module import ObjISbox
#from epar import EvaluationCorr, Data, AttackCorr


# create our little application :)
app = Flask(__name__)
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config.from_object('config')

db = SQLAlchemy(app)


#from epar.epar import EvaluationCorr, Data, AttackCorr
#from epar.object_module import ObjISbox


class Project(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    project_name = db.Column(db.String(64), index = True, unique = True)
    description = db.Column(db.String(400))
    timestamp = db.Column(db.DateTime)

    def __init__(self, project_name, description, timestamp=None):
        self.project_name = project_name
        self.description = description
        if timestamp is None:
            timestamp = datetime.utcnow()
        self.timestamp = timestamp

    def __repr__(self):
        return '<User %r>' % (self.project_name) 


import epar.project_views
import epar.upload_views
import epar.epar_views
import epar.login_views
