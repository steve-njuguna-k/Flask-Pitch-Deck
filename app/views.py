import datetime
from app import app
from flask import render_template, flash, redirect, request, url_for
from .email import send_email
from .models import UserModel, db
from flask_login import current_user, login_user, logout_user, login_required
from .token import confirm_token, generate_confirmation_token
from .forms import LoginForm, RegisterForm

@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
     
    if request.method == 'POST':
        email = request.form['email']
        user = UserModel.query.filter_by(email = email).first()
        if user.email_verified==False:
            flash('⚠️ Email is not verified, please check your inbox', 'danger')
            
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('home'))
        if not user:
            flash('⚠️ Incorrect Email or Password! Try Again', 'danger')
     
    return render_template('Login.html', form = form)


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
            flash('⚠️ Email Already Taken! Choose Another One', 'danger')

        else:   
            user = UserModel(first_name = first_name, last_name = last_name, email = email, password = password, confirmed = False)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            token = generate_confirmation_token(user.email)
            confirm_url = url_for('confirm_email', token = token, _external = True)
            html = render_template('Activation.html', confirm_url = confirm_url)
            subject = "Please Confirm Your Email Address"
            send_email(user.email, subject, html)

            flash('✅ Registration Successful! Check Your Email  For A Verification Link', 'success')
            return redirect(url_for('register'))

    return render_template('Register.html')
        

@app.route('/logout')
def logout():
    logout_user()
    # redirecting to home page
    return redirect(url_for('home'))

@login_required
@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('⚠️ The confirmation link is invalid or has expired!', 'danger')
    user = UserModel.query.filter_by(email=email).first_or_404()

    if user.confirmed:
        flash('✅ Account already confirmed! Procee to log in.', 'success')

    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('✅ You have confirmed your account! You can now log in', 'success')

    return redirect(url_for('login'))

@login_required
@app.route('/unconfirmed')
def unconfirmed():
    if current_user.confirmed:
        return redirect('home')
    else:
        flash('⚠️ Please Confirm Your Email Address!', 'warning')
        
    return render_template('Login.html')