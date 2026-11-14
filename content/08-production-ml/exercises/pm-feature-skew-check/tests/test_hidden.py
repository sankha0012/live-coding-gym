from solution import find_skew

NAN = float("nan")


def test_identical_is_clean():
    assert find_skew({"a": 1.0, "b": "x"}, {"a": 1.0, "b": "x"}) == {}


def test_empty_inputs():
    assert find_skew({}, {}) == {}


def test_numeric_tolerance_boundary():
    online = {"price": 10.0, "dist": 2.0}
    offline = {"price": 10.5, "dist": 2.75}
    out = find_skew(online, offline, tolerance=0.5)
    assert out == {"dist": "diff"}


def test_missing_features_on_either_side():
    out = find_skew({"a": 1, "extra": 2}, {"a": 1, "lost": 3})
    assert out == {"extra": "missing_offline", "lost": "missing_online"}


def test_null_handling():
    out = find_skew({"a": None, "b": NAN, "c": NAN, "d": 1.0}, {"a": NAN, "b": NAN, "c": 2.0, "d": None})
    assert out == {"c": "diff", "d": "diff"}


def test_non_numeric_and_bool():
    out = find_skew({"city": "SP", "flag": True, "n": 1}, {"city": "RJ", "flag": False, "n": 1})
    assert out == {"city": "diff", "flag": "diff"}


def test_sorted_output_and_int_float_mix():
    out = find_skew({"z": 1, "a": 5}, {"z": 2.0, "a": 6})
    assert list(out) == ["a", "z"]
    assert find_skew({"x": 3}, {"x": 3.0}) == {}


def test_zero_and_empty_string_are_not_null_and_default_tolerance():
    assert find_skew({"a": 0, "b": ""}, {"a": 0.0, "b": ""}) == {}
    assert find_skew({"a": 0, "b": ""}, {"a": None, "b": None}) == {"a": "diff", "b": "diff"}
    assert find_skew({"a": 1.0}, {"a": 1.001}) == {"a": "diff"}
    assert find_skew({"a": 1.0}, {"a": 1.0000001}) == {}
