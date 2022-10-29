from flask import Flask
from flask import render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('recipes_overview'))

# TODO: Implement authentication.
@app.route('/login')
def login():
    return 'This is the login page!'

@app.route('/recipe')
def recipes_overview():
    return render_template('recipes-overview.html', seq=range(20))

@app.route('/recipe/<string:recipe_id>')
def recipe_view(recipe_id):
    return 'View recipe with id: %s' % recipe_id
