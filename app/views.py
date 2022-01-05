from app import app
from flask import render_template

@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/register')
def register():
    return render_template('Register.html')