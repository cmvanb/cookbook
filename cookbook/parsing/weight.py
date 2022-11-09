class WeightUnit():
    def __init__(self, long_name, short_name, aliases, base_equivalent_grams):
        self.long_name = long_name
        self.short_name = short_name
        self.aliases = aliases
        self.base_equivalent_grams = base_equivalent_grams

# NOTE: Based on: https://www.unitconverters.net/

weightUnits = [
    WeightUnit('milligrams',  'mg',  [],  0.001),
    WeightUnit('grams',       'g',   [],  1),
    WeightUnit('kilograms',   'kg',  [],  1000),
    WeightUnit('ounces',      'oz',  [],  28.3495),
    WeightUnit('pounds',      'lb',  [],  453.592)
]

WeightUnits = dict(map(lambda unit: (unit.long_name, unit), weightUnits))

