from . import main
from flask import render_template, flash, current_app
from multiprocessing import Process, Manager
from streaming_api_example import run
from .forms import LoginForm, SignupForm
from flask.ext.login import login_user, logout_user, login_required, current_user
# from ..models import User

process_dct = {}
dict_dct = {}

@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    app = current_app._get_current_object()
    login_form = LoginForm(CSRF_ENABLED=app.config['WTF_CSRF_ENABLED'])
    signup_form = SignupForm(CSRF_ENABLED=app.config['WTF_CSRF_ENABLED'])

    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user, login_form.remember_me.data)
            return redirect(url_for('.create_job'))
        flash('Invalid username or password.')

    if signup_form.validate_on_submit():
        existingUser = User.query.filter_by(username=signup_form.username.data).first()
        if existingUser:
            flash('Username already exists. Try again')
        else:
            u = User(
                    username=signup_form.username.data,
                    password=signup_form.password.data
                )
            db.session.add(u)
            db.session.commit()
            login_user(u, signup_form.remember_me.data)
            return redirect(url_for('.create_job'))

    return render_template('main/index.html', login_form=login_form, signup_form=signup_form)

@main.route('/create_job', methods=['GET', 'POST'])
@login_required
def create_job():
    print('Username: ' + current_user.username)

    # manager = Manager()
    # d = manager.dict()
    # d['running'] = True
    # d['counter'] = 0
    # p = Process(target=run, args=(d,))
    # process_dct['user'] = p
    # dict_dct['user'] = d
    # p.start()
    # print('Process started: ' + str(p.is_alive()))
    return render_template('main/404.html')

@main.route('/get_data', methods=['GET'])
@login_required
def get_data():
    print('Counter: ' + str(dict_dct['user']['counter']))
    print('Running: ' + str(dict_dct['user']['running']))
    print('Process running: ' + str(process_dct['user'].is_alive()))
    return render_template('main/404.html')

@main.route('/stop_job', methods=['GET', 'POST'])
@login_required
def stop_job():
    dict_dct['user']['running'] = False
    print('Counter: ' + str(dict_dct['user']['counter']))
    print('Running: ' + str(dict_dct['user']['running']))
    print('Process running: ' + process_dct['user'].is_alive())
    return render_template('main/404.html')
