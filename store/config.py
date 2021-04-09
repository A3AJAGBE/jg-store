import os
from dotenv import load_dotenv
load_dotenv()


class Config(object):
    """Base config, uses staging database server."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True