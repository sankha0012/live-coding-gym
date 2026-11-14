import pytest
from solution import parse_quantity


def test_number():
    assert parse_quantity("5") == 5


def test_spaces():
    assert parse_quantity("  7 ") == 7


def test_not_provided():
    assert parse_quantity(None) == 0
    assert parse_quantity("") == 0
    assert parse_quantity("   ") == 0


def test_zero_is_zero():
    assert parse_quantity("0") == 0


@pytest.mark.parametrize("bad", ["abc", "3.5", "1,000"])
def test_bad_text_raises(bad):
    with pytest.raises(ValueError):
        parse_quantity(bad)
