from . import main
import code
from flask import render_template, flash, current_app, redirect, url_for, Flask, Markup
from multiprocessing import Process, Manager
from streaming_api_example import run
from .forms import LoginForm, SignupForm, CreateJobForm
from flask.ext.login import login_user, logout_user, login_required, current_user
from ..models import User
from .. import db
from streaming import run
import threading
import metric_analysis


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
            login_user(u)
            return redirect(url_for('.create_job'))

    return render_template('main/index.html', login_form=login_form, signup_form=signup_form)

@main.route('/create_job', methods=['GET', 'POST'])
@login_required
def create_job():
    app = current_app._get_current_object()
    create_job_form = CreateJobForm(CSRF_ENABLED=app.config['WTF_CSRF_ENABLED'])

    if create_job_form.validate_on_submit():
        if current_user.username in process_dct:
            flash('This username already has a job underway')
        else:
            manager = Manager()
            # d = manager.dict()
            d = {}
            d['keys'] = {
                'CONSUMER_KEY': str(create_job_form.consumer_key.data),
                'CONSUMER_SECRET': str(create_job_form.consumer_secret.data),
                'ACCESS_TOKEN': str(create_job_form.access_token.data),
                'ACCESS_TOKEN_SECRET': str(create_job_form.access_token_secret.data)
            }
            d['running'] = True
            d['metrics'] = None
            # p = Process(target=run, args=(d,))
            t = threading.Thread(target=run, args=(d,))
            process_dct[current_user.username] = t
            dict_dct[current_user.username] = d
            # p.start()
            t.start()
            print('/create_job')
            print('Thread started: ' + str(t.is_alive()) + ' for user ' + str(current_user.username))
            return redirect(url_for('.get_data'))
    return render_template('main/create_job.html', create_job_form=create_job_form)

@main.route('/get_data', methods=['GET'])
@login_required
def get_data():
    # code.interact(local=locals())
    if current_user.username in process_dct:
        print('/get_data')
        print('Data: ' + str(dict_dct[current_user.username]))
        print('Running: ' + str(dict_dct[current_user.username]['running']))
        print('Thread running: ' + str(process_dct[current_user.username].is_alive()))
        d = dict_dct[current_user.username]

        metrics_exist = False
        usr_dct = {}
        aggr_set = {}
        usr_dct = {}
        usrs = {}

        if d['metrics'] != None:
            metrics_exist = True
            aggr_set = get_chart(d['metrics']['stream_sentiment']['pos_sentiment'], d['metrics']['stream_sentiment']['neu_sentiment'],
                d['metrics']['stream_sentiment']['neg_sentiment'])
            print("pos " + str(d['metrics']['stream_sentiment']['pos_sentiment']))
            print("neu " + str(d['metrics']['stream_sentiment']['neu_sentiment']))
            print("neg " + str(d['metrics']['stream_sentiment']['neg_sentiment']))
            usrs = d['metrics']['user_metrics']
            print(aggr_set)

            for username in usrs:
                pos = 0.0
                neut = 0.0
                neg = 0.0
                n = 0
                for tweet in d['metrics']['tweet_metrics']:
                    if username == d['metrics']['tweet_metrics'][tweet]['user']:
                        pos += d['metrics']['tweet_metrics'][tweet]['pos_sentiment']
                        neut += d['metrics']['tweet_metrics'][tweet]['neu_sentiment']
                        neg += d['metrics']['tweet_metrics'][tweet]['neg_sentiment']
                        n += 1
                if n > 0:
                    usr_dct[username] = get_chart(pos / n, neut / n, neg / n)
                else:
                    usr_dct[username] = get_chart(0, 1, 0)

        if metrics_exist:
            flag = 'true'
        else:
            flag = 'false'
        return render_template('main/show_data.html', result=dict_dct[current_user.username],
            aggr_set=aggr_set, users=usrs, user_dct=usr_dct, metrics_exist=flag)
    else:
        flash('No job exists for this User')
        return redirect(url_for('.create_job'))

@main.route('/stop_job', methods=['GET', 'POST'])
@login_required
def stop_job():
    if current_user.username in process_dct:
        process = process_dct[current_user.username]
        dict_dct[current_user.username]['running'] = False
        print('Sent process stop signal, waiting for process to complete')
        # process.join()
        print('Thread finished: ' + str(process_dct[current_user.username].is_alive()))
        process_dct.pop(current_user.username, None)
        dict_dct.pop(current_user.username, None)
    else:
        flash('No job exists for this User to stop')

    return redirect(url_for('.create_job'))

@main.route('/logout', methods=['GET'])
@login_required
def log_out():
    logout_user()
    return redirect(url_for('.index'))

def get_chart(pos, neu, neg):
    p = pos
    ne = neu
    ng = neg
    labels = ["positive", "neutral", "negative"]
    values = [p, ne, ng]
    colors = ["#9fff80", "#ffff00", "#ff0000"]
    return zip(values, labels, colors)

