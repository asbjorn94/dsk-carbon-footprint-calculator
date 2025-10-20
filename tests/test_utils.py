import pytest
from source import utils

@pytest.mark.parametrize("input, output", 
                            [
                                ("400 g spaghetti",('400 g', 234, 'spaghetti', 'Pasta', 1.73))
                             ])
def test_parse_recipe_item(input, output):
    assert utils.parse_recipe_item(input) == output

#Reflection: Maybe the most future-proof approach is to test on the correct returning of the id, as naming and footprints might change in newer versions of "Den store klimadatabase"?
@pytest.mark.parametrize("input, id, product, footprint", 
                            [
                                ("spaghetti", 234,"Pasta", 1.73),
                                ("hvidløg, finthakkede", 136, "Hvidløg", 1.13),
                                ("håndfulde frisk basilikum, grofthakket", 486, "Basilikum, frisk", 0.33),
                                ("tomater, grofthakkede", 2, "Tomat", 0.46),
                                ("parmesan, eller anden hård ost", 79, "Parmesan ost, 32+", 6.63),
                                ("salt", 151, "Salt, bordsalt (jodberiget)", 0.44),
                                ("sort peber, friskkværnet", 302, "Peber, sort", 4.69),
                             ])
def test_get_best_database_match(input, id, product, footprint):
    result = utils.get_best_database_match(input)
    assert result.id == id
    assert result.product == product
    assert result.footprint == pytest.approx(footprint)