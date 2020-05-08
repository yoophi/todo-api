from datetime import datetime

from app.database import db


class Todo(db.Model):
    __tablename__ = 'tdods'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Unicode(255), nullable=False)
    priority = db.Column(db.Integer, default=3)
    user_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
