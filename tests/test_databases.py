import pytest
from source import databases


@pytest.mark.parametrize("input, output", 
                            [
                                (2,"Tomat")
                             ])
def test_parse_recipe_item(input, output):
    assert databases.get_dsk_item_by_id(input).product == output

