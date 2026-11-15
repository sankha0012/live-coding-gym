import pytest

from solution import retry


class Flaky:
    def __init__(self, failures, result="ok"):
        self.failures = failures
        self.result = result
        self.calls = 0

    def __call__(self):
        self.calls += 1
        if self.calls <= self.failures:
            raise RuntimeError(f"fail {self.calls}")
        return self.result


def run(fn, attempts=4, base_ms=100, cap_ms=5000):
    sleeps = []
    out = retry(fn, attempts=attempts, base_ms=base_ms, cap_ms=cap_ms, sleep=sleeps.append)
    return out, sleeps


def test_success_first_try_never_sleeps():
    out, sleeps = run(Flaky(0))
    assert out == "ok" and sleeps == []


def test_delays_are_in_seconds():
    out, sleeps = run(Flaky(3))
    assert out == "ok"
    assert sleeps == pytest.approx([0.1, 0.2, 0.4])


def test_delay_is_capped():
    fn = Flaky(5)
    out, sleeps = run(fn, attempts=6, base_ms=1000, cap_ms=3000)
    assert out == "ok"
    assert sleeps == pytest.approx([1.0, 2.0, 3.0, 3.0, 3.0])


def test_raises_last_exception_after_attempts():
    fn = Flaky(10)
    sleeps = []
    with pytest.raises(RuntimeError, match="fail 4"):
        retry(fn, attempts=4, base_ms=100, cap_ms=5000, sleep=sleeps.append)
    assert fn.calls == 4


def test_no_sleep_after_final_failure():
    fn = Flaky(10)
    sleeps = []
    with pytest.raises(RuntimeError):
        retry(fn, attempts=3, base_ms=100, cap_ms=5000, sleep=sleeps.append)
    assert sleeps == pytest.approx([0.1, 0.2])


def test_single_attempt_never_sleeps():
    fn = Flaky(1)
    sleeps = []
    with pytest.raises(RuntimeError):
        retry(fn, attempts=1, base_ms=100, cap_ms=5000, sleep=sleeps.append)
    assert sleeps == [] and fn.calls == 1
