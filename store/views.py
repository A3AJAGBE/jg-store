from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from store import app, db, login_manager
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
    if current_user.is_authenticated:
        flash("You are unable to view that page because you are currently logged in.", "info")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        first_name = request.form['first_name'].title()
        last_name = request.form['last_name'].title()
        email = request.form['email']
        password = request.form['password']

        # Make sure the email does not exist
        if Users.query.filter_by(email=email).first():
            flash("That email exists in the database.", "danger")
        else:
            encrypt_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

            new_user = Users(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=encrypt_password,
            )
            db.session.add(new_user)
            db.session.commit()

            # Log in and authenticate user after adding details to database.
            login_user(new_user)
            flash(f"Registered successfully {first_name}, you're now logged in.", "success")
            return redirect(url_for('index'))
    return render_template('register.html', year=current_year, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash("You are unable to view that page because you are currently logged in.", "info")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        email = request.form['email']
        password = request.form['password']

        # Find the user by email
        user = Users.query.filter_by(email=email).first()

        if not user:
            flash("Invalid email address, try again.", "danger")
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, try again.', "danger")
        else:
            login_user(user)
            flash('You are logged in successfully', "success")
            return redirect(url_for('index'))
    return render_template('login.html', year=current_year, form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You are logged out successfully', "success")
    return redirect(url_for('index'))
