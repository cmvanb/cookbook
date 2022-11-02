import os
import uuid

from flask import (
    Blueprint, current_app, flash, g, redirect, render_template, request, url_for, session
    )
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename

from cookbook.auth import login_required
from cookbook.db import get_db

# TODO: Extract to utility?
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def file_allowed(file):
    return file.mimetype[0:5] == 'image' \
           and '.' in file.filename \
           and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

bp = Blueprint('recipes', __name__, url_prefix='/recipes')

@bp.route('/')
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
        instructions = request.form['instructions']

        # TODO: POST tags and ingredients.

        image = request.files['image']
        if image is not None:
            if image.filename == '':
                error = 'Non-existent image was selected.'
            elif not file_allowed(image):
                error = 'Image format not allowed.'
            else:
                filename = str(uuid.uuid4())
                # filename = secure_filename(image.filename)

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
        elif not instructions:
            error = 'Instructions is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            sql = """
                INSERT INTO recipe (
                    user_id, title, author, description,  source_url,
                    image_path, servings, prep_time,  cook_time, instructions)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
            args = (g.user['id'], title, author, description, source_url,
                image_path, servings, prep_time, cook_time, instructions)
            recipe = db.execute(sql, args).fetchone()
            db.commit()
            return redirect(url_for('recipes.view', id=recipe['id']))

    return render_template('recipes/add.html')

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
        abort(404, f"Recipe id {id} does not exist.")

    # NOTE: SQL shouldn't return recipe that doesn't belong to user, this is defensive.
    if recipe['user_id'] != g.user['id']:
        abort(403)

    return recipe

@bp.route('/view/<int:id>')
@login_required
def view(id):
    recipe = get_recipe(id)
    return render_template('recipes/view.html', recipe=recipe)
