from solution import mean_valid


def test_plain():
    assert mean_valid([1.0, 2.0, 3.0]) == 2.0


def test_ignores_nan_and_none():
    assert mean_valid([1.0, float("nan"), None, 3.0]) == 2.0


def test_zero_counts():
    assert mean_valid([0.0, 4.0]) == 2.0


def test_all_invalid():
    assert mean_valid([float("nan"), None]) is None


def test_empty():
    assert mean_valid([]) is None
