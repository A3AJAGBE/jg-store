import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    """Base config, uses staging database server."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Database Configs
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT') or 25
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['aminatajagbe@yahoo.com']


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
