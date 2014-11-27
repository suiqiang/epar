# all the imports

import numpy as np
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

#from object_module import ObjISbox
#from epar import EvaluationCorr, Data, AttackCorr


# create our little application :)
app = Flask(__name__)
#app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config.from_object('config')



#from epar.epar import EvaluationCorr, Data, AttackCorr
#from epar.object_module import ObjISbox


import epar.project_views
import epar.upload_views
import epar.epar_views
