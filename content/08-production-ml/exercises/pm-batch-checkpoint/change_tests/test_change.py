import pytest
from solution import run_batch


class Handler:
    def __init__(self):
        self.calls = []

    def __call__(self, item):
        self.calls.append(item)
        if item == "boom":
            raise RuntimeError("boom")
        return item * 10


def test_limit_processes_only_part():
    h, store = Handler(), {}
    assert run_batch([1, 2, 3, 4, 5], h, store, limit=2) == [10, 20]
    assert h.calls == [1, 2]
    assert store["next"] == 2


def test_repeated_limited_runs_continue():
    h, store = Handler(), {}
    items = [1, 2, 3, 4, 5]
    assert run_batch(items, h, store, limit=2) == [10, 20]
    assert run_batch(items, h, store, limit=2) == [10, 20, 30, 40]
    assert run_batch(items, h, store, limit=2) == [10, 20, 30, 40, 50]
    assert h.calls == [1, 2, 3, 4, 5]
    assert run_batch(items, h, store, limit=2) == [10, 20, 30, 40, 50]
    assert h.calls == [1, 2, 3, 4, 5]


def test_limit_counts_only_new_items():
    h = Handler()
    store = {"next": 2, "results": ["a", "b"]}
    assert run_batch([1, 2, 3, 4, 5], h, store, limit=2) == ["a", "b", 30, 40]
    assert h.calls == [3, 4]


def test_limit_zero_and_larger_than_work():
    h, store = Handler(), {}
    assert run_batch([1, 2], h, store, limit=0) == []
    assert h.calls == []
    assert run_batch([1, 2], h, store, limit=10) == [10, 20]
    assert h.calls == [1, 2]


def test_failure_with_limit_still_propagates_and_keeps_checkpoint():
    h, store = Handler(), {}
    with pytest.raises(RuntimeError):
        run_batch([1, "boom", 3], h, store, limit=5)
    assert store["next"] == 1
    assert store["results"] == [10]
