from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, validators
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from gamehype.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class AddGameForm(FlaskForm):
    game_name = StringField(
        'Game Title',
        [validators.required(), validators.length(min=2, max=128)]
        )
    release_date = DateField('Release Date', format='%d/%m/%Y')
    genre = SelectField('Genre(s)', choices=[('Cool','Uncool')])
    submit = SubmitField('Submit')
