from . import db
from flask_login import UserMixin
from sqlalchemy import Enum, CheckConstraint
import enum

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Tasks', backref='owner', lazy=True)

class TaskStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.Integer, nullable=False) 
    status = db.Column(Enum(TaskStatus), nullable=False, default=TaskStatus.pending)
    completed = db.Column(db.Boolean, default=False)
    tag = db.Column(db.JSON)
    create_date = db.Column(db.DateTime, server_default=db.func.now())
    due_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    __table_args__ = (
        CheckConstraint('priority >= 1 AND priority <= 5', name='check_priority_range'),
    )

