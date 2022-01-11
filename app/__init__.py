from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .models import db, login
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

mail = Mail()
app = Flask(__name__)

from app import views

#load .env variables
load_dotenv('.env')
app.config.from_pyfile('config.py')

#create postgresql database (flask db init, flask db migrate, flask db upgrade)
db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

#initialize flask-login module
login.init_app(app)
login.login_view = 'login'

#initialize flask-mail module
mail.init_app(app)

#initialize flask-bcrypt module
bcrypt = Bcrypt(app)
