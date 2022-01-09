from flask_mail import Mail, Message
from flask import app
from .config import MAIL_DEFAULT_SENDER

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients = [to],
        html = template,
        sender = MAIL_DEFAULT_SENDER
    )
    Mail.send(msg)