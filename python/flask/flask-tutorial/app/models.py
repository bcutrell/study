
# https://www.pythonsheets.com/notes/python-sqlalchemy.html

from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import desc

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    videos = db.relationship('Video', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Video(db.Model):
    # store videos by title + user + datetime

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(240))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Video {}>'.format(self.title)

    @classmethod
    def load_all(self):
        return self.query.order_by(desc(Video.timestamp)).limit(3).all()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

