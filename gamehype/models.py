from datetime import datetime
from gamehype import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    ratings = db.relationship('Rating', backref='hypeman', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hype = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

    def __repr__(self):
        return '<Rating {}>'.format(self.hype)


class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform_name = db.Column(db.String(64), index=True, unique=True)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(128), index=True, unique=True)
    release_date = db.Column(db.DateTime, index=True)
    ratings = db.relationship('Rating', backref='game', lazy='dynamic')

    def __repr__(self):
        return '<Game {}>'.format(self.game_name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
