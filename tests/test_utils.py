import pytest
from source import utils
import logging
logging.basicConfig(level=logging.INFO)


@pytest.mark.parametrize("input, output", 
                            [
                                ("400 g spaghetti",('400 g', 234, 'spaghetti', 'Pasta', 1.73))
                             ])
def test_parse_recipe_item(input, output):
    assert utils.parse_recipe_item(input) == output

#Reflection: Maybe the most future-proof approach is to test on the correct returning of the id, as naming and footprints might change in newer versions of "Den store klimadatabase"?
#Recipe: https://www.valdemarsro.dk/pasta-med-friske-tomater/
@pytest.mark.parametrize("input, id, product, footprint", 
                            [
                                ("spaghetti", 234,"Pasta", 1.73),
                                ("hvidløg, finthakkede", 136, "Hvidløg", 1.13),
                                ("håndfulde frisk basilikum, grofthakket", 486, "Basilikum, frisk", 0.33),
                                ("tomat, grofthakkede", 2, "Tomat", 0.46),
                                ("parmesan, eller anden hård ost", 79, "Parmesan ost, 32+", 6.63),
                                ("salt", 151, "Salt, bordsalt (jodberiget)", 0.44),
                                ("sort peber, friskkværnet", 302, "Peber, sort", 4.69),
                             ])
def test_get_best_database_match1(input, id, product, footprint):
    result = utils.get_best_database_match(input)
    assert result.id == id
    assert result.product == product
    assert result.footprint == pytest.approx(footprint)

#Recipe: https://vegetariskhverdag.dk/2019/01/spaghetti-alla-puttanesca/
@pytest.mark.parametrize("input, id", 
                            [
                                ("Olivenolie", 349),
                                ("løg", 266),
                                ("hvidløg", 136),
                                #("chiliflakes",), Should throw error, not found
                                ("hvidvin (valgfrit)", 375),
                                #("dåser hakket tomat",), Should throw error, not found
                                ("glas små kapers (ca. 65g)", 437),
                                ("glas kalamata oliven (ca. 200g)", 139) #Should map to "Oliven, sorte, uden sten, i saltlage
                                #("Revet skal fra en halv citron",), #How to handle this?
                                #("æblecidereddike",), Should throw error, not found
                                #("Salt og peber", ) Should be handled in a way where carbon footprint from both salt and pepper is fetched
                                #("Server med: parmesan og frisk persille (for vegansk kan parmesan erstattes af gærflager)", ) Similar approach to the above

                             ])
def test_get_best_database_match2(input, id):
    result = utils.get_best_database_match(input)
    #print(f"\nProduct name: {result.product}\n")
    assert result.id == id