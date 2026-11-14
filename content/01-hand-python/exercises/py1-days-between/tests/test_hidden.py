import pytest

from solution import days_between


def test_forward():
    assert days_between("2024-01-01", "2024-01-31") == 30


def test_backward_is_positive():
    assert days_between("2024-01-31", "2024-01-01") == 30


def test_same_day_and_leap_year():
    assert days_between("2024-05-05", "2024-05-05") == 0
    assert days_between("2024-02-28", "2024-03-01") == 2
    assert days_between("2023-02-28", "2023-03-01") == 1
    assert days_between("2023-12-31", "2024-12-31") == 366


@pytest.mark.parametrize("bad", ["not-a-date", "2024-13-01", "2024-02-30", ""])
def test_bad_input_raises(bad):
    with pytest.raises(ValueError):
        days_between(bad, "2024-01-01")
    with pytest.raises(ValueError):
        days_between("2024-01-01", bad)
