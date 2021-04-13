from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from itsdangerous import SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from store import app, db, login_manager
from store.forms import *
from store.models import Users, Contact
from store.emails import *

# Get the year
current_year = datetime.now().year


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@app.route('/')
def index():
    return render_template('index.html', year=current_year)


@app.route('/about')
def about():
    return render_template('about.html', year=current_year)





@app.route('/contact_us', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = request.form['name'].title()
        email = request.form['email']
        message = request.form['message']

        user_message = Contact(
            name=name,
            email=email,
            message=message,
        )
        db.session.add(user_message)
        db.session.commit()
        flash(f'Message sent successfully {name}.', "success")
        return redirect(url_for('contact'))
    return render_template('contact.html', year=current_year, form=form)


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
            text_body = render_template('emails/email_confirmation.txt', confirm_email_url=confirm_email_url,
                                        first_name=first_name)
            html_body = render_template('emails/email_confirmation.html', confirm_email_url=confirm_email_url,
                                        first_name=first_name)
            email_confirmation(user_email, text_body, html_body)

            flash(f'Registration successful {first_name}, check for email confirmation in your inbox',
                  "success")
            return redirect(url_for('index'))
    return render_template('auth/register.html', form=form)


@app.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
    try:
        email = confirm_token(token)
    except SignatureExpired:
        flash('The confirmation link is Invalid or has expired', 'danger')
        return redirect(url_for('email_unconfirmed'))
    else:

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


@app.route('/unconfirmed', methods=['GET', 'POST'])
def email_unconfirmed():
    if current_user.is_authenticated and current_user.email_confirmed:
        return redirect(url_for('index'))
    form = NewEmailConfirmationRequestForm()
    if form.validate_on_submit():
        email = request.form['email']

        user = Users.query.filter_by(email=email).first()

        if not user:
            flash('That is not a registered email address.', 'danger')
        elif user.email_confirmed:
            flash('That email address has already been confirmed.', 'danger')
        else:
            token = generate_token(email)
            user_email = email
            confirm_email_url = url_for('confirm_email', token=token, _external=True)
            text_body = render_template('emails/resend_confirmation.txt', confirm_email_url=confirm_email_url,
                                        first_name=user.first_name)
            html_body = render_template('emails/resend_confirmation.html', confirm_email_url=confirm_email_url,
                                        first_name=user.first_name)
            email_confirmation_resend(user_email, text_body, html_body)
            flash(f'A new email confirmation has been sent {user.first_name}.', 'success')
            return redirect(url_for('email_unconfirmed'))
    return render_template('auth/email_unconfirmed.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        flash("You are unable to view that page because you are currently logged in or unauthorised.", "info")
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
    return render_template('auth/login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You are logged out successfully', "success")
    return redirect(url_for('index'))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if current_user.is_authenticated:
        flash("You are unable to view that page because you are currently logged in.", "info")
        return redirect(url_for('index'))
    if form.validate_on_submit():
        email = request.form['email']

        user = Users.query.filter_by(email=email).first()

        if not user:
            flash('That is not a registered email address.', 'danger')
        elif not user.email_confirmed:
            flash('That email address is not confirmed.', 'danger')
        else:
            token = generate_token(email)
            user_email = email
            reset_password_url = url_for('reset_password', token=token, _external=True)
            text_body = render_template('emails/password_reset.txt', reset_password_url=reset_password_url,
                                        first_name=user.first_name)
            html_body = render_template('emails/password_reset.html', reset_password_url=reset_password_url,
                                        first_name=user.first_name)
            email_password_reset(user_email, text_body, html_body)
            flash(f'An email has been sent {user.first_name}, check it for further instructions.', 'success')
            return redirect(url_for('reset_password_request'))
    return render_template('auth/reset_password_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()
    try:
        email = confirm_token(token)
    except SignatureExpired:
        flash('The password reset link is Invalid or has expired, request for another', 'danger')
        return redirect(url_for('reset_password_request'))
    else:
        user = Users.query.filter_by(email=email).first()

        if not user.email_confirmed:
            flash(f'{user.first_name}, you have not confirmed that email. Kindly, confirm before proceeding.', 'info')
            return redirect(url_for('email_unconfirmed'))

        if form.validate_on_submit():
            password = request.form['password']
            encrypt_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            user.password = encrypt_password
            db.session.add(user)
            db.session.commit()

            login_user(user)
            flash(f'Password reset successful {user.first_name}, you are now logged in.', 'success')
            return redirect(url_for('index'))
    return render_template('auth/password_reset.html', form=form)


@app.route('/profile/<name>')
@login_required
def profile(name):
    user = Users.query.filter_by(first_name=name).first_or_404()
    return render_template('profile.html', year=current_year, profile=user)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        encrypt_new_password = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)

        user = Users.query.filter_by(email=current_user.email).first()

        if not check_password_hash(user.password, old_password):
            flash('Old password is incorrect, try again.', 'danger')
        else:
            user.password = encrypt_new_password
            db.session.commit()

            user_email = user.email
            reset_password_request_url = url_for('reset_password_request', _external=True)
            text_body = render_template('emails/password_changed.txt',
                                        reset_password_request_url=reset_password_request_url,
                                        first_name=user.first_name)
            html_body = render_template('emails/password_changed.html',
                                        reset_password_request_url=reset_password_request_url,
                                        first_name=user.first_name)
            email_password_change(user_email, text_body, html_body)

            flash(f'Password successfully changed {user.first_name}.', 'success')
            return redirect(url_for('change_password'))

    return render_template('auth/change_password.html', form=form)
