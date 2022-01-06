from flask import Flask
from flask_migrate import Migrate
from .models import db

app = Flask(__name__)

from app import views

# Database Configuration and Creating object of SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:12345@localhost:5432/pitchDeckDB"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)