import pytest
from solution import BoundedQueue


def test_fifo_order():
    q = BoundedQueue(3)
    for x in (1, 2, 3):
        assert q.put(x) is True
    assert [q.get(), q.get(), q.get()] == [1, 2, 3]
    assert q.dropped == 0


def test_drop_oldest():
    q = BoundedQueue(2, "drop_oldest")
    q.put("a")
    q.put("b")
    assert q.put("c") is True
    assert len(q) == 2
    assert q.dropped == 1
    assert [q.get(), q.get()] == ["b", "c"]


def test_reject():
    q = BoundedQueue(2, "reject")
    q.put("a")
    q.put("b")
    assert q.put("c") is False
    assert len(q) == 2
    assert q.dropped == 1
    assert [q.get(), q.get()] == ["a", "b"]


def test_never_above_capacity_and_counts():
    for policy in ("drop_oldest", "reject"):
        q = BoundedQueue(5, policy)
        for i in range(100):
            q.put(i)
            assert len(q) <= 5
        assert q.dropped == 95


def test_space_frees_after_get():
    q = BoundedQueue(1, "reject")
    q.put(1)
    assert q.put(2) is False
    q.get()
    assert q.put(3) is True
    assert q.get() == 3


def test_empty_get_raises():
    with pytest.raises(IndexError):
        BoundedQueue(2).get()


def test_none_is_a_valid_item():
    q = BoundedQueue(2)
    q.put(None)
    assert len(q) == 1
    assert q.get() is None


@pytest.mark.parametrize("args", [(0,), (-1,), (2, "newest")])
def test_bad_args(args):
    with pytest.raises(ValueError):
        BoundedQueue(*args)


def test_default_policy_is_drop_oldest():
    q = BoundedQueue(1)
    assert q.put(1) is True
    assert q.put(2) is True
    assert q.dropped == 1
    assert q.get() == 2


def test_falsy_items_are_ordinary_items():
    q = BoundedQueue(3)
    for x in (0, "", False):
        assert q.put(x) is True
    assert len(q) == 3
    assert [q.get(), q.get(), q.get()] == [0, "", False]


def test_get_on_empty_after_draining():
    q = BoundedQueue(2)
    q.put(1)
    q.get()
    with pytest.raises(IndexError):
        q.get()


def test_drop_oldest_keeps_fifo_across_many_drops():
    q = BoundedQueue(3)
    for i in range(10):
        q.put(i)
    assert q.dropped == 7
    assert [q.get(), q.get(), q.get()] == [7, 8, 9]
