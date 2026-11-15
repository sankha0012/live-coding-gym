from solution import TTLCache


class Clock:
    def __init__(self):
        self.t = 100.0

    def __call__(self):
        return self.t


def make(ttl=10, size=5):
    c = Clock()
    return TTLCache(ttl, size, c), c


def test_per_key_ttl_shorter_than_default():
    cache, clock = make(ttl=10)
    cache.set("a", 1, 2)
    cache.set("b", 2)
    clock.t += 1.99
    assert cache.get("a") == 1
    clock.t += 0.01
    assert cache.get("a") is None
    assert cache.get("b") == 2


def test_per_key_ttl_longer_than_default():
    cache, clock = make(ttl=5)
    cache.set("a", 1, 20)
    cache.set("b", 2)
    clock.t += 6
    assert cache.get("a") == 1
    assert cache.get("b") is None
    clock.t += 14
    assert cache.get("a") is None


def test_none_means_default_and_len_counts_live():
    cache, clock = make(ttl=10)
    cache.set("a", 1, None)
    cache.set("b", 2, 3)
    assert len(cache) == 2
    clock.t += 3
    assert len(cache) == 1
    clock.t += 7
    assert len(cache) == 0


def test_replacing_resets_the_lifetime():
    cache, clock = make(ttl=10)
    cache.set("a", 1, 2)
    cache.set("a", 3)
    clock.t += 5
    assert cache.get("a") == 3
    cache.set("a", 4, 1)
    clock.t += 1
    assert cache.get("a") is None
