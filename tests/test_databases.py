import pytest
from source import databases


@pytest.mark.parametrize("id, product, footprint", 
                            [
                                (2,"Tomat", 0.46)
                             ])
def test_get_dsk_item_by_id(id, product, footprint):
    assert databases.get_dsk_item_by_id(id).product == product
    assert databases.get_dsk_item_by_id(id).footprint == pytest.approx(footprint)

