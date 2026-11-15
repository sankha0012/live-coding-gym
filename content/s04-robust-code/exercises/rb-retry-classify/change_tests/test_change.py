from solution import TransientError, call_with_retry


def failing(n, exc=TransientError):
    calls = []

    def fn():
        calls.append(1)
        if len(calls) <= n:
            raise exc("boom")
        return "ok"

    return fn, calls


def test_delay_is_capped():
    sleeps = []
    fn, calls = failing(4)
    assert call_with_retry(fn, 4, sleeps.append, base_delay=1.0, max_delay=3.0) == "ok"
    assert sleeps == [1.0, 2.0, 3.0, 3.0]
    assert len(calls) == 5


def test_cap_given_by_keyword_with_other_base():
    sleeps = []
    fn, _ = failing(3, TimeoutError)
    call_with_retry(fn, 3, sleeps.append, 0.5, max_delay=0.75)
    assert sleeps == [0.5, 0.75, 0.75]


def test_cap_above_all_delays_changes_nothing():
    sleeps = []
    fn, _ = failing(3)
    call_with_retry(fn, 3, sleeps.append, max_delay=100.0)
    assert sleeps == [1.0, 2.0, 4.0]


def test_none_means_no_cap():
    sleeps = []
    fn, _ = failing(5)
    call_with_retry(fn, 5, sleeps.append, max_delay=None)
    assert sleeps == [1.0, 2.0, 4.0, 8.0, 16.0]


def test_capped_still_does_not_sleep_after_last_failure_or_retry_permanent():
    sleeps = []
    fn, calls = failing(10)
    try:
        call_with_retry(fn, 2, sleeps.append, max_delay=1.5)
        assert False
    except TransientError:
        pass
    assert sleeps == [1.0, 1.5] and len(calls) == 3
    sleeps = []
    fn, calls = failing(10, ValueError)
    try:
        call_with_retry(fn, 2, sleeps.append, max_delay=1.5)
        assert False
    except ValueError:
        pass
    assert sleeps == [] and len(calls) == 1
