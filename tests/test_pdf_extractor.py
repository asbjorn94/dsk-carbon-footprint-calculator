import pytest
from helper_scripts.pdf_extractor import map_to_dsk_item

@pytest.mark.parametrize("input, output", [
    ("Agurk, rå","Agurk"),
    ("Tomat, rå","Tomat"),
    ("Pølsebrød - almindeligt/hotdog","Pølsebrød"),
    ("Pølsebrød - fransk hotdog","Pølsebrød"),
    ("Kakao","Kakao, pulver")
])
def test_map_to_dsk_item(input, output):
    assert map_to_dsk_item(input).product == output


@pytest.mark.parametrize("input, output", [
    ("Kardemomme",None),
    ("Sesamolie",None),
])
def test_map_to_dsk_item_none_results(input, output):
    assert map_to_dsk_item(input) == output