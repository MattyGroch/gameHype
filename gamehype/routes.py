from flask import render_template
from gamehype import app
from gamehype.models import User, Rating

@app.route('/')
@app.route('/index')
def index():
    user = User.query.get(1)
    ratings = Rating.query.all()
    return render_template('index.html', title='Home', user=user, ratings=ratings)

@app.route('/ratingtest')
def ratingtest():
    user = User.query.get(1)
    ratings = Rating.query.all()
    return render_template('ratingtest.html', title='Home', user=user, ratings=ratings)
