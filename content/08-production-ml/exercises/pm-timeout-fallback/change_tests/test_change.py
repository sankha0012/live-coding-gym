from solution import predict_with_fallback


class Clock:
    def __init__(self):
        self.t = 100.0

    def __call__(self):
        return self.t


def make_model(clock, took, boom=None):
    calls = []

    def model(x):
        calls.append(x)
        clock.t += took
        if boom:
            raise boom
        return x * 2

    model.calls = calls
    return model


def test_late_result_is_kept():
    c = Clock()
    m = make_model(c, 2.0)
    assert predict_with_fallback(m, 4, -1, 0.5, c, keep_late=True) == (8, "late")
    assert m.calls == [4]


def test_late_falsy_result_is_kept():
    c = Clock()
    m = make_model(c, 3.0)
    assert predict_with_fallback(m, 0, -1, 0.5, c, keep_late=True) == (0, "late")


def test_in_time_is_still_model():
    c = Clock()
    m = make_model(c, 0.5)
    assert predict_with_fallback(m, 2, -1, 0.5, c, keep_late=True) == (4, "model")


def test_error_still_falls_back_with_keep_late():
    c = Clock()
    m = make_model(c, 5.0, boom=RuntimeError("down"))
    assert predict_with_fallback(m, 1, "fb", 0.5, c, keep_late=True) == ("fb", "error")
    assert m.calls == [1]


def test_default_still_times_out():
    c = Clock()
    m = make_model(c, 2.0)
    assert predict_with_fallback(m, 1, -1, 0.5, c) == (-1, "timeout")
    c2 = Clock()
    m2 = make_model(c2, 2.0)
    assert predict_with_fallback(m2, 1, -1, 0.5, c2, keep_late=False) == (-1, "timeout")
