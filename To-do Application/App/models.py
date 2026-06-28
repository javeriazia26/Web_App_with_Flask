#python class that represents table in database
from app import db #we import the db object from our app package 
from werkzeug.security import generate_password_hash, check_password_hash

class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(8), nullable=False)
    hashed_password = db.Column(db.String(200), nullable=False)
    tasks = db.relationship("Task", backref="credential", lazy=True)

class Task(db.Model):  # creating table called Task that inherits from db.Model
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='pending')
    user_id=db.Column(db.Integer, db.ForeignKey("credential.id"), nullable=False)
