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

    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    ADMINS = ['admin@thejewelrygallery.com.ng']

    SECURITY_SALT = os.environ.get('SECURITY_SALT')


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
