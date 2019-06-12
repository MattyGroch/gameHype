from datetime import datetime
from gamehype import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


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

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


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

    games = db.relationship('Game', secondary="platform_games", lazy='dynamic')

    def __repr__(self):
        return '<Platform {}>'.format(self.platform_name)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(128), index=True, unique=True)
    release_date = db.Column(db.DateTime, index=True)
    ratings = db.relationship('Rating', backref='game', lazy='dynamic')

    platforms = db.relationship('Platform', secondary="platform_games", lazy='dynamic')

    genres = db.relationship('Genre', secondary="genre_games", lazy='dynamic')

    developers = db.Relationship('Developer', secondary="developer_games", lazy='dynamic')
    publishers = db.Relationship('Publisher', secondary="publisher_games", lazy='dynamic')

    def __repr__(self):
        return '<Game {}>'.format(self.game_name)

    def check_platform(self, platform):
        return self.platforms.filter(platform_games.c.platform_id == platform.id).count() > 0

    def add_platform(self, platform):
        if not self.check_platform(platform):
            self.platforms.append(platform)

    def remove_platform(self, platform):
        if self.check_platform(platform):
            self.platforms.remove(platform)

    def check_genre(self, genre):
        return self.genres.filter(genre_games.c.genre_id == genre.id).count() > 0

    def add_genre(self, genre):
        if not self.check_genre(genre):
            self.genres.append(genre)

    def remove_genre(self, genre):
        if self.check_genre(genre):
            self.genres.remove(genre)

    def check_developer(self, developer):
        return self.developers.filter(developer_games.c.developer_id == developer.id).count() > 0

    def add_developer(self, developer):
        if not self.check_developer(developer):
            self.developers.append(developer)

    def remove_developer(self, developer):
        if self.check_developer(developer):
            self.developers.remove(developer)

    def check_publisher(self, publisher):
        return self.publishers.filter(publisher_games.c.publisher_id == publisher.id).count() > 0

    def add_publisher(self, publisher):
        if not self.check_publisher(publisher):
            self.publishers.append(publisher)

    def remove_publisher(self, publisher):
        if self.check_publisher(publisher):
            self.publishers.remove(publisher)

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(64), index=True, unique=True)

    games = db.relationship('Game', secondary="genre_games", lazy='dynamic')

    def __repr__(self):
        return '<Genre {}>'.format(self.genre_name)

class Developer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    developer_name = db.Column(db.String(128), index=True, unique=True)

    games = db.relationship('Game', secondary="developer_games", lazy='dynamic')

    def __repr__(self):
        return '<Developer {}>'.format(self.developer_name)

class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publisher_name = db.Column(db.String(128), index=True, unique=True)

    games = db.relationship('Game', secondary="publisher_games", lazy='dynamic')

    def __repr__(self):
        return '<Publisher {}>'.format(self.publisher_name)

platform_games = db.Table('platform_games',
    db.Column('platform_id', db.Integer, db.ForeignKey('platform.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'))
    )

genre_games = db.Table('genre_games',
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'))
    )

developer_games = db.Table('developer_games',
    db.Column('developer_id', db.Integer, db.ForeignKey('developer.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'))
    )

publisher_games = db.Table('publisher_games',
    db.Column('publisher_id', db.Integer, db.ForeignKey('publisher.id')),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'))
    )

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
