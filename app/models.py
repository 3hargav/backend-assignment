from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Videos(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(1000))
    channel_id = db.Column(db.String(255))
    published_at = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)
    thumbnails = db.relationship('Thumbnails', backref='videos', lazy=True)


class Thumbnails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000))
    video_id = db.Column(db.String(255), db.ForeignKey('videos.id'), nullable=False)
    resolution = db.Column(db.String(40))
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)


class ApiKeys(db.Model):
    key = db.Column(db.String(255), primary_key=True)
    is_quota_exceeded = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
