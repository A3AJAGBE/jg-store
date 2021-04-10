from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from store import app, db, login_manager
from store.forms import *
from store.models import Users
from store.emails import generate_token, confirm_token, email_confirmation

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

            token = generate_token(email)
            user_email = email
            confirm_email_url = url_for('confirm_email', token=token, _external=True)
            text_body = render_template('emails/email_confirmation.txt', confirm_email_url=confirm_email_url)
            html_body = render_template('emails/email_confirmation.html', confirm_email_url=confirm_email_url)
            email_confirmation(user_email, text_body, html_body)

            flash(f'Registration successful {new_user.first_name}, check for email confirmation in your inbox',
                  "success")
            return redirect(url_for('index'))
    return render_template('auth/register.html', year=current_year, form=form)


@app.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    email = confirm_token(token)
    # flash('The confirmation link is Invalid or has expired', 'danger')

    user = Users.query.filter_by(email=email).first_or_404()

    if user.email_confirmed:
        flash(f'{user.first_name}, you have confirmed that email. Kindly login.', 'info')
        return redirect(url_for('login'))
    else:
        user.email_confirmed = True
        user.email_confirmed_at = datetime.utcnow()
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f'Email confirmation successful {user.first_name}, you are now logged in.', 'success')
        return redirect(url_for('index'))


@app.route('/unconfirmed')
def email_unconfirmed():
    if current_user.is_authenticated and current_user.email_confirmed:
        return redirect(url_for('index'))
    return render_template('auth/email_unconfirmed.html')


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
            if user.email_confirmed:
                login_user(user)
                flash('You are logged in successfully', "success")
                return redirect(url_for('index'))
            else:
                flash('You are yet to confirm your email address.', "danger")
                return redirect(url_for('email_unconfirmed'))
    return render_template('auth/login.html', year=current_year, form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You are logged out successfully', "success")
    return redirect(url_for('index'))


@app.route('/profile/<name>')
@login_required
def profile(name):
    user = Users.query.filter_by(first_name=name).first_or_404()
    return render_template('profile.html', year=current_year, profile=user)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if current_user.is_authenticated:
        flash("You are unable to view that page because you are currently logged in.", "info")
        return redirect(url_for('index'))
    return render_template('auth/reset_password_request.html', year=current_year, form=form)
