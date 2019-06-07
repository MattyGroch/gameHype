from flask import render_template
from gamehype import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Timmy Jimmy'}
    ratings = [
        {
            'hypeman': {'username': 'Matt'},
            'hype': '5/5'
        },
        {
            'hypeman': {'username': 'Ben'},
            'hype': '3/5'
        }
    ]
    return render_template('index.html', title='Home', user=user, ratings=ratings)
