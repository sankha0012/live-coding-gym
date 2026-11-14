from solution import flatten


def test_basic():
    assert flatten([[1, 2], [3], []]) == [1, 2, 3]


def test_empty():
    assert flatten([]) == []
    assert flatten([[], []]) == []


def test_one_level_only():
    assert flatten([[1, [2]], [3]]) == [1, [2], 3]


def test_does_not_change_input():
    data = [[1], [2]]
    flatten(data)
    assert data == [[1], [2]]
