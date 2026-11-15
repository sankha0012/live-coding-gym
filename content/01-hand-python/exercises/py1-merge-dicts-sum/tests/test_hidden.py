from solution import merge_dicts_sum


def test_basic():
    assert merge_dicts_sum([{"a": 1, "b": 2}, {"b": 3, "c": 4}]) == {"a": 1, "b": 5, "c": 4}


def test_many_dicts():
    assert merge_dicts_sum([{"x": 1}, {"x": 2}, {"x": 3}]) == {"x": 6}


def test_input_not_changed():
    first = {"a": 1}
    merge_dicts_sum([first, {"a": 2}])
    assert first == {"a": 1}


def test_empty_list_and_empty_dicts():
    assert merge_dicts_sum([]) == {}
    assert merge_dicts_sum([{}, {}]) == {}


def test_zero_and_negative_totals_kept():
    assert merge_dicts_sum([{"a": 1}, {"a": -1}]) == {"a": 0}
    assert merge_dicts_sum([{"a": 1}, {"a": -3}]) == {"a": -2}
    assert merge_dicts_sum([{"a": -2}]) == {"a": -2}


def test_zero_values_keep_their_key():
    assert merge_dicts_sum([{"a": 0}, {"b": 1}]) == {"a": 0, "b": 1}


def test_floats():
    assert merge_dicts_sum([{"a": 0.5}, {"a": 0.25}]) == {"a": 0.75}
