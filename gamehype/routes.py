from flask import render_template, flash, redirect, url_for
from gamehype import app
from gamehype.models import User, Rating
from gamehype.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    user = User.query.get(1)
    ratings = Rating.query.all()
    return render_template(
        'index.html',
        title='Home',
        user=user,
        ratings=ratings
        )


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
