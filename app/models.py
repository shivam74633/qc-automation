from .init import db
from sqlalchemy.sql import func

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(50), default='free')  # free, busy, or offline
    is_logged_in = db.Column(db.Boolean, default=True) # As autentication module is alread in place so making all users as logged in
    tasks = db.relationship('Task', backref='user', lazy=True)
    
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255))
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    status = db.Column(db.String(50), default='unassigned')
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())