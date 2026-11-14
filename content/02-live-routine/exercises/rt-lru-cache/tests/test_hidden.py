from solution import LRUCache


def test_missing():
    c = LRUCache(2)
    assert c.get(1) == -1


def test_example():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)
    assert c.get(2) == -1
    assert c.get(1) == 1
    assert c.get(3) == 3


def test_update_existing_no_evict():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(1, 10)
    assert c.get(1) == 10
    assert c.get(2) == 2


def test_put_refreshes():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(1, 5)
    c.put(3, 3)
    assert c.get(2) == -1
    assert c.get(1) == 5


def test_capacity_one():
    c = LRUCache(1)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == -1
    assert c.get(2) == 2


def test_falsy_values():
    c = LRUCache(2)
    c.put(1, 0)
    c.put(2, None)
    assert c.get(1) == 0
    assert c.get(2) is None


def test_update_newest_keeps_oldest():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(2, 20)
    assert c.get(1) == 1
    assert c.get(2) == 20
