from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, welcome to the home page!'

@app.route('/login')
def login():
    return 'This is the login page!'

@app.route('/recipe/')
def recipes_overview():
    return render_template('recipes-overview.html')

@app.route('/recipe/<string:recipe_id>')
def recipe_view(recipe_id):
    return 'View recipe with id: %s' % recipe_id
