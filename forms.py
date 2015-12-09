from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, EqualTo

class LoginForm(Form):
    username = StringField('Username',
                        validators=[Required(), Length(1, 64)])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class SignupForm(Form):
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Enter a password:', validators=[Required(), EqualTo('password2', message='Passwords must match') ])
    password2 = PasswordField('Confirm password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign up')