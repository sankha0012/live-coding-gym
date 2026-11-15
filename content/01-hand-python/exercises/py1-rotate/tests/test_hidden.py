from solution import rotate


def test_basic():
    assert rotate([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]


def test_empty():
    assert rotate([], 3) == []


def test_k_larger_than_length():
    assert rotate([1, 2, 3], 4) == [3, 1, 2]
    assert rotate([1, 2, 3], 3) == [1, 2, 3]


def test_zero():
    assert rotate([1, 2, 3], 0) == [1, 2, 3]


def test_negative():
    assert rotate([1, 2, 3], -1) == [2, 3, 1]


def test_input_unchanged():
    data = [1, 2, 3]
    out = rotate(data, 1)
    assert data == [1, 2, 3]
    assert out is not data


def test_negative_wraps():
    assert rotate([1, 2, 3], -4) == [2, 3, 1]
    assert rotate([1, 2, 3, 4, 5], -7) == [3, 4, 5, 1, 2]


def test_always_returns_a_new_list():
    data = [1, 2, 3]
    for k in (0, 3, 6, 1, -3):
        out = rotate(data, k)
        assert out is not data
        out.append(99)
        assert data == [1, 2, 3]
