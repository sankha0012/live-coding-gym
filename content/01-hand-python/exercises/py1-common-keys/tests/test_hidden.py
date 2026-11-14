from solution import common_keys


def test_basic():
    assert common_keys([{"a": 1, "b": 2}, {"b": 3, "c": 4}]) == ["b"]


def test_three_dicts_sorted():
    assert common_keys([{"z": 1, "a": 1, "m": 1}, {"m": 2, "a": 2}, {"a": 3, "m": 3, "q": 3}]) == ["a", "m"]


def test_no_overlap():
    assert common_keys([{"a": 1}, {"b": 2}]) == []


def test_single_dict():
    assert common_keys([{"b": 1, "a": 2}]) == ["a", "b"]


def test_empty_list():
    assert common_keys([]) == []
