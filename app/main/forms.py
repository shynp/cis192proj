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


class CreateJobForm(Form):
	consumer_key = StringField('Consumer Key', validators=[Required()])
	consumer_secret = StringField('Consumer Secret', validators=[Required()])
	access_token = StringField('Access Token', validators=[Required()])
	access_token_secret = StringField('Access Token Secret', validators=[Required()])
	submit = SubmitField('Create Job')