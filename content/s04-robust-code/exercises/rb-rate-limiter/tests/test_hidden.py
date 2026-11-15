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


def test_refill_measured_from_construction_time():
    c = Clock(100.0)
    b = TokenBucket(3, 1, c)
    assert [b.allow() for _ in range(3)] == [True, True, True]
    c.t = 100.4
    assert b.allow() is False
    c.t = 101.0
    assert b.allow() is True
    assert b.allow() is False


def test_zero_cost_always_allowed_and_free():
    c = Clock()
    b = TokenBucket(2, 1, c)
    assert b.allow(2) is True
    assert b.allow(0) is True
    assert b.allow() is False
    c.t = 1
    assert b.allow() is True


def test_two_buckets_are_independent():
    c1, c2 = Clock(), Clock()
    a = TokenBucket(1, 1, c1)
    b = TokenBucket(1, 1, c2)
    assert a.allow() is True
    assert b.allow() is True
    assert a.allow() is False and b.allow() is False
    c1.t = 1
    assert a.allow() is True
    assert b.allow() is False


def test_partial_refills_accumulate_across_denied_calls():
    c = Clock()
    b = TokenBucket(5, 2, c)
    assert b.allow(5) is True
    for t in (0.25, 0.5, 0.75):
        c.t = t
        assert b.allow(2) is False
    c.t = 1.0
    assert b.allow(2) is True
    assert b.allow(0.5) is False
