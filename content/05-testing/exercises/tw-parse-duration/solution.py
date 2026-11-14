import pytest

from solution import parse_duration


def test_single_units():
    assert parse_duration("45s") == 45
    assert parse_duration("2h") == 7200
    assert parse_duration("10m") == 600


def test_combined_units():
    assert parse_duration("1h30m") == 5400
    assert parse_duration("1h5s") == 3605
    assert parse_duration("1h2m3s") == 3723
    assert parse_duration("90m") == 5400
    assert parse_duration("75s") == 75


def test_returns_int():
    assert isinstance(parse_duration("1m"), int)


def test_empty_string_raises():
    with pytest.raises(ValueError):
        parse_duration("")


@pytest.mark.parametrize("bad", ["abc", "90", "1h30", "5x", "1h30mxyz", "30m1h", "1h1h"])
def test_invalid_text_raises(bad):
    with pytest.raises(ValueError):
        parse_duration(bad)
