from flask import Flask
from flask_login import login_manager
from flask_migrate import Migrate
from .models import User, db, login
from flask_mail import Mail
from dotenv import load_dotenv
from .commands import create_tables
import os

mail = Mail()
load_dotenv('.env')

def create_app(config_file='config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    db.init_app(app)
    migrate = Migrate(app, db)
    login.init_app(app)
    login.login_view = 'login'
    mail.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    from app import views

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

    app.cli.add_command(create_tables)

    return app


