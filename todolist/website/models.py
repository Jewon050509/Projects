from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

# Database that represent User
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    tasks = db.relationship('Task', order_by='Task.due_date.asc()')

# Database that represent Task
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    due_date = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))