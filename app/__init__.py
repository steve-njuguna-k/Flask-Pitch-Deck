from flask import Flask
from flask_migrate import Migrate
from .models import db, login
from flask_mail import Mail

mail = Mail()

app = Flask(__name__)

from app import views

# Database Configuration and Creating object of SQLAlchemy
app.config['SECRET_KEY'] = "+09vcm=z94^g3%ai)v0ip$*i0p!w^+y)6q=&ay8ll-ukei_x5n"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:12345@localhost:5432/pitchDeckDB"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_SALT'] = app.config['SECRET_KEY']

db.init_app(app)
migrate = Migrate(app, db)

login.init_app(app)
login.login_view = 'login'

mail.init_app(app)
