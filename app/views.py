import datetime
from app import app
from flask import render_template, flash, redirect, request, url_for
from .email import send_email
from .models import Comment, Like, UserModel, db, Pitch
from flask_login import current_user, login_user, logout_user, login_required
from .forms import CommentsForm, LoginForm, RegisterForm, PitchForm
from flask_bcrypt import Bcrypt
from .token import confirm_token, generate_confirmation_token
bcrypt = Bcrypt(app)

@app.route('/', methods=['POST','GET'])
def home():
    pitches = Pitch.query.all()
    user = current_user._get_current_object()
    form = PitchForm()
    if form.validate_on_submit():
        pitch_body = form.pitch_body.data
        category = form.category.data
        user_id = current_user._get_current_object().id

        pitch_obj = Pitch(user_id = user_id, pitch_body = pitch_body, category = category)
        db.session.add(pitch_obj)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('Index.html', form = form, pitches = pitches, user = user)

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = UserModel.query.filter_by(email=form.email.data).first()
        if user and user.confirmed ==0:
            flash('⚠️ Your Acount Is Not Activated! Please Check Your Email Inbox And Click The Activation Link We Sent To Activate It', 'danger')
            return render_template('Login.html', form=form)

        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('home'))
        
        if user and not bcrypt.check_password_hash(user.password, request.form['password']):
            flash('⚠️ Invalid Password!', 'danger')
            return render_template('Login.html', form=form)

        if not user and bcrypt.check_password_hash(user.password, request.form['password']):
            flash('⚠️ Invalid Email Address!', 'danger')
            return render_template('Login.html', form=form)

        if not user:
            flash('⚠️ Account Does Not Exist!', 'danger')
            return render_template('Login.html', form=form)

    return render_template('Login.html', form=form)

@app.route('/register/', methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = UserModel(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=password, confirmed=False)
        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('confirm_email', token=token, _external=True)
        html = render_template('Activation.html', confirm_url=confirm_url)
        subject = "[PITCH DECK] Confrim Your Email Address"
        send_email(user.email, subject, html)

        return redirect(url_for("email_verification_sent"))

    return render_template('Register.html', form=form)
        
@app.route('/logout')
@login_required
def logout():
    user = current_user
    user.authenticated = False
    logout_user()
    # redirecting to home page
    return redirect(url_for('home'))

@app.route('/confirm/<token>')
def confirm_email(token):
    if UserModel.confirmed==1:
        flash('✅ Account Already Confirmed! You Can Log In.', 'success')
        return redirect(url_for('login'))

    email = confirm_token(token)
    user = UserModel.query.filter_by(email=email).first_or_404()

    if user.email == email:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('✅ You Have Successfully Confirmed Your Email Address. You Can Now Log In. Thanks!', 'success')
    else:
        flash('⚠️ The Confirmation Link Is Invalid Or Has Expired.', 'danger')

    return redirect(url_for('login'))

@app.route('/sent')
def email_verification_sent():
    if UserModel.confirmed==1:
        flash('✅ You Can Now Log In!', 'success')
        return redirect(url_for('login'))
    else:
        flash('✅ Registration Successful! A Confirmation Link Has Been Sent To The Registered Email Address.', 'success')
        return redirect(url_for('register'))

@app.route('/pitches')
@login_required
def my_pitches():
    form = PitchForm
    pitches = Pitch.query.filter_by(user_id = current_user._get_current_object().id)
    return render_template('Pitches.html', pitches = pitches, form = form)

@app.route('/add-comment/<pitch>', methods=['POST','GET'])
@login_required
def addComment(pitch):
    form = CommentsForm()
    pitch = Pitch.query.filter_by(id = pitch).first()
    comments = Comment.query.filter_by(pitches_id = pitch.id)
    comment = form.comment.data
    user_id = current_user._get_current_object().id

    if form.validate_on_submit():
        comment=Comment(comment = comment, pitch = pitch, user_id = user_id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('pitches'))
    return render_template('Add Comment.html', form = form, pitch = pitch, comments = comments)

@app.route('/profile',methods=['POST','GET'])
@login_required
def profile():
    user = current_user._get_current_object()
    return render_template('Profile.html', user = user)

@app.route('/likes/<id>',methods=['POST','GET'])
@login_required
def like(id):
    pitch_id = Pitch.query.filter_by(id = id).first()
    likes = Like.query.filter_by(pitches_id = id).all()

@app.route('/pitches/business', methods=['GET'])
def business():
    pitches = Pitch.query.filter_by(category = "Business Pitches").order_by(Pitch.category.desc())
    return render_template('Business.html', pitches = pitches)

@app.route('/pitches/all', methods=['GET'])
def pitches():
    pitches = Pitch.query.all()
    return render_template('All Pitches.html', pitches = pitches)

@app.route('/pitches/creative', methods=['GET'])
def creative():
    pitches = Pitch.query.filter_by(category = "Creative Pitches").order_by(Pitch.category.desc())
    return render_template('Creative.html', pitches = pitches)

@app.route('/pitches/interview', methods=['GET'])
def interview():
    pitches = Pitch.query.filter_by(category = "Interview Pitches").order_by(Pitch.category.desc())
    return render_template('Interview.html', pitches = pitches)

@app.route('/pitches/sales', methods=['GET'])
def sales():
    pitches = Pitch.query.filter_by(category = "Sales Pitches").order_by(Pitch.category.desc())
    return render_template('Sales.html', pitches = pitches)

@app.route('/pitches/product', methods=['GET'])
def product():
    pitches = Pitch.query.filter_by(category = "Product Pitches").order_by(Pitch.category.desc())
    return render_template('Product.html', pitches = pitches)