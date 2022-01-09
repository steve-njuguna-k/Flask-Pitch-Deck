from flask import Flask
from flask_migrate import Migrate
from .models import db, login
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

mail = Mail()
app = Flask(__name__)

from app import views
load_dotenv('.env')
app.config.from_pyfile('config.py')

db.init_app(app)
migrate = Migrate(app, db)
login.init_app(app)
login.login_view = 'login'
mail.init_app(app)
bcrypt = Bcrypt(app)
