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


def test_spaces_inside_strings_survive():
    assert to_json({"a b": "x y"}) == '{"a b":"x y"}'
    assert from_json(to_json({"k k": "v v"})) == {"k k": "v v"}


def test_valid_falsy_json_is_not_none():
    assert from_json("0") == 0
    assert from_json("[]") == []
    assert from_json("false") is False
    assert from_json('""') == ""
    assert from_json("{}") == {}


def test_json_literals_parse():
    assert from_json("true") is True
    assert from_json('{"a": null}') == {"a": None}
