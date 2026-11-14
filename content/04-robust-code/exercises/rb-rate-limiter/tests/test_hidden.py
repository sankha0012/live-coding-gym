import pytest

from solution import TokenBucket


class Clock:
    def __init__(self, t=0.0):
        self.t = t

    def __call__(self):
        return self.t


def test_burst_then_deny():
    c = Clock()
    b = TokenBucket(3, 1, c)
    assert [b.allow() for _ in range(4)] == [True, True, True, False]


def test_refill_over_time():
    c = Clock()
    b = TokenBucket(3, 1, c)
    for _ in range(3):
        b.allow()
    c.t = 1
    assert b.allow() is True
    assert b.allow() is False
    c.t = 1.5
    assert b.allow() is False
    c.t = 2
    assert b.allow() is True


def test_refill_is_capped():
    c = Clock()
    b = TokenBucket(3, 1, c)
    c.t = 1000
    assert [b.allow() for _ in range(4)] == [True, True, True, False]


def test_denied_call_consumes_nothing():
    c = Clock()
    b = TokenBucket(2, 1, c)
    assert b.allow(2) is True
    c.t = 1
    assert b.allow(2) is False
    c.t = 2
    assert b.allow(2) is True


def test_cost_above_capacity_never_allowed():
    b = TokenBucket(2, 1, Clock())
    assert b.allow(3) is False
    assert b.allow(2) is True


def test_clock_going_backwards():
    c = Clock(10)
    b = TokenBucket(2, 1, c)
    assert b.allow(2) is True
    c.t = 5
    assert b.allow() is False
    c.t = 6
    assert b.allow() is True
    assert b.allow() is False


def test_bad_arguments():
    for cap, rate in [(0, 1), (-1, 1), (1, 0), (1, -2)]:
        with pytest.raises(ValueError):
            TokenBucket(cap, rate, Clock())


def test_fractional_rate():
    c = Clock()
    b = TokenBucket(1, 0.5, c)
    assert b.allow() is True
    c.t = 1
    assert b.allow() is False
    c.t = 2
    assert b.allow() is True


def test_cost_needs_only_that_many_tokens():
    c = Clock()
    b = TokenBucket(2, 1, c)
    assert b.allow(2) is True
    c.t = 0.5
    assert b.allow(0.5) is True
    assert b.allow(0.01) is False
