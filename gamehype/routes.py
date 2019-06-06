from gamehype import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, Idiot! You did it!"
