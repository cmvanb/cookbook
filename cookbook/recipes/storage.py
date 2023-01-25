#-------------------------------------------------------------------------------
# Recipes storage layer
#-------------------------------------------------------------------------------

import os
import uuid

from flask import current_app
from werkzeug.exceptions import abort

from cookbook.db import get_db

# Retrieve all recipes by user.
#-------------------------------------------------------------------------------
def get_all_recipes(user_id):
    db = get_db()

    sql = """
        SELECT r.id, user_id, created, title, description, image_path
        FROM recipe r WHERE r.user_id = ?
        ORDER BY title ASC
        """
    args = (user_id, )

    return db.execute(sql, args).fetchall()

# Retrieve recipe by ID and user.
#-------------------------------------------------------------------------------
def get_recipe(recipe_id, user_id):
    db = get_db()

    sql = """
        SELECT
            r.id, user_id, created, title, author, description, source_url,
            image_path, servings, prep_time, cook_time, instructions
        FROM recipe r
        WHERE r.id = ? AND r.user_id = ?
        """
    args = (recipe_id, user_id)

    recipe = db.execute(sql, args).fetchone()
    if recipe is None:
        abort(404, f'Recipe id {recipe_id} not found.')

    return recipe

# Retrieve recipe's ingredient maps by ID.
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

    return db.execute(sql, args).fetchall()

# Retrieve recipe's ingredients by ID as a flattened list.
# TODO: Remove this hack by implementing proper ingredient parsing at ingest.
#-------------------------------------------------------------------------------
def get_recipe_ingredients_text(recipe_id):
    maps = get_recipe_ingredient_maps(recipe_id)
    recipe_ingredients_text = ''

    [recipe_ingredients_text := \
        recipe_ingredients_text + m['input_text'] + \
        ('\n' if i < len(maps) - 1 else '') \
        for i, m in enumerate(maps)]

    return recipe_ingredients_text

# Add new recipe.
#-------------------------------------------------------------------------------
def add_recipe(user_id, title, author, description, source_url, servings,
               prep_time, cook_time, instructions, image, parsed_ingredients):
    image_path = save_user_image(image)
    
    db = get_db()

    # Add recipe.
    sql = """
        INSERT INTO recipe (
            user_id, title, author, description, source_url,
            image_path, servings, prep_time, cook_time, instructions
            )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        RETURNING id
        """
    args = (user_id, title, author, description, source_url, image_path, servings,
        prep_time, cook_time, instructions)

    recipe = db.execute(sql, args).fetchone()
    db.commit()

    recipe_id = recipe['id']

    # Add ingredient maps.
    for ingredient in parsed_ingredients:
        sql = """
            INSERT INTO recipe_ingredient_map (
                recipe_id, input_text, count
                )
            VALUES (?, ?, ?)
            """
        args = (recipe_id, ingredient.name, ingredient.count)

        db.execute(sql, args)
        db.commit()

    return recipe_id

# Edit existing recipe.
#-------------------------------------------------------------------------------
def edit_recipe(recipe_id, user_id, title, author, description, source_url,
                servings, prep_time, cook_time, instructions, image,
                parsed_ingredients):
    recipe = get_recipe(recipe_id, user_id)

    delete_user_image(recipe['image_path'])
    image_path = save_user_image(image)

    db = get_db()

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

    db.execute(sql, args)
    db.commit()

    # Delete pre-existing ingredient maps.
    sql = """
        DELETE FROM recipe_ingredient_map
        WHERE recipe_id = ?
        """
    args = (recipe_id, )

    db.execute(sql, args)
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

        db.execute(sql, args)
        db.commit()

# Delete existing recipe.
#-------------------------------------------------------------------------------
def delete_recipe(recipe_id, user_id):
    recipe = get_recipe(recipe_id, user_id)

    delete_user_image(recipe['image_path'])

    db = get_db()

    # Delete recipe.
    sql = """
        DELETE FROM recipe 
        WHERE id = ? AND user_id = ?
        """
    args = (recipe_id, user_id)

    db.execute(sql, args)
    db.commit()

    # Delete ingredient maps.
    sql = """
        DELETE FROM recipe_ingredient_map
        WHERE recipe_id = ?
        """
    args = (recipe_id, )

    db.execute(sql, args)
    db.commit()

# Save user uploaded image.
#-------------------------------------------------------------------------------
def save_user_image(image):
    directory = os.path.join(current_app.static_folder, 'user_images')
    if not os.path.exists(directory):
        os.mkdir(directory)

    file_name = str(uuid.uuid4())

    image.save(os.path.join(directory, file_name))

    return os.path.join('user_images', file_name)

# Delete user uploaded image.
#-------------------------------------------------------------------------------
def delete_user_image(image_path):
    path = os.path.join(current_app.static_folder, image_path)

    if os.path.exists(path):
        os.remove(path)

