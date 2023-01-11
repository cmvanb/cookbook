#-------------------------------------------------------------------------------
# Recipes views
#-------------------------------------------------------------------------------

import os
import uuid

from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for, session

from cookbook.auth.utils import login_required
from cookbook.db import get_db
from cookbook.recipes import parsing, storage, validation

# Recipes blueprint
#-------------------------------------------------------------------------------
blueprint = Blueprint(
    'recipes', __name__, 
    url_prefix='/recipes', 
    static_folder='static', 
    template_folder='templates',
)

# Index view.
#-------------------------------------------------------------------------------
@blueprint.route('')
@login_required
def index():
    user_id = session['user_id']

    recipes = storage.get_all_recipes(user_id)

    return render_template('index.html', recipes=recipes)

# Add recipe view.
#-------------------------------------------------------------------------------
@blueprint.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    def post():
        user_id      = g.user['id']
        title        = request.form['title']
        author       = request.form['author']
        description  = request.form['description']
        source_url   = request.form['source_url']
        servings     = request.form['servings']
        prep_time    = request.form['prep_time']
        cook_time    = request.form['cook_time']
        ingredients  = request.form['ingredients']
        instructions = request.form['instructions']
        image        = request.files['image']

        error = validation.validate_recipe(
            title, author, description, source_url, servings, prep_time,
            cook_time, ingredients, instructions, image)

        if error is not None:
            return (None, error)

        parsed_ingredients = parsing.parse_ingredients(ingredients)

        recipe_id = storage.add_recipe(
            user_id, title, author, description, source_url, servings,
            prep_time, cook_time, instructions, image, parsed_ingredients)

        return (recipe_id, None)

    if request.method == 'POST':
        recipe_id, error = post()

        if error is None:
            return redirect(url_for('.view', id=recipe_id))
        else:
            flash(error)

    return render_template('add.html')

# Edit recipe view.
#-------------------------------------------------------------------------------
@blueprint.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    user_id = session['user_id']

    def post():
        title        = request.form['title']
        author       = request.form['author']
        description  = request.form['description']
        source_url   = request.form['source_url']
        servings     = request.form['servings']
        prep_time    = request.form['prep_time']
        cook_time    = request.form['cook_time']
        ingredients  = request.form['ingredients']
        instructions = request.form['instructions']
        image        = request.files['image']

        error = validation.validate_recipe(
            title, author, description, source_url, servings, prep_time,
            cook_time, ingredients, instructions, image)

        if error is not None:
            return error

        parsed_ingredients = parsing.parse_ingredients(ingredients)

        storage.edit_recipe(
            id, user_id, title, author, description, source_url, servings,
            prep_time, cook_time, instructions, image, parsed_ingredients)

        return None

    if request.method == 'POST':
        error = post()

        if error is None:
            return redirect(url_for('.view', id=id))
        else:
            flash(error)

    recipe = storage.get_recipe(id, user_id)
    recipe_ingredients_text = storage.get_recipe_ingredients_text(id)

    return render_template(
        'edit.html',
        recipe=recipe,
        recipe_ingredients_text=recipe_ingredients_text)

# View recipe view.
#-------------------------------------------------------------------------------
@blueprint.route('/view/<int:id>')
@login_required
def view(id):
    user_id = session['user_id']

    recipe = storage.get_recipe(id, user_id)
    recipe_ingredient_maps = storage.get_recipe_ingredient_maps(id)

    return render_template(
        'view.html',
        recipe=recipe,
        recipe_ingredient_maps=recipe_ingredient_maps)

# Delete recipe view.
#-------------------------------------------------------------------------------
@blueprint.route('/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    user_id = session['user_id']

    storage.delete_recipe(id, user_id)

    return redirect(url_for('.index'))

