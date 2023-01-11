#-------------------------------------------------------------------------------
# Recipes validation layer
#-------------------------------------------------------------------------------

# Determine whether an image is acceptable to the server.
# NOTE: Perhaps worthwhile to check some more substantial image attiributes than
#   the user-provided file extension.
#-------------------------------------------------------------------------------
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg' }

def image_allowed(file):
    return file.mimetype[0:5] == 'image' \
        and '.' in file.filename \
        and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Validate user input recipe data.
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

    # TODO: Perform further validation on:
    # Source URL
    # Servings
    # Prep Time
    # Cook Time
    # Tags
    # Ingredients

    if not image_allowed(image):
        return 'Image not allowed.'

    return None

