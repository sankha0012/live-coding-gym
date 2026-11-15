import pytest

from solution import withdraw


def test_normal_withdrawal():
    assert withdraw(100, 30) == 70


def test_withdraw_whole_balance():
    assert withdraw(50, 50) == 0


def test_zero_amount_raises():
    with pytest.raises(ValueError):
        withdraw(100, 0)


def test_negative_amount_raises():
    with pytest.raises(ValueError):
        withdraw(100, -5)


def test_overdraft_raises():
    with pytest.raises(RuntimeError):
        withdraw(10, 11)
