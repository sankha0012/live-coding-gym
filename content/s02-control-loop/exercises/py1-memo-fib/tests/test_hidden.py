from solution import fib


class CountingDict(dict):
    def __init__(self):
        super().__init__()
        self.sets = 0

    def __setitem__(self, k, v):
        self.sets += 1
        super().__setitem__(k, v)


def test_small_values():
    c = {}
    assert [fib(i, c) for i in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_large_value():
    assert fib(90, {}) == 2880067194370816120


def test_cache_is_filled_once():
    c = CountingDict()
    assert fib(50, c) == 12586269025
    assert c.sets == 49
    assert fib(50, c) == 12586269025
    assert c.sets == 49


def test_default_cache_persists():
    fib(60)
    assert 60 in fib.__defaults__[0]
