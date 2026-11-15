from solution import fill_features


def test_empty_string_filled_when_flag_on():
    got = fill_features({"city": "", "items": 0}, {"city": "unknown", "items": 1}, empty_is_missing=True)
    assert got == ({"city": "unknown", "items": 0}, ["city"])


def test_zero_false_still_real_when_flag_on():
    row = {"a": 0, "b": 0.0, "c": False}
    got = fill_features(row, {"a": 1, "b": 1, "c": True}, empty_is_missing=True)
    assert got == (row, [])


def test_none_and_absent_still_filled_when_flag_on():
    got, names = fill_features({"a": None, "b": ""}, {"a": 1, "b": 2, "c": 3}, empty_is_missing=True)
    assert got == {"a": 1, "b": 2, "c": 3}
    assert names == ["a", "b", "c"]


def test_empty_string_in_non_default_key_kept():
    got, names = fill_features({"note": "", "a": 5}, {"a": 1}, empty_is_missing=True)
    assert got == {"note": "", "a": 5} and names == []


def test_flag_off_keeps_empty_string():
    got, names = fill_features({"city": ""}, {"city": "unknown"})
    assert got == {"city": ""} and names == []


def test_no_mutation_with_flag():
    row, d = {"city": ""}, {"city": "x"}
    fill_features(row, d, empty_is_missing=True)
    assert row == {"city": ""} and d == {"city": "x"}
