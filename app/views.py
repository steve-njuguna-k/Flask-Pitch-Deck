from app import app
from flask import render_template, flash, redirect, request, session, logging, url_for
from .forms import RegisterForm, LoginForm
from .models import UserModel, db
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    # Creating Login form object
    form = LoginForm(request.form)
    # verifying that method is post and form is valid
    if request.method == 'POST' and form.validate:
        # checking that user is exist or not by email
        user = UserModel.query.filter_by(email = form.email.data).first()

        if user:
            # if user exist in database than we will compare our database hased password and password come from login form 
            if check_password_hash(user.password, form.password.data):
                # if password is matched, allow user to access and save email and username inside the session
                flash('You have successfully logged in.', "success")

                session['logged_in'] = True
                session['email'] = user.email 
                # After successful login, redirecting to home page
                return redirect(url_for('home'))

            else:
                # if password is in correct , redirect to login page
                flash('Email Address or Password Is Incorrect! Please Try Again.', "Danger")

                return redirect(url_for('login'))
    # rendering login page
    return render_template('Login.html', form = form)


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