from solution import TransientError, call_with_retry


def flaky(failures, exc=TransientError):
    state = {"calls": 0}

    def fn():
        state["calls"] += 1
        if state["calls"] <= failures:
            raise exc("boom")
        return "ok"

    return fn, state


def test_success_first_try_no_sleep():
    sleeps = []
    fn, st = flaky(0)
    assert call_with_retry(fn, 3, sleeps.append) == "ok"
    assert st["calls"] == 1 and sleeps == []


def test_retries_with_exponential_backoff():
    sleeps = []
    fn, st = flaky(2)
    assert call_with_retry(fn, 3, sleeps.append) == "ok"
    assert st["calls"] == 3
    assert sleeps == [1.0, 2.0]


def test_base_delay():
    sleeps = []
    fn, _ = flaky(3, TimeoutError)
    assert call_with_retry(fn, 3, sleeps.append, base_delay=0.5) == "ok"
    assert sleeps == [0.5, 1.0, 2.0]


def test_permanent_error_not_retried():
    for exc in (ValueError, KeyError, FileNotFoundError):
        sleeps = []
        fn, st = flaky(5, exc)
        try:
            call_with_retry(fn, 3, sleeps.append)
            assert False
        except exc:
            pass
        assert st["calls"] == 1 and sleeps == []


def test_exhausted_reraises_last_without_extra_sleep():
    sleeps = []
    fn, st = flaky(10, ConnectionError)
    try:
        call_with_retry(fn, 2, sleeps.append)
        assert False
    except ConnectionError:
        pass
    assert st["calls"] == 3
    assert sleeps == [1.0, 2.0]


def test_zero_retries():
    sleeps = []
    fn, st = flaky(1)
    try:
        call_with_retry(fn, 0, sleeps.append)
        assert False
    except TransientError:
        pass
    assert st["calls"] == 1 and sleeps == []


def test_backoff_keeps_doubling():
    sleeps = []
    fn, st = flaky(10, TimeoutError)
    try:
        call_with_retry(fn, 5, sleeps.append)
        assert False
    except TimeoutError:
        pass
    assert st["calls"] == 6
    assert sleeps == [1.0, 2.0, 4.0, 8.0, 16.0]


def test_transient_subclasses_are_retried():
    class MyTransient(TransientError):
        pass

    for exc in (ConnectionResetError, BrokenPipeError, ConnectionRefusedError, MyTransient):
        sleeps = []
        fn, st = flaky(1, exc)
        assert call_with_retry(fn, 2, sleeps.append) == "ok"
        assert st["calls"] == 2 and sleeps == [1.0], exc


def test_other_oserrors_are_permanent():
    for exc in (OSError, PermissionError, IsADirectoryError, FileExistsError):
        sleeps = []
        fn, st = flaky(5, exc)
        try:
            call_with_retry(fn, 3, sleeps.append)
            assert False
        except exc:
            pass
        assert st["calls"] == 1 and sleeps == [], exc


def test_last_transient_error_is_the_one_raised():
    sleeps, calls = [], []

    def fn():
        calls.append(1)
        raise TimeoutError("attempt %d" % len(calls))

    try:
        call_with_retry(fn, 2, sleeps.append)
        assert False
    except TimeoutError as e:
        assert str(e) == "attempt 3"
    assert sleeps == [1.0, 2.0]


def test_permanent_error_after_transient_failures_stops_at_once():
    sleeps, calls = [], []

    def fn():
        calls.append(1)
        if len(calls) < 3:
            raise TransientError("t")
        raise ValueError("bad request")

    try:
        call_with_retry(fn, 5, sleeps.append)
        assert False
    except ValueError as e:
        assert str(e) == "bad request"
    assert len(calls) == 3 and sleeps == [1.0, 2.0]
