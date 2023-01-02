import os
import uuid

from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, url_for, session
    )
from werkzeug.exceptions import abort

from cookbook.auth import login_required
from cookbook.db import get_db
from cookbook.parsing.ingredient_parser import IngredientParser

# TODO: Extract to utility?
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def file_allowed(file):
    return file.mimetype[0:5] == 'image' \
           and '.' in file.filename \
           and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

bp = Blueprint('recipes', __name__, url_prefix='/recipes')

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
        abort(404, f"Recipe id {id} not found.")

    return recipe

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

@bp.route('')
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
    return render_template('recipes/index.html', recipes=recipes)

@bp.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    if request.method == 'POST':
        error = None

        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        source_url = request.form['source_url']
        servings = request.form['servings']
        image_path = None
        prep_time = request.form['prep_time']
        cook_time = request.form['cook_time']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        # Validate image.
        image = request.files['image']
        if image is not None:
            if image.filename == '':
                error = 'Non-existent image was selected.'
            elif not file_allowed(image):
                error = 'Image format not allowed.'
            else:
                filename = str(uuid.uuid4())

                # Save image to disk.
                image.save(os.path.join(current_app.static_folder, 'user_images', filename))

                # Store relative path in database.
                image_path = os.path.join('user_images', filename)
        else:
            error = 'Image not in request.'

        # TODO: Perform validation on:
        # Source URL
        # Servings
        # Prep Time
        # Cook Time
        # Tags
        # Ingredients

        if not title:
            error = 'Title is required.'
        elif not author:
            error = 'Author is required.'
        elif not description:
            error = 'Description is required.'
        elif not source_url:
            error = 'Source URL is required.'
        elif image_path == None:
            error = 'Image could not be uploaded.'
        elif not servings:
            error = 'Servings is required.'
        elif not prep_time:
            error = 'Prep Time is required.'
        elif not cook_time:
            error = 'Cook Time is required.'
        elif not ingredients:
            error = 'Ingredients is required.'
        elif not instructions:
            error = 'Instructions is required.'

        # Parse ingredients.
        ingredient_parser = IngredientParser()
        parsed_ingredients = ingredient_parser.Parse(ingredients)

        if error is not None:
            flash(error)
            return render_template('recipes/add.html')

        db = get_db()

        # Insert recipe row.
        sql = """
            INSERT INTO recipe (
                user_id, title, author, description, source_url,
                image_path, servings, prep_time, cook_time, instructions
                )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING id
            """
        args = (g.user['id'], title, author, description, source_url,
            image_path, servings, prep_time, cook_time, instructions)
        recipe = db.execute(sql, args).fetchone()
        db.commit()

        recipe_id = recipe['id']

        # TODO: If new ingredient(s) detected, insert ingredient row(s).

        # Insert recipe_ingredient_map rows.
        for ingredient in parsed_ingredients:
            print(f"{ingredient.count} {ingredient.unit.long_name} of {ingredient.name}")
            sql = """
                INSERT INTO recipe_ingredient_map (
                    recipe_id, input_text, count
                    )
                VALUES (?, ?, ?)
                """
            args = (recipe_id, ingredient.name, ingredient.count)
            db.execute(sql, args)
            db.commit()

        return redirect(url_for('recipes.view', id=recipe_id))

    return render_template('recipes/add.html')

@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    recipe = get_recipe(id)

    if request.method == 'POST':
        return redirect(url_for('recipes.view', id=recipe_id))

    recipe_ingredient_maps = get_recipe_ingredient_maps(id)

    # TODO: Replace this hack with proper ingredient parsing.
    recipe_ingredients_text = ''
    [recipe_ingredients_text := \
        recipe_ingredients_text + map['input_text'] + \
        ('\n' if i < len(recipe_ingredient_maps) - 1 else '') \
        for i, map in enumerate(recipe_ingredient_maps)]

    return render_template(
        'recipes/edit.html',
        recipe=recipe,
        recipe_ingredients_text=recipe_ingredients_text
        )

@bp.route('/view/<int:id>')
@login_required
def view(id):
    recipe = get_recipe(id)
    recipe_ingredient_maps = get_recipe_ingredient_maps(id)

    return render_template(
        'recipes/view.html',
        recipe=recipe,
        recipe_ingredient_maps=recipe_ingredient_maps
        )

@bp.route('/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    # To check whether recipe exists, will abort otherwise.
    get_recipe(id)

    # TODO: Delete associated images.

    db = get_db()
    db.execute('DELETE FROM recipe WHERE id = ?', (id,))
    db.commit()

    return redirect(url_for('recipes.index'))

