from solution import dedupe


def test_removes_duplicates():
    assert dedupe([1, 1, 1]) == [1]


def test_keeps_first_occurrence_in_order():
    assert dedupe([3, 1, 2, 3, 1]) == [3, 1, 2]


def test_strings():
    assert dedupe(["b", "a", "b", "c", "a"]) == ["b", "a", "c"]


def test_empty_and_no_duplicates():
    assert dedupe([]) == []
    assert dedupe([2, 1, 3]) == [2, 1, 3]


def test_result_is_new_list_even_without_duplicates():
    data = [2, 1, 3]
    assert dedupe(data) is not data


def test_input_not_mutated():
    data = [1, 2, 1, 3, 2]
    result = dedupe(data)
    assert data == [1, 2, 1, 3, 2]
    assert result is not data
