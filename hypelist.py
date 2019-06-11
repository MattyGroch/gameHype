from gamehype import db, app
from gamehype.models import User, Rating, Game, Platform


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Rating': Rating, 'Game': Game, 'Platform': Platform}
