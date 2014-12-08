from epar import db
from datetime import datetime



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
