import copy

from solution import tag_rows


def test_all_rows_are_tagged():
    rows = [{"value": 3}, {"value": -1}, {"value": 0}]
    assert tag_rows(rows) == ["ok", "negative", "ok"]


def test_none_is_missing_and_does_not_crash():
    assert tag_rows([{"value": None}, {"value": -2}]) == ["missing", "negative"]


def test_empty_input():
    assert tag_rows([]) == []


def test_calls_are_independent():
    tag_rows([{"value": 1}, {"value": 2}])
    assert tag_rows([{"value": -5}]) == ["negative"]


def test_input_not_modified():
    rows = [{"value": None}, {"value": 7}]
    before = copy.deepcopy(rows)
    tag_rows(rows)
    assert rows == before


def test_returns_a_new_list_each_time():
    a = tag_rows([{"value": 1}])
    b = tag_rows([{"value": 1}])
    assert a == b == ["ok"]
    assert a is not b
