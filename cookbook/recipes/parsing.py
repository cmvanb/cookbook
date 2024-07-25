#-------------------------------------------------------------------------------
# Recipes parsing logic
#-------------------------------------------------------------------------------


# TODO: Extract to model layer.
class WeightUnit():
    """ Weight unit data model. """

    def __init__(self, long_name, short_name, aliases, base_equivalent_grams):
        self.long_name = long_name
        self.short_name = short_name
        self.aliases = aliases
        self.base_equivalent_grams = base_equivalent_grams


# TODO: Extract to model layer.
class Ingredient():
    """ Ingredient data model. """

    def __init__(self, name, count, unit, modifier = None):
        self.name = name
        self.count = count
        self.unit = unit
        self.modifier = modifier


# NOTE: Values based on: https://www.unitconverters.net/
weightUnits = [
    WeightUnit('milligrams',  'mg',  [],  0.001),
    WeightUnit('grams',       'g',   [],  1),
    WeightUnit('kilograms',   'kg',  [],  1000),
    WeightUnit('ounces',      'oz',  [],  28.3495),
    WeightUnit('pounds',      'lb',  [],  453.592)
]

WeightUnits = dict(map(lambda unit: (unit.long_name, unit), weightUnits))


def parse_ingredients(ingredients_input):
    """ Parse ingredients to data models. """

    result = []
    lines = ingredients_input.split('\n')

    for line in lines:
        result.append(Ingredient(line, 1, WeightUnits['grams']))

    return result


def parse_ingredients_list(ingredient_maps):
    """ Parse ingredients to list. """

    return [m['input_text'].strip()
        for m in ingredient_maps]


def parse_instructions_list(instructions):
    """ Parse instructions to list. """

    return [i.strip()
        for i in instructions.split('\n')
        if len(i.strip()) > 0]
