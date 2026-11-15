import pytest

from solution import BankAccount


def test_deposit_and_withdraw():
    a = BankAccount()
    assert a.balance == 0
    a.deposit(100)
    a.withdraw(30)
    assert a.balance == 70


def test_withdraw_whole_balance():
    a = BankAccount()
    a.deposit(50)
    a.withdraw(50)
    assert a.balance == 0


def test_overdraft_raises_and_keeps_balance():
    a = BankAccount()
    a.deposit(10)
    with pytest.raises(ValueError):
        a.withdraw(11)
    assert a.balance == 10


def test_non_positive_amounts():
    a = BankAccount()
    a.deposit(10)
    for bad in (0, -5):
        with pytest.raises(ValueError):
            a.deposit(bad)
        with pytest.raises(ValueError):
            a.withdraw(bad)
    assert a.balance == 10


def test_balance_read_only():
    a = BankAccount()
    with pytest.raises(AttributeError):
        a.balance = 5
