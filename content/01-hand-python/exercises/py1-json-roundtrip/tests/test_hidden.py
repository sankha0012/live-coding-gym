from solution import from_json, to_json


def test_sorted_compact():
    assert to_json({"b": 1, "a": [1, 2]}) == '{"a":[1,2],"b":1}'


def test_nested_keys_sorted():
    assert to_json({"b": {"d": 1, "c": 2}, "a": 0}) == '{"a":0,"b":{"c":2,"d":1}}'


def test_empty_dict():
    assert to_json({}) == "{}"


def test_roundtrip():
    d = {"z": {"y": 1, "x": None}, "a": "hi", "n": 2.5}
    assert from_json(to_json(d)) == d


def test_invalid_returns_none():
    assert from_json("{bad") is None
    assert from_json("") is None
