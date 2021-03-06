from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from flask.ext.login import LoginManager
from flask.ext import assets
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment

# db = SQLAlchemy()

db = None

def init_db(app):
    global db
    db = SQLAlchemy(app)

    from models import User
    if app.config['DEBUG']:
        print 'Recreating all db'
        db.create_all() # I DO create everything

bootstrap = Bootstrap()
moment = Moment()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # print(app.config.SQLALCHEMY_DATABASE_URI)
    config[config_name].init_app(app)

    env = assets.Environment(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    # db.init_app(app)
    init_db(app)

    login_manager.init_app(app)

    # if not app.config['SSL_DISABLE']:
    #     from flask.ext.sslify import SSLify
    #     app.debug = False
    #     sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app