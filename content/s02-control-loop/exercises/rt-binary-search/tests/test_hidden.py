from solution import first_index


def test_basic():
    assert first_index([1, 3, 5, 7, 9], 7) == 3


def test_duplicates_first():
    assert first_index([1, 2, 2, 2, 3], 2) == 1
    assert first_index([5, 5, 5, 5], 5) == 0
    assert first_index([1, 2, 2, 3], 2) == 1
    assert first_index([1, 1, 2, 2, 2, 2, 2], 2) == 2


def test_missing():
    assert first_index([1, 3, 5], 4) == -1
    assert first_index([1, 3, 5], 0) == -1
    assert first_index([1, 3, 5], 9) == -1


def test_empty_and_single():
    assert first_index([], 1) == -1
    assert first_index([4], 4) == 0
    assert first_index([4], 5) == -1


def test_ends():
    assert first_index([1, 2, 3, 4], 1) == 0
    assert first_index([1, 2, 3, 4], 4) == 3


class _C(int):
    calls = 0

    def _count(self):
        _C.calls += 1

    def __eq__(self, o):
        self._count()
        return int.__eq__(self, o)

    def __ne__(self, o):
        self._count()
        return int.__ne__(self, o)

    def __lt__(self, o):
        self._count()
        return int.__lt__(self, o)

    def __le__(self, o):
        self._count()
        return int.__le__(self, o)

    def __gt__(self, o):
        self._count()
        return int.__gt__(self, o)

    def __ge__(self, o):
        self._count()
        return int.__ge__(self, o)

    __hash__ = int.__hash__


def _comparisons(values, target, want):
    nums = [_C(v) for v in values]
    _C.calls = 0
    assert first_index(nums, _C(target)) == want
    return _C.calls


def test_is_binary_search_not_linear():
    n = 4096
    assert _comparisons([7] * n, 7, 0) < 100  # long run of duplicates
    assert _comparisons(list(range(n)), n - 1, n - 1) < 100
    assert _comparisons(list(range(n)), n + 5, -1) < 100
    assert _comparisons([i // 3 for i in range(n)], 600, 1800) < 100


def test_exhaustive_small_lists():
    from itertools import combinations_with_replacement
    for size in range(0, 7):
        for nums in combinations_with_replacement(range(4), size):
            nums = list(nums)
            for t in range(-1, 5):
                want = nums.index(t) if t in nums else -1
                assert first_index(nums, t) == want, (nums, t)
