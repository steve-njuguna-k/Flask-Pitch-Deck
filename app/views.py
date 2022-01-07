from app import app
from flask import render_template, flash, redirect, request, session, url_for
from .models import UserModel, db
from flask_login import current_user, login_user, logout_user

@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
     
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('home'))
     
    return render_template('Login.html')


@app.route('/register/', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
     
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
 
        if UserModel.query.filter_by(email = email).first():
            flash('Email already Present')

        else:   
            user = UserModel(first_name = first_name, last_name = last_name, email = email, password=password)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('Register.html')
        

@app.route('/logout')
def logout():
    logout_user()
    # redirecting to home page
    return redirect(url_for('home'))