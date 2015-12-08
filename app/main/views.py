from . import main
from flask import render_template
from multiprocessing import Process, Manager
from streaming_api_example import run
from .forms import LoginForm, SignupForm
from flask.ext.login import login_user, logout_user, login_required

process_dct = {}
dict_dct = {}

@main.route('/')
@main.route('/index')
def index():
	app = current_app._get_current_object()
    login_form = LoginForm(CSRF_ENABLED=app.config['WTF_CSRF_ENABLED'])
    signup_form = SignupForm(CSRF_ENABLED=app.config['WTF_CSRF_ENABLED'])

    if login_form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('mentors.index'))
        flash('Invalid username or password.')
    return render_template('main/login.html', form=form)

@main.route('/create_job')
@login_required
def create_job():
	manager = Manager()
	d = manager.dict()
	d['running'] = True
	d['counter'] = 0
	p = Process(target=run, args=(d,))
	process_dct['user'] = p
	dict_dct['user'] = d
	p.start()
	print('Process started: ' + str(p.is_alive()))
	return render_template('main/404.html')

@main.route('/get_data')
@login_required
def get_data():
	print('Counter: ' + str(dict_dct['user']['counter']))
	print('Running: ' + str(dict_dct['user']['running']))
	print('Process running: ' + str(process_dct['user'].is_alive()))
	return render_template('main/404.html')

@main.route('/stop_job')
@login_required
def stop_job():
	dict_dct['user']['running'] = False
	print('Counter: ' + str(dict_dct['user']['counter']))
	print('Running: ' + str(dict_dct['user']['running']))
	print('Process running: ' + process_dct['user'].is_alive())
	return render_template('main/404.html')
