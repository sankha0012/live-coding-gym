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
