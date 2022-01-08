from flask import Flask
from flask_migrate import Migrate
from .models import db, login
from flask_mail import Mail
import os

mail = Mail()

app = Flask(__name__)

from app import views

# Database Configuration and Creating object of SQLAlchemy
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
app.config['SECURITY_PASSWORD_SALT'] = os.environ['SECURITY_PASSWORD_SALT']

db.init_app(app)
migrate = Migrate(app, db)

login.init_app(app)
login.login_view = 'login'

mail.init_app(app)
