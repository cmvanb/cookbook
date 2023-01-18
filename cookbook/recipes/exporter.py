#-------------------------------------------------------------------------------
# Export recipe
#-------------------------------------------------------------------------------

import io
import yaml
import math

from cookbook.recipes import utils

# Convert recipe model to YAML format.
#-------------------------------------------------------------------------------
def recipe_to_yaml(recipe, ingredients_list, instructions_list):
    object = {}
    object['title'] = recipe['title']
    object['author'] = recipe['author']
    object['description'] = recipe['description']
    object['source_url'] = recipe['source_url']
    object['servings'] = recipe['servings']
    object['prep_time'] = recipe['prep_time']
    object['cook_time'] = recipe['cook_time']
    object['ingredients'] = ingredients_list
    object['instructions'] = instructions_list

    data = yaml.dump(object, width=math.inf, allow_unicode=True, sort_keys=False).encode()

    file = io.BytesIO()
    file.write(data)
    file.seek(0)

    return file

# Format recipe file name.
#-------------------------------------------------------------------------------
def recipe_file_name(title):
    title = utils.kebabcase(title)
    return f'{title}.yaml'

