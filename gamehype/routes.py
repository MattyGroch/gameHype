import json, random

from flask import render_template, flash, redirect, url_for, request, jsonify
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from gamehype import app, db
from gamehype.models import User, Rating, Game, Genre, Platform
from gamehype.forms import LoginForm, RegistrationForm, AddGameForm, EditGameForm


@app.route('/')
@app.route('/index')
def index():
    return render_template(
        'index.html',
        title='Home',
        )


@app.route('/ratings')
def ratings():
    ratings = Rating.query.all()
    return render_template(
        'ratings.html',
        title='Ratings',
        ratings=ratings
        )


@app.route('/games')
def games():
    games = Game.query.all()
    user = current_user
    return render_template(
        'games.html',
        title='Game List',
        games=games,
        user=user
        )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    ratings = Rating.query.filter_by(user_id=user.id).all()
    return render_template('user.html', ratings=ratings, user=user)

@app.route('/game/<game_id>')
def game(game_id):
    game = Game.query.get(game_id)
    return render_template('game.html', game=game)

@app.route('/editgame/<game_id>', methods=['GET', 'POST'])
def edit_game(game_id):
    game = Game.query.get(game_id)
    form = EditGameForm()
    if form.validate_on_submit():
        game.game_name = form.game_name.data
        game.release_date = form.release_date.data
        game.update_lists(form.genres.data, 'genres')
        game.update_lists(form.platforms.data, 'platforms')
        db.session.commit()
        return redirect(url_for('game', game_id=game.id))
    elif request.method == 'GET':
        form.game_name.data = game.game_name
        form.release_date.data = game.release_date
        form.platforms.data = game.platforms.all()
        form.genres.data = game.genres.all()

    return render_template('edit_game.html', game=game, form=form)


@app.route('/add_game', methods=['GET', 'POST'])
@login_required
def add_game():
    form = AddGameForm()
    if form.validate_on_submit():
        game_name = form.game_name.data
        game = Game(
            game_name=form.game_name.data,
            release_date=form.release_date.data,
            )
        genres = form.genres.data
        platforms = form.platforms.data
        db.session.add(game)
        db.session.commit()
        for g in genres:
            game.add_genre(g)
        db.session.commit()
        for p in platforms:
            game.add_platform(p)
        db.session.commit()
        flash('Congratulations, ' + game_name + ' has been added!')
        return redirect(url_for('games'))
    return render_template('add_game.html', title='Add a Game', form=form)


@app.route('/seed')
def seed_db():
    if not Game.query.all() and not Genre.query.all() and not Platform.query.all():
        with open('gamehype/seed-data.json') as seedfile:
            data = json.loads(seedfile.read())
            for g in data['genres']:
                genre = Genre(genre_name=g)
                db.session.add(genre)
            for p in data['platforms']:
                plat = Platform(platform_name=p)
                db.session.add(plat)
            db.session.commit()
    return redirect('/games')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/change_hype_level', methods = ['POST'])
def change_hype_level():
    data = request.get_json()
    print(data)
    rating = Rating(
        user_id = data['user_id'],
        game_id = data['game_id'],
        hype = data['rating']
    )
    db.session.add(rating)
    db.session.commit()
    return jsonify({'message': 'Rating updated'}), 200
