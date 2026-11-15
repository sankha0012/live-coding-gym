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


def test_4x4_clockwise():
    m = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    assert rotate(m) == [[13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3], [16, 12, 8, 4]]


def test_result_is_a_new_matrix():
    for m in ([[5]], [[1, 2], [3, 4]]):
        out = rotate(m)
        assert out is not m
        assert all(r is not q for r in out for q in m)
