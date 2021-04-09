from flask import render_template
from datetime import datetime
from store import app, login_manager
from store.forms import RegisterForm, LoginForm
from store.models import Users

# Get the year
current_year = datetime.now().year


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route('/')
def index():
    return render_template('index.html', year=current_year)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        pass
    return render_template('register.html', year=current_year, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return render_template('login.html', year=current_year, form=form)
