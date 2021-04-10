from flask_mail import Message
from store import mail, app
from itsdangerous import URLSafeTimedSerializer


def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_SALT'])


def confirm_token(token, expiration=1800):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    email = serializer.loads(
        token,
        salt=app.config['SECURITY_SALT'],
        max_age=expiration
    )
    return email


def send_email(subject, recipients, text_body, html_body):
    msg = Message(
        subject,
        sender=app.config['MAIL_DEFAULT_SENDER'],
        recipients=recipients,
        body=text_body,
        html=html_body,
    )
    mail.send(msg)


def email_confirmation(user_email, text_body, html_body):
    send_email('[The Jewelry Gallery] Email Confirmation',
               recipients=[user_email],
               text_body=text_body,
               html_body=html_body)


def email_confirmation_resend(user_email, text_body, html_body):
    send_email('[The Jewelry Gallery] New Email Confirmation',
               recipients=[user_email],
               text_body=text_body,
               html_body=html_body)


def email_password_reset(user_email, text_body, html_body):
    send_email('[The Jewelry Gallery] Reset Password',
               recipients=[user_email],
               text_body=text_body,
               html_body=html_body)
