from app import app
from flask import render_template, flash, redirect, request, session, logging, url_for
from .forms import RegisterForm, LoginForm
from .models import UserModel, db
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/login/')
def login():
    return render_template('Login.html')

@app.route('/register/', methods = ['GET', 'POST'])
def register():
     # Creating RegistrationForm class object
    form = RegisterForm(request.form)

    # Cheking that method is post and form is valid or not.
    if request.method == 'POST' and form.validate():
        # if all is fine, generate hashed password
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        # create new user model object
        new_user = UserModel(
            first_name = form.first_name.data, 
            last_name = form.last_name.data, 
            email = form.email.data, 
            password = hashed_password )

        # saving user object into data base with hashed password
        db.session.add(new_user)
        db.session.commit()

        flash('Account Successfully Created! You Can Now Log In', 'success')

        # if registration successful, then redirecting to login Page
        return redirect(url_for('login'))

    else:
        # if method is Get, than render registration form
        return render_template('Register.html', form = form)