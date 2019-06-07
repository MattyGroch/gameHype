from datetime import datetime
from gamehype import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    ratings = db.relationship('Rating', backref='hypeman', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hype = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Rating {}>'.format(self.rating)
