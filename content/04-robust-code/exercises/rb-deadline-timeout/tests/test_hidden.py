import pytest

from solution import process_until


class Clock:
    def __init__(self, t=0.0):
        self.t = t

    def __call__(self):
        return self.t


def test_all_done_before_deadline():
    c = Clock()
    got = process_until([1, 2, 3], lambda x: x * 2, 100, c)
    assert got == ([2, 4, 6], [])


def test_stops_when_time_runs_out():
    c = Clock()

    def handler(x):
        c.t += 10
        return x

    results, remaining = process_until(list("abcde"), handler, 25, c)
    assert results == ["a", "b", "c"]
    assert remaining == ["d", "e"]


def test_boundary_is_exclusive():
    c = Clock()

    def handler(x):
        c.t += 5
        return x

    results, remaining = process_until([1, 2, 3], handler, 10, c)
    assert results == [1, 2]
    assert remaining == [3]


def test_deadline_already_passed():
    c = Clock(50)
    calls = []
    items = [1, 2]
    results, remaining = process_until(items, calls.append, 50, c)
    assert (results, remaining) == ([], [1, 2])
    assert calls == []
    assert remaining is not items


def test_empty_items():
    assert process_until([], lambda x: x, 10, Clock()) == ([], [])


def test_handler_error_propagates():
    def handler(x):
        if x == 2:
            raise RuntimeError("boom")
        return x

    with pytest.raises(RuntimeError):
        process_until([1, 2, 3], handler, 100, Clock())


def test_input_not_modified_and_works_on_iterables():
    items = [1, 2, 3]
    process_until(items, lambda x: x, 100, Clock())
    assert items == [1, 2, 3]
    assert process_until(iter([1, 2]), lambda x: x, 100, Clock()) == ([1, 2], [])
