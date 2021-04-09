from flask import Flask
from store.config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

from store import views
