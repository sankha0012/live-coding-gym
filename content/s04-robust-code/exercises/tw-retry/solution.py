import pytest

from solution import retry


def make_flaky(failures, result="ok"):
    state = {"calls": 0}

    def fn():
        state["calls"] += 1
        if state["calls"] <= failures:
            raise ValueError(f"fail {state['calls']}")
        return result

    return fn, state


def test_success_first_try_does_not_sleep():
    fn, state = make_flaky(0)
    sleeps = []
    assert retry(fn, 3, sleeps.append) == "ok"
    assert state["calls"] == 1
    assert sleeps == []


def test_succeeds_after_failures():
    fn, state = make_flaky(2)
    sleeps = []
    assert retry(fn, 3, sleeps.append) == "ok"
    assert state["calls"] == 3
    assert sleeps == [1, 1]


def test_retries_on_any_exception_type():
    calls = []

    def fn():
        calls.append(1)
        if len(calls) == 1:
            raise KeyError("x")
        return 7

    assert retry(fn, 2, lambda s: None) == 7


def test_uses_all_tries_then_raises_last_error():
    fn, state = make_flaky(10)
    with pytest.raises(ValueError, match="fail 3"):
        retry(fn, 3, lambda s: None)
    assert state["calls"] == 3


def test_no_sleep_after_last_failure():
    fn, _ = make_flaky(10)
    sleeps = []
    with pytest.raises(ValueError):
        retry(fn, 3, sleeps.append)
    assert sleeps == [1, 1]


def test_single_try():
    fn, state = make_flaky(1)
    sleeps = []
    with pytest.raises(ValueError):
        retry(fn, 1, sleeps.append)
    assert state["calls"] == 1
    assert sleeps == []
