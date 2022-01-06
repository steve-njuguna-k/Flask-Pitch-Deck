from flask import Flask, render_template, flash, redirect, request, session, logging, url_for
from flask_sqlalchemy import SQLAlchemy
from .forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

from app import views

# Database Configuration and Creating object of SQLAlchemy

app.config['SECRET_KEY'] = '!9m@S-dThyIlW[pHQbN^'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create User Model which contains id [Auto Generated], first_name, last_name, email and password
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name= db.Column(db.String(15), unique=True)
    last_name = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256), unique=True)

    def __init__(self, id, first_name, last_name, email, password):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Email Address: {}>'.format(self.email)