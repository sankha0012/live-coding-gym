import pytest
from solution import TTLCache


class Clock:
    def __init__(self):
        self.t = 100.0

    def __call__(self):
        return self.t


def make(ttl=10, size=3):
    c = Clock()
    return TTLCache(ttl, size, c), c


def test_set_get_and_default():
    cache, _ = make()
    cache.set("a", 1)
    assert cache.get("a") == 1
    assert cache.get("zzz") is None
    assert cache.get("zzz", "d") == "d"


def test_expires_at_exactly_ttl():
    cache, clock = make(ttl=10)
    cache.set("a", 1)
    clock.t += 9.99
    assert cache.get("a") == 1
    clock.t += 0.01
    assert cache.get("a") is None
    assert len(cache) == 0


def test_set_again_restarts_ttl():
    cache, clock = make(ttl=10)
    cache.set("a", 1)
    clock.t += 8
    cache.set("a", 2)
    clock.t += 8
    assert cache.get("a") == 2


def test_evicts_oldest_when_full():
    cache, clock = make(size=2)
    cache.set("a", 1)
    clock.t += 1
    cache.set("b", 2)
    clock.t += 1
    cache.set("c", 3)
    assert cache.get("a") is None
    assert cache.get("b") == 2 and cache.get("c") == 3
    assert len(cache) == 2


def test_replacing_key_does_not_evict_and_refreshes_age():
    cache, clock = make(size=2)
    cache.set("a", 1)
    clock.t += 1
    cache.set("b", 2)
    clock.t += 1
    cache.set("a", 10)
    assert cache.get("b") == 2 and cache.get("a") == 10
    clock.t += 1
    cache.set("c", 3)
    assert cache.get("b") is None
    assert cache.get("a") == 10


def test_replacing_newer_key_keeps_older_key():
    cache, clock = make(size=2)
    cache.set("a", 1)
    clock.t += 1
    cache.set("b", 2)
    clock.t += 1
    cache.set("b", 3)
    assert cache.get("a") == 1 and cache.get("b") == 3


def test_expired_entries_are_dropped_before_evicting_live_ones():
    cache, clock = make(ttl=5, size=2)
    cache.set("old", 1)
    clock.t += 3
    cache.set("fresh", 2)
    clock.t += 3
    cache.set("new", 3)
    assert cache.get("fresh") == 2 and cache.get("new") == 3
    assert len(cache) == 2


def test_none_value_is_a_hit_and_bad_size():
    cache, _ = make()
    cache.set("k", None)
    assert cache.get("k", "default") is None
    assert len(cache) == 1
    with pytest.raises(ValueError):
        TTLCache(5, 0, Clock())


def test_get_does_not_refresh_age():
    cache, clock = make(size=2)
    cache.set("a", 1)
    clock.t += 1
    cache.set("b", 2)
    clock.t += 1
    assert cache.get("a") == 1
    cache.set("c", 3)
    assert cache.get("a") is None and cache.get("b") == 2
