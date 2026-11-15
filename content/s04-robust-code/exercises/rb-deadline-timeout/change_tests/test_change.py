from solution import process_until


class Clock:
    def __init__(self, t=0.0):
        self.t = t

    def __call__(self):
        return self.t


def test_max_items_limits_work():
    calls = []

    def handler(x):
        calls.append(x)
        return x * 2

    got = process_until([1, 2, 3, 4], handler, 100, Clock(), max_items=2)
    assert got == ([2, 4], [3, 4])
    assert calls == [1, 2]


def test_max_items_zero_runs_nothing():
    calls = []
    got = process_until([1, 2], calls.append, 100, Clock(), max_items=0)
    assert got == ([], [1, 2]) and calls == []


def test_max_items_larger_than_items():
    assert process_until([1, 2], lambda x: x, 100, Clock(), max_items=10) == ([1, 2], [])


def test_deadline_can_stop_before_max_items():
    c = Clock()

    def handler(x):
        c.t += 10
        return x

    got = process_until(list("abcde"), handler, 25, c, max_items=4)
    assert got == (["a", "b", "c"], ["d", "e"])


def test_max_items_stops_before_deadline_and_none_means_no_limit():
    c = Clock()

    def handler(x):
        c.t += 1
        return x

    assert process_until([1, 2, 3, 4], handler, 100, c, max_items=3) == ([1, 2, 3], [4])
    assert process_until([1, 2, 3], handler, 1000, Clock(), max_items=None) == ([1, 2, 3], [])


def test_generator_input_with_max_items():
    got = process_until((i for i in range(5)), lambda x: x, 100, Clock(), max_items=2)
    assert got == ([0, 1], [2, 3, 4]) and isinstance(got[1], list)
