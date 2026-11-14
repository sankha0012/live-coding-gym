from solution import rotate


def test_2x2():
    assert rotate([[1, 2], [3, 4]]) == [[3, 1], [4, 2]]


def test_3x3():
    assert rotate([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [[7, 4, 1], [8, 5, 2], [9, 6, 3]]


def test_1x1_and_empty():
    assert rotate([[5]]) == [[5]]
    assert rotate([]) == []


def test_input_not_changed():
    m = [[1, 2], [3, 4]]
    rotate(m)
    assert m == [[1, 2], [3, 4]]


def test_returns_lists():
    assert all(isinstance(r, list) for r in rotate([[1, 2], [3, 4]]))
