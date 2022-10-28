from flask import Flask

app = Flask(__name__)

@app.route('/')
def home_page():
    return 'Hello, welcome to the home page!'

@app.route('/login')
def login():
    return 'This is the login page!'
