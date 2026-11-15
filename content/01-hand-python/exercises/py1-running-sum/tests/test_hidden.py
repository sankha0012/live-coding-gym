from solution import running_sum


def test_basic():
    assert running_sum([1, 2, 3, 4]) == [1, 3, 6, 10]


def test_empty():
    assert running_sum([]) == []


def test_negative():
    assert running_sum([5, -2, -3, 4]) == [5, 3, 0, 4]


def test_single():
    assert running_sum([7]) == [7]


def test_input_unchanged():
    data = [1, 2, 3]
    running_sum(data)
    assert data == [1, 2, 3]


def test_floats():
    assert running_sum([0.5, 0.25, -0.75]) == [0.5, 0.75, 0.0]


def test_zeros_keep_their_position():
    assert running_sum([0, 1, 0, 2, 0]) == [0, 1, 1, 3, 3]
    assert running_sum([0]) == [0]
