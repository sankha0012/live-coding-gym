from solution import BoundedQueue


def test_put_many_reject():
    q = BoundedQueue(2, "reject")
    assert q.put_many([1, 2, 3]) == 2
    assert len(q) == 2
    assert q.dropped == 1
    assert [q.get(), q.get()] == [1, 2]


def test_put_many_drop_oldest():
    q = BoundedQueue(2)
    assert q.put_many([1, 2, 3]) == 3
    assert q.dropped == 1
    assert [q.get(), q.get()] == [2, 3]


def test_put_many_empty_and_partial_space():
    q = BoundedQueue(3, "reject")
    assert q.put_many([]) == 0
    q.put("a")
    assert q.put_many(iter(["b", "c", "d", "e"])) == 2
    assert q.dropped == 2
    assert [q.get(), q.get(), q.get()] == ["a", "b", "c"]


def test_put_many_falsy_items_count():
    q = BoundedQueue(5)
    assert q.put_many([0, "", None, False]) == 4
    assert len(q) == 4
