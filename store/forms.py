from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators, TextAreaField


class RegisterForm(FlaskForm):
    first_name = StringField("First Name", [validators.InputRequired(message="This field cannot be empty."),
                                            validators.Length(min=2, max=50,
                                                              message="First name must be between 2 to 50 characters.")
                                            ])
    last_name = StringField("Last Name", [validators.InputRequired(message="This field cannot be empty."),
                                          validators.Length(min=2, max=50,
                                                            message="Last name must be between 2 to 50 characters.")])
    email = StringField("Email Address", [validators.InputRequired(message="This field cannot be empty."),
                                          validators.Email(message="That is not a valid email address.")])
    password = PasswordField("Password", [validators.InputRequired(message="This field cannot be empty."),
                                          validators.Length(min=8, message="Password must be at least 8 characters.")])
    submit = SubmitField("Create an account")


class LoginForm(FlaskForm):
    email = StringField("Email Address", [validators.InputRequired(message="This field cannot be empty."),
                                          validators.Email(message="That is not a valid email address.")])
    password = PasswordField("Password", [validators.InputRequired(message="This field cannot be empty."),
                                          validators.Length(min=8, message="Password must be at least 8 characters.")])
    submit = SubmitField("Log in")


class NewEmailConfirmationRequestForm(FlaskForm):
    email = StringField("Registered Email Address", [validators.InputRequired(message="This field cannot be empty."),
                                                     validators.Email(message="That is not a valid email address.")])
    submit = SubmitField("Submit request")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Registered Email Address", [validators.InputRequired(message="This field cannot be empty."),
                                                     validators.Email(message="That is not a valid email address.")])
    submit = SubmitField("Submit request")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("New Password", [validators.InputRequired(message="This field cannot be empty."),
                                              validators.Length(min=8,
                                                                message="Password must be at least 8 characters.")])
    submit = SubmitField("Reset password")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", [validators.InputRequired(message="This field cannot be empty."),
                                                  validators.Length(min=8,
                                                                    message="Password must be at least 8 characters.")])
    new_password = PasswordField("New Password", [validators.InputRequired(message="This field cannot be empty."),
                                                  validators.Length(min=8,
                                                                    message="Password must be at least 8 characters.")])
    submit = SubmitField("Change password")


class ContactForm(FlaskForm):
    name = StringField('Name', [validators.InputRequired(message="This field cannot be empty."),
                                validators.Length(min=5, max=100,
                                                  message="Name must be between 5 to 100 characters.")])
    email = StringField('Email Address', [validators.InputRequired(message="This field cannot be empty."),
                                          validators.Email(message="That is not a valid email address.")])
    message = TextAreaField('Message', [validators.InputRequired(message="This field cannot be empty."),
                                        validators.Length(min=10,
                                                          message="Message must be at least 10 characters.")
                                        ])
    submit = SubmitField('Send message')
