from flask import render_template
from gamehype import app
from gamehype.models import User, Rating

@app.route('/')
@app.route('/index')
def index():
    user = User.query.all()
    rating = Rating.query.all()
    return render_template('index.html', title='Home', user=user, rating=rating)
