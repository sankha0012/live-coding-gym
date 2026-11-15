from solution import invert_dict


def test_repeated_values():
    assert invert_dict({"a": 1, "b": 2, "c": 1}) == {1: ["a", "c"], 2: ["b"]}


def test_keys_sorted():
    assert invert_dict({"z": 0, "m": 0, "a": 0}) == {0: ["a", "m", "z"]}


def test_all_unique():
    assert invert_dict({"x": "p", "y": "q"}) == {"p": ["x"], "q": ["y"]}


def test_empty():
    assert invert_dict({}) == {}


def test_every_group_sorted():
    d = {"z": 1, "y": 2, "b": 1, "x": 2, "a": 1}
    assert invert_dict(d) == {1: ["a", "b", "z"], 2: ["x", "y"]}
    assert list(invert_dict(d)[2]) == ["x", "y"]
