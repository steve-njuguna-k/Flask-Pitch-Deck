from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import DataRequired

# Creating Login Form contains email and password
class LoginForm(Form):
    email = StringField("Email", validators=[validators.Length(min=7, max=50), validators.DataRequired(message="Please Fill This Field")])
    password = PasswordField("Password", validators=[validators.DataRequired(message="Please Fill This Field")])

# Creating Registration Form contains username, name, email, password and confirm password.
class RegisterForm(Form):
    first_name = StringField("First Name", validators=[validators.Length(min=3, max=25), validators.DataRequired(message="Please Fill This Field")])
    last_name = StringField("Last Name", validators=[validators.Length(min=3, max=25), validators.DataRequired(message="Please Fill This Field")])
    email = StringField("Email Address", validators=[validators.Email(message="Please enter a valid email address")])
    password = PasswordField("Password", validators=[
        validators.DataRequired(message="Please Fill This Field"),
        validators.EqualTo(fieldname="confirm", message="Your Passwords Do Not Match")
    ])
    confirm = PasswordField("Confirm Password", validators=[validators.DataRequired(message="Please Fill This Field")])