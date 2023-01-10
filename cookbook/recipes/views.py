#-------------------------------------------------------------------------------
# Recipes views
#-------------------------------------------------------------------------------

import os
import uuid

from flask import Blueprint, current_app, flash, g, redirect, render_template, request, url_for, session
from werkzeug.exceptions import abort

from cookbook.auth.utils import login_required
from cookbook.db import get_db
from cookbook.recipes.utils import image_format_allowed
from cookbook.recipes.parsing import parse_ingredients

# Recipes blueprint
#-------------------------------------------------------------------------------
blueprint = Blueprint(
    'recipes', __name__, 
    url_prefix='/recipes', 
    static_folder='static', 
    template_folder='templates',
)

# TODO: Extract.
# Retrieve a recipe by its ID.
#-------------------------------------------------------------------------------
def get_recipe(id):
    db = get_db()
    sql = """
        SELECT
            r.id, user_id, created, title, author, description, source_url,
            image_path, servings, prep_time, cook_time, instructions
        FROM recipe r
        WHERE r.id = ? AND r.user_id = ?
        """
    args = (id, session['user_id'])
    recipe = db.execute(sql, args).fetchone()

    if recipe is None:
        abort(404, f'Recipe id {id} not found.')

    return recipe

# TODO: Extract.
# Retrieve a recipe's ingredient maps by its ID.
#-------------------------------------------------------------------------------
def get_recipe_ingredient_maps(recipe_id):
    db = get_db()
    sql = """
        SELECT
            id, recipe_id, input_text, count
        FROM recipe_ingredient_map m
        WHERE m.recipe_id = ?
        """
    args = (recipe_id, )
    recipe_ingredient_maps = db.execute(sql, args).fetchall()

    return recipe_ingredient_maps

# Validation logic.
#-------------------------------------------------------------------------------
def validate_recipe(title, author, description, source_url, servings, prep_time,
                    cook_time, ingredients, instructions, image):
    # TODO: Make some of these optional.
    if not title:
        return 'Title is required.'
    if not author:
        return 'Author is required.'
    if not description:
        return 'Description is required.'
    if not source_url:
        return 'Source URL is required.'
    if not servings:
        return 'Servings is required.'
    if not prep_time:
        return 'Prep Time is required.'
    if not cook_time:
        return 'Cook Time is required.'
    if not ingredients:
        return 'Ingredients is required.'
    if not instructions:
        return 'Instructions is required.'
    if not image:
        return 'Image is required.'

    # TODO: Perform validation on:
    # Source URL
    # Servings
    # Prep Time
    # Cook Time
    # Tags
    # Ingredients

    if image.filename == '':
        return 'Non-existent image was selected.'
    elif not image_format_allowed(image):
        return 'Image format not allowed.'

    return None

# Index view.
#-------------------------------------------------------------------------------
@blueprint.route('')
@login_required
def index():
    db = get_db()
    sql = """
        SELECT r.id, user_id, created, title, description, image_path
        FROM recipe r WHERE r.user_id = ?
        ORDER BY title ASC
        """
    args = (session['user_id'], )
    recipes = db.execute(sql, args).fetchall()
    return render_template('index.html', recipes=recipes)

# Add recipe view.
#-------------------------------------------------------------------------------
@blueprint.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        user         = g.user['id']
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

        error = validate_recipe(
            title, author, description, source_url, servings, prep_time,
            cook_time, ingredients, instructions, image,
        )

        if error is not None:
            flash(error)
            return render_template('add.html')

        parsed_ingredients = parse_ingredients(ingredients)

        # Save image to disk and save relative path for storage in database.
        image = request.files['image']
        image_file_name = str(uuid.uuid4())
        # TODO: Use blueprint static folder.
        image.save(os.path.join(current_app.static_folder, 'user_images', image_file_name))
        image_path = os.path.join('user_images', image_file_name)

        # Insert recipe row.
        db = get_db()
        sql = """
            INSERT INTO recipe (
                user_id, title, author, description, source_url,
                image_path, servings, prep_time, cook_time, instructions
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING id
            """
        recipe = db.execute(sql, (
                user, title, author, description, source_url, image_path,
                servings, prep_time, cook_time, instructions
            )).fetchone()
        db.commit()

        recipe_id = recipe['id']

        # TODO: If new ingredient(s) detected, insert ingredient row(s).

        # Insert recipe_ingredient_map rows.
        for ingredient in parsed_ingredients:
            print(f'{ingredient.count} {ingredient.unit.long_name} of {ingredient.name}')
            sql = """
                INSERT INTO recipe_ingredient_map (
                    recipe_id, input_text, count
                    )
                VALUES (?, ?, ?)
                """
            args = (recipe_id, ingredient.name, ingredient.count)
            db.execute(sql, args)
            db.commit()

        return redirect(url_for('.view', id=recipe_id))

    return render_template('add.html')

# Edit recipe view.
#-------------------------------------------------------------------------------
@blueprint.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    if request.method == 'POST':
        # TODO: Implement.

        return redirect(url_for('.view', id=id))

    recipe = get_recipe(id)
    recipe_ingredient_maps = get_recipe_ingredient_maps(id)

    # TODO: Replace this hack with proper ingredient parsing.
    recipe_ingredients_text = ''
    [recipe_ingredients_text := \
        recipe_ingredients_text + map['input_text'] + \
        ('\n' if i < len(recipe_ingredient_maps) - 1 else '') \
        for i, map in enumerate(recipe_ingredient_maps)]

    return render_template(
        'edit.html',
        recipe=recipe,
        recipe_ingredients_text=recipe_ingredients_text
        )

# View recipe view.
#-------------------------------------------------------------------------------
@blueprint.route('/view/<int:id>')
@login_required
def view(id):
    recipe = get_recipe(id)
    recipe_ingredient_maps = get_recipe_ingredient_maps(id)

    return render_template(
        'view.html',
        recipe=recipe,
        recipe_ingredient_maps=recipe_ingredient_maps
        )

# Delete recipe view.
#-------------------------------------------------------------------------------
@blueprint.route('/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    # To check whether recipe exists, will abort otherwise.
    get_recipe(id)

    # TODO: Delete associated images.

    db = get_db()
    db.execute('DELETE FROM recipe WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('.index'))

