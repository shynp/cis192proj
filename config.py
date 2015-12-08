import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test dev key'
    SQLACHEMY_COMMIT_ON_TEARDOWN = True
    SSL_DISABLE = False
    WTF_CSRF_ENABLED = True

    @staticmethod
    def init_app(app):
        pass

class DevConfig(Config):
    DEBUG = False
    SQLACHEMY_DATABASE_URI = os.environ.get('DEV_DB_URL') or \
        'sqlite:///' + os.path.join(basedir, 'dev-db.sqlite')

class ProdConfig(Config):
    DEBUG = False
    SQLACHEMY_DATABASE_URI = os.environ.get('PROD_DB_URL') or \
        'sqlite:///' + os.path.join(basedir, 'prod-db.sqlite')

    @classmethod
    def init_app(app):
        Config.init_app(app)

        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

config = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'default': DevConfig
}