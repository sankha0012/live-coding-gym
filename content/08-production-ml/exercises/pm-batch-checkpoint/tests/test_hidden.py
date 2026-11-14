import pytest
from solution import run_batch


class Handler:
    def __init__(self, fail_at=None):
        self.calls = []
        self.fail_at = set(fail_at or [])

    def __call__(self, item):
        self.calls.append(item)
        if item in self.fail_at:
            self.fail_at.discard(item)
            raise RuntimeError(f"crash on {item}")
        return item * 10


def test_full_run():
    h, store = Handler(), {}
    assert run_batch([1, 2, 3], h, store) == [10, 20, 30]
    assert h.calls == [1, 2, 3]


def test_empty_items():
    assert run_batch([], Handler(), {}) == []


def test_crash_then_resume():
    items = [1, 2, 3, 4, 5]
    h, store = Handler(fail_at=[3]), {}
    with pytest.raises(RuntimeError):
        run_batch(items, h, store)
    assert store["next"] == 2
    assert store["results"] == [10, 20]
    assert run_batch(items, h, store) == [10, 20, 30, 40, 50]
    assert h.calls == [1, 2, 3, 3, 4, 5]


def test_finished_items_not_reprocessed():
    h, store = Handler(), {}
    run_batch([1, 2], h, store)
    assert run_batch([1, 2], h, store) == [10, 20]
    assert h.calls == [1, 2]


def test_crash_on_first_item_keeps_checkpoint_at_zero():
    h, store = Handler(fail_at=[1]), {}
    with pytest.raises(RuntimeError):
        run_batch([1, 2], h, store)
    assert store.get("next", 0) == 0
    assert store.get("results", []) == []
    assert run_batch([1, 2], h, store) == [10, 20]


def test_resume_from_existing_checkpoint():
    h = Handler()
    store = {"next": 2, "results": ["a", "b"]}
    assert run_batch([1, 2, 3, 4], h, store) == ["a", "b", 30, 40]
    assert h.calls == [3, 4]
