from cookbook.parsing.weight import WeightUnits

class Ingredient():
    def __init__(self, name, count, unit, modifier = None):
        self.name = name
        self.count = count
        self.unit = unit
        self.modifier = modifier

class IngredientParser():
    def Parse(self, ingredients_text):
        result = []
        lines = ingredients_text.split('\n')

        for line in lines:
            ingredient = self.ParseLine(line)
            result.append(ingredient)

        return result

    def ParseLine(self, ingredient_line):
        # TODO: Actually parse name, count and unit.
        return Ingredient(ingredient_line, 1, WeightUnits['grams'])
    
