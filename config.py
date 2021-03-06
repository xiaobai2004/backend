import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = ''
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SSL_ENABLED = bool
    os.environ.get('SSL_ENABLED') or False

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%(username)s:%(password)s@%(host)s:%(port)s/%(dbname)s" %  {
        "username" : 'root',
        "password" : '',
        "host" : 'localhost',
        "port" : '3306',
        "dbname" : 'wenbaidb'
    }
 
    EXCEL_OUTPUT_PATH = os.environ.get('EXCEL_OUTPUT_PATH') or basedir


class TestingConfig(Config):
    TESTING = True
    SSL_ENABLED = bool(os.environ.get('SSL_ENABLED')) or False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    EXCEL_OUTPUT_PATH = os.environ.get('EXCEL_OUTPUT_PATH') or basedir


class ProductionConfig(Config):
    SSL_ENABLED = bool(os.environ.get('SSL_ENABLED')) or True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%(username)s:%(password)s@%(host)s:%(port)s/%(dbname)s" %  {
        "username" : os.environ.get('MYSQL_USER'),
        "password" : os.environ.get('MYSQL_PASS'),
        "host" : os.environ.get('MYSQL_HOST'),
        "port" : os.environ.get('MYSQL_PORT'),
        "dbname" : os.environ.get('MYSQL_DB')
    }
    EXCEL_OUTPUT_PATH = os.environ.get('EXCEL_OUTPUT_PATH') or basedir


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

cur_cfg = config['default']
