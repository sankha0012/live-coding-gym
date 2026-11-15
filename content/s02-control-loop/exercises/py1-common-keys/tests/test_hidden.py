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


def test_every_dict_must_have_the_key():
    assert common_keys([{"a": 1, "b": 1}, {"a": 2, "b": 2}, {"a": 3}]) == ["a"]
    assert common_keys([{"a": 1, "b": 1}, {"a": 2, "b": 2}, {"a": 3}, {"b": 4}]) == []


def test_many_keys_sorted():
    names = ["k%02d" % i for i in range(12)]
    d1 = {k: 1 for k in reversed(names)}
    d2 = {k: 2 for k in names}
    assert common_keys([d1, d2]) == names


def test_inputs_not_modified():
    d1, d2 = {"a": 1, "b": 2}, {"b": 3}
    assert common_keys([d1, d2]) == ["b"]
    assert d1 == {"a": 1, "b": 2} and d2 == {"b": 3}
