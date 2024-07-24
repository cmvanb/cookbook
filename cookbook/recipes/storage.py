#-------------------------------------------------------------------------------
# Recipes storage layer
#-------------------------------------------------------------------------------

import os
import uuid
from pathlib import Path

from flask import current_app
from werkzeug.exceptions import abort

from cookbook.db import get_db


def get_all_recipes(user_id):
    """ Retrieve all recipes by user. """

    db = get_db()
    cursor = db.cursor()

    sql = """
        SELECT r.id, user_id, created, title, description, image_path
        FROM recipe r WHERE r.user_id = ?
        ORDER BY title ASC
        """
    args = (user_id, )

    return cursor.execute(sql, args).fetchall()


def get_recipe(recipe_id, user_id):
    """ Retrieve recipe by ID and user. """

    db = get_db()
    cursor = db.cursor()

    sql = """
        SELECT
            r.id, user_id, created, title, author, description, source_url,
            image_path, servings, prep_time, cook_time, instructions
        FROM recipe r
        WHERE r.id = ? AND r.user_id = ?
        """
    args = (recipe_id, user_id)

    recipe = cursor.execute(sql, args).fetchone()
    if recipe is None:
        abort(404, f'Recipe id {recipe_id} not found.')

    return recipe


def get_recipe_ingredient_maps(recipe_id):
    """ Retrieve recipe's ingredient maps by ID. """

    db = get_db()
    cursor = db.cursor()

    sql = """
        SELECT
            id, recipe_id, input_text, count
        FROM recipe_ingredient_map m
        WHERE m.recipe_id = ?
        """
    args = (recipe_id, )

    return cursor.execute(sql, args).fetchall()


# TODO: Remove this hack by implementing proper ingredient parsing at ingest.
def get_recipe_ingredients_text(recipe_id):
    """ Retrieve recipe's ingredients by ID as a flattened list. """

    maps = get_recipe_ingredient_maps(recipe_id)
    recipe_ingredients_text = ''

    [recipe_ingredients_text := \
        recipe_ingredients_text + m['input_text'] + \
        ('\n' if i < len(maps) - 1 else '') \
        for i, m in enumerate(maps)]

    return recipe_ingredients_text


def add_recipe(user_id, title, author, description, source_url, servings,
               prep_time, cook_time, instructions, image, parsed_ingredients):
    """ Add new recipe. """

    image_path = save_user_image(image)
    
    db = get_db()
    cursor = db.cursor()

    # Add recipe.
    sql = """
        INSERT INTO recipe (
            user_id, title, author, description, source_url,
            image_path, servings, prep_time, cook_time, instructions
            )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
    args = (user_id, title, author, description, source_url, image_path, servings,
        prep_time, cook_time, instructions)

    cursor.execute(sql, args)

    recipe_id = cursor.lastrowid

    db.commit()

    # Add ingredient maps.
    for ingredient in parsed_ingredients:
        sql = """
            INSERT INTO recipe_ingredient_map (
                recipe_id, input_text, count
                )
            VALUES (?, ?, ?)
            """
        args = (recipe_id, ingredient.name, ingredient.count)

        cursor.execute(sql, args)
        db.commit()

    return recipe_id


def edit_recipe(recipe_id, user_id, title, author, description, source_url,
                servings, prep_time, cook_time, instructions, image,
                parsed_ingredients):
    """ Edit existing recipe. """

    recipe = get_recipe(recipe_id, user_id)

    delete_user_image(recipe['image_path'])
    image_path = save_user_image(image)

    db = get_db()
    cursor = db.cursor()

    # Update recipe.
    sql = """
        UPDATE recipe
        SET (
            title, author, description, source_url, image_path, servings,
            prep_time, cook_time, instructions
            ) = (?, ?, ?, ?, ?, ?, ?, ?, ?)
        WHERE id = ? AND user_id = ?
        """
    args = (title, author, description, source_url, image_path, servings,
        prep_time, cook_time, instructions, recipe_id, user_id)

    cursor.execute(sql, args)
    db.commit()

    # Delete pre-existing ingredient maps.
    sql = """
        DELETE FROM recipe_ingredient_map
        WHERE recipe_id = ?
        """
    args = (recipe_id, )

    cursor.execute(sql, args)
    db.commit()

    # Add updated ingredient maps.
    for ingredient in parsed_ingredients:
        sql = """
            INSERT INTO recipe_ingredient_map (
                recipe_id, input_text, count
                )
            VALUES (?, ?, ?)
            """
        args = (recipe_id, ingredient.name, ingredient.count)

        cursor.execute(sql, args)
        db.commit()


def delete_recipe(recipe_id, user_id):
    """ Delete existing recipe. """

    recipe = get_recipe(recipe_id, user_id)

    delete_user_image(recipe['image_path'])

    db = get_db()
    cursor = db.cursor()

    # Delete recipe.
    sql = """
        DELETE FROM recipe 
        WHERE id = ? AND user_id = ?
        """
    args = (recipe_id, user_id)

    cursor.execute(sql, args)
    db.commit()

    # Delete ingredient maps.
    sql = """
        DELETE FROM recipe_ingredient_map
        WHERE recipe_id = ?
        """
    args = (recipe_id, )

    cursor.execute(sql, args)
    db.commit()


def save_user_image(image):
    """ Save user uploaded image. """

    path = Path(current_app.config['STATIC_FOLDER']) / 'user_images'
    if not os.path.exists(path):
        os.mkdir(path)

    file_name = str(uuid.uuid4())

    image.save(os.path.join(path, file_name))

    return os.path.join('user_images', file_name)


def delete_user_image(image_path: str):
    """ Delete user uploaded image. """

    path = Path(current_app.config['STATIC_FOLDER']) / image_path

    if os.path.exists(path):
        os.remove(path)
