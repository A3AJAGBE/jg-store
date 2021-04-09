from flask import render_template
from datetime import datetime
from store import app
from store.forms import *

# Get the year
current_year = datetime.now().year


@app.route('/')
def index():
    return render_template('index.html', year=current_year)


@app.route('/register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        pass
    return render_template('register.html', year=current_year, form=form)


@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template('login.html', year=current_year, form=form)
