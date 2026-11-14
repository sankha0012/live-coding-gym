from solution import predict_with_fallback


class Clock:
    def __init__(self):
        self.t = 100.0

    def __call__(self):
        return self.t


def make_model(clock, took, result=None, boom=None):
    calls = []

    def model(x):
        calls.append(x)
        clock.t += took
        if boom:
            raise boom
        return result if result is not None else x * 2

    model.calls = calls
    return model


def test_fast_call():
    c = Clock()
    m = make_model(c, 0.05)
    assert predict_with_fallback(m, 4, -1, 0.1, c) == (8, "model")
    assert m.calls == [4]


def test_exactly_at_deadline_is_ok():
    c = Clock()
    m = make_model(c, 0.5)
    assert predict_with_fallback(m, 1, -1, 0.5, c) == (2, "model")


def test_slow_call_uses_fallback():
    c = Clock()
    m = make_model(c, 2.0)
    assert predict_with_fallback(m, 1, -1, 0.5, c) == (-1, "timeout")
    assert m.calls == [1]


def test_exception_uses_fallback():
    c = Clock()
    m = make_model(c, 0.01, boom=RuntimeError("model down"))
    assert predict_with_fallback(m, 1, -1, 0.5, c) == (-1, "error")
    assert m.calls == [1]


def test_slow_and_raising_is_error():
    c = Clock()
    m = make_model(c, 5.0, boom=ValueError("x"))
    assert predict_with_fallback(m, 1, "fb", 0.5, c) == ("fb", "error")


def test_falsy_results_are_kept():
    c = Clock()
    assert predict_with_fallback(lambda x: 0, 1, -1, 1, c) == (0, "model")
    assert predict_with_fallback(lambda x: None, 1, -1, 1, c) == (None, "model")
