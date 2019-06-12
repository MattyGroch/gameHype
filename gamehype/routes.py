from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from gamehype import app, db
from gamehype.models import User, Rating, Game
from gamehype.forms import LoginForm, RegistrationForm, AddGameForm


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
    return render_template(
        'games.html',
        title='Game List',
        games=games
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


@app.route('/add_game', methods=['GET', 'POST'])
@login_required
def add_game():
    form = AddGameForm()
    if form.validate_on_submit():
        game_name = form.game_name.data
        game = Game(
            game_name=form.game_name.data,
            release_date=form.release_date.data,
            genres=form.genres.data
            )
        db.session.add(game)
        db.session.commit()
        flash('Congratulations, ' + game_name + ' has been added!')
        return redirect(url_for('games'))
    return render_template('add_game.html', title='Add a Game', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
