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


def test_falsy_results_are_kept():
    c = Clock()
    got = process_until([0, 1, 2, 3], lambda x: None if x % 2 else 0, 100, c)
    assert got == ([0, None, 0, None], [])


def test_generator_input_stopping_midway_keeps_unstarted_items():
    c = Clock()

    def handler(x):
        c.t += 1
        return x * 10

    results, remaining = process_until((i for i in range(6)), handler, 3, c)
    assert results == [0, 10, 20]
    assert remaining == [3, 4, 5] and isinstance(remaining, list)
    results, remaining = process_until((i for i in range(3)), handler, 0, Clock(5))
    assert (results, remaining) == ([], [0, 1, 2])


def test_clock_consulted_before_each_item():
    c = Clock()
    seen = []

    def handler(x):
        seen.append(c.t)
        c.t += 4
        return x

    results, remaining = process_until([1, 2, 3, 4], handler, 9, c)
    assert seen == [0, 4, 8] and results == [1, 2, 3] and remaining == [4]
