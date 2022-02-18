from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from files.setup import app

db = SQLAlchemy(app)
#TIER ONE DATABASE
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    #information
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    passed = db.Column(db.String(), nullable=True)
    #return
    def __repr__(self):
        return f"User('{self.username}', '{self.passed}')"
        
db.create_all()