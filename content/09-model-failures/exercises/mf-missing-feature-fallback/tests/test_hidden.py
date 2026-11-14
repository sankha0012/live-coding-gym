from solution import fill_features

D = {"distance_km": 3.0, "items": 1, "is_rain": False}


def test_nothing_missing():
    row = {"distance_km": 5.0, "items": 2, "is_rain": True}
    assert fill_features(row, D) == (row, [])


def test_absent_and_none():
    got, names = fill_features({"items": None}, D)
    assert got == {"distance_km": 3.0, "items": 1, "is_rain": False}
    assert names == ["distance_km", "is_rain", "items"]


def test_zero_and_false_are_real():
    got, names = fill_features({"distance_km": 0.0, "items": 0, "is_rain": False}, D)
    assert got == {"distance_km": 0.0, "items": 0, "is_rain": False}
    assert names == []


def test_extra_keys_kept():
    got, names = fill_features({"promo": "x", "items": 4}, D)
    assert got["promo"] == "x" and got["items"] == 4
    assert names == ["distance_km", "is_rain"]


def test_empty_row_and_no_mutation():
    row = {}
    got, names = fill_features(row, D)
    assert got == D and names == ["distance_km", "is_rain", "items"]
    assert row == {}
