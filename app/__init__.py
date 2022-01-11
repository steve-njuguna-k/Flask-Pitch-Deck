from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .models import login
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

mail = Mail()
app = Flask(__name__)

db = SQLAlchemy(app)

from app import views

#load .env variables
load_dotenv('.env')
app.config.from_pyfile('config.py')

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

#create postgresql database (flask db init, flask db migrate, flask db upgrade)
db.init_app(app)
migrate = Migrate(app, db)

#initialize flask-login module
login.init_app(app)
login.login_view = 'login'

#initialize flask-mail module
mail.init_app(app)

#initialize flask-bcrypt module
bcrypt = Bcrypt(app)
