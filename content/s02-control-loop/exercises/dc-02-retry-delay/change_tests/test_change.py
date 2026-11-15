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


def test_factor_three_delays_in_seconds():
    sleeps = []
    out = retry(Flaky(3), attempts=4, base_ms=100, cap_ms=5000, sleep=sleeps.append, factor=3)
    assert out == "ok"
    assert sleeps == pytest.approx([0.1, 0.3, 0.9])


def test_factor_delay_is_still_capped():
    sleeps = []
    out = retry(Flaky(4), attempts=5, base_ms=100, cap_ms=500, sleep=sleeps.append, factor=3)
    assert out == "ok"
    assert sleeps == pytest.approx([0.1, 0.3, 0.5, 0.5])


def test_factor_still_raises_last_without_final_sleep():
    fn = Flaky(10)
    sleeps = []
    with pytest.raises(RuntimeError, match="fail 3"):
        retry(fn, attempts=3, base_ms=100, cap_ms=5000, sleep=sleeps.append, factor=3)
    assert sleeps == pytest.approx([0.1, 0.3])


def test_default_factor_is_two():
    sleeps = []
    retry(Flaky(3), attempts=4, base_ms=100, cap_ms=5000, sleep=sleeps.append)
    assert sleeps == pytest.approx([0.1, 0.2, 0.4])
