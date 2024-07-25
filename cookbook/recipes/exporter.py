#-------------------------------------------------------------------------------
# Export recipe
#-------------------------------------------------------------------------------

import io
import yaml
import math

from cookbook.recipes import utils


def recipe_to_yaml(recipe, ingredients_list, instructions_list):
    """ Convert recipe model to YAML format. """

    output = {}
    output['title'] = recipe['title']
    output['author'] = recipe['author']
    output['description'] = recipe['description']
    output['source_url'] = recipe['source_url']
    output['servings'] = recipe['servings']
    output['prep_time'] = recipe['prep_time']
    output['cook_time'] = recipe['cook_time']
    output['ingredients'] = ingredients_list
    output['instructions'] = instructions_list

    data = yaml.dump(output, width=math.inf, allow_unicode=True, sort_keys=False).encode()

    file = io.BytesIO()
    file.write(data)
    file.seek(0)

    return file


def recipe_file_name(title):
    """ Format recipe file name. """

    title = utils.kebabcase(title)
    return f'{title}.yaml'
