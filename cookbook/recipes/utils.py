#-------------------------------------------------------------------------------
# Recipes Utilities
#-------------------------------------------------------------------------------

ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg' }

# Utility function to determine whether an image filetype is acceptable.
#-------------------------------------------------------------------------------
def image_format_allowed(file):
    return file.mimetype[0:5] == 'image' \
        and '.' in file.filename \
        and file.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

