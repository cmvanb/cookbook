#-------------------------------------------------------------------------------
# Recipes validation layer
#-------------------------------------------------------------------------------

from . import utils

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
    elif not utils.image_format_allowed(image):
        return 'Image format not allowed.'

    return None

