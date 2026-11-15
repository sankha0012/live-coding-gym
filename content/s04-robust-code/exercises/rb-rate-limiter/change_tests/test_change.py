import pytest

from solution import TokenBucket


class Clock:
    def __init__(self, t=0.0):
        self.t = t

    def __call__(self):
        return self.t


def test_negative_cost_raises():
    b = TokenBucket(3, 1, Clock())
    for cost in (-1, -0.5, -100):
        with pytest.raises(ValueError):
            b.allow(cost)


def test_negative_cost_does_not_change_the_bucket():
    c = Clock()
    b = TokenBucket(2, 1, c)
    assert b.allow(2) is True
    with pytest.raises(ValueError):
        b.allow(-5)
    assert b.allow() is False
    c.t = 1
    assert b.allow() is True
    assert b.allow() is False


def test_negative_cost_cannot_overfill():
    b = TokenBucket(2, 1, Clock())
    with pytest.raises(ValueError):
        b.allow(-10)
    assert [b.allow() for _ in range(3)] == [True, True, False]


def test_zero_cost_still_fine():
    b = TokenBucket(1, 1, Clock())
    assert b.allow(0) is True
    assert b.allow() is True
    assert b.allow() is False
