#-------------------------------------------------------------------------------
# Recipes views
#-------------------------------------------------------------------------------

from flask import Blueprint, flash, g, redirect, render_template, request, url_for, session, send_file

from cookbook.auth.utils import login_required
from cookbook.recipes import parsing, storage, validation, exporter


blueprint = Blueprint(
    'recipes', __name__, 
    url_prefix='/recipes', 
    static_folder='static', 
    template_folder='templates',
)


@blueprint.route('')
@login_required
def index():
    """ Index view. Shows all recipes for the current user. """

    user_id = session['user_id']

    recipes = storage.get_all_recipes(user_id)

    return render_template('index.html', recipes=recipes)


@blueprint.route('/add', methods=('GET', 'POST'))
@login_required
def add():
    """ Add recipe view. """

    def post():
        """ POST validates recipe form data, parses ingredients and adds the
        recipe to the database. """

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

    status = 200

    if request.method == 'POST':
        recipe_id, error = post()

        if error is None:
            return redirect(url_for('.view', id=recipe_id))
        else:
            flash(error)
            status = 400

    return render_template('add.html'), status


@blueprint.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    """ Edit recipe view. """

    user_id = session['user_id']

    def post():
        """ POST validates recipe form data, parses ingredients and edits the
        recipe in the database. """

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

    status = 200

    if request.method == 'POST':
        error = post()

        if error is None:
            return redirect(url_for('.view', id=id))
        else:
            flash(error)
            status = 400

    recipe = storage.get_recipe(id, user_id)
    recipe_ingredients_text = storage.get_recipe_ingredients_text(id)

    return render_template(
        'edit.html',
        recipe=recipe,
        recipe_ingredients_text=recipe_ingredients_text), status


@blueprint.route('/view/<int:id>')
@login_required
def view(id):
    """ View recipe view. Simply renders a recipe. """

    user_id = session['user_id']

    recipe = storage.get_recipe(id, user_id)
    recipe_ingredient_maps = storage.get_recipe_ingredient_maps(id)

    return render_template(
        'view.html',
        recipe=recipe,
        recipe_ingredient_maps=recipe_ingredient_maps)


@blueprint.route('/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    """ Delete recipe view. Deletes a recipe from the database. """

    user_id = session['user_id']

    storage.delete_recipe(id, user_id)

    return redirect(url_for('.index'))


@blueprint.route('/export/<int:id>')
@login_required
def export(id):
    """ Export recipe view. Exports a recipe as a YAML file. """

    user_id = session['user_id']

    recipe = storage.get_recipe(id, user_id)
    recipe_ingredient_maps = storage.get_recipe_ingredient_maps(id)

    ingredients_list = parsing.parse_ingredients_list(recipe_ingredient_maps)
    instructions_list = parsing.parse_instructions_list(recipe['instructions'])

    file_name = exporter.recipe_file_name(recipe['title'])
    yaml = exporter.recipe_to_yaml(recipe, ingredients_list, instructions_list)

    return send_file(yaml, download_name=file_name, as_attachment=True)
