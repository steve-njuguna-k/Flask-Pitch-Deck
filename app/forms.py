from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField(label='Email Address', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email Address"})
    password = PasswordField(label='Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})

class RegisterForm(FlaskForm):
    first_name = StringField(label='First Name', validators=[DataRequired(), Length(min=3, max=255)])
    last_name = StringField(label='Last Name', validators=[DataRequired(), Length(min=3, max=255)])
    email = StringField(label='Email Address', validators=[DataRequired(), Email(), Length(min=6, max=255)])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=6, max=255)])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])