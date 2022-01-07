from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
login = LoginManager()

# Create User Model which contains id [Auto Generated], first_name, last_name, email and password
class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name= db.Column(db.String(15), unique=True)
    last_name = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(256), unique=True)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<Email Address: {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)
     
    def check_password(self, password):
        return check_password_hash(self.password, password)

#Since Flask_Login knows nothing about databases, we need to create a function to link both of them.
@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))