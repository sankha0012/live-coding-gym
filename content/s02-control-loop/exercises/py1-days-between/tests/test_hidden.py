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


def test_century_leap_rules():
    # 1900 and 2100 are not leap years, 2000 is.
    assert days_between("1900-02-28", "1900-03-01") == 1
    assert days_between("2100-02-28", "2100-03-01") == 1
    assert days_between("2000-02-28", "2000-03-01") == 2
    assert days_between("1999-12-31", "2001-01-01") == 367


def test_long_span_and_invalid_leap_day():
    assert days_between("1999-01-01", "2024-01-01") == 9131
    with pytest.raises(ValueError):
        days_between("2023-02-29", "2024-01-01")
    with pytest.raises(ValueError):
        days_between("1900-02-29", "2024-01-01")
