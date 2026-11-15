import pytest
from solution import DriftAlert


def feed(a, scores):
    return [a.update(s) for s in scores]


def test_starts_inactive():
    assert DriftAlert(0.25, 0.1).active is False


def test_raise_and_clear():
    a = DriftAlert(0.25, 0.10)
    assert feed(a, [0.05, 0.30, 0.05]) == [None, "raised", "cleared"]
    assert a.active is False


def test_no_flapping_inside_band():
    a = DriftAlert(0.25, 0.10)
    events = feed(a, [0.30, 0.20, 0.24, 0.12, 0.26, 0.15])
    assert events == ["raised", None, None, None, None, None]
    assert a.active is True


def test_boundaries_do_not_change_state():
    a = DriftAlert(0.25, 0.10)
    assert a.update(0.25) is None and a.active is False
    a.update(0.26)
    assert a.update(0.10) is None and a.active is True


def test_repeat_events_are_none():
    a = DriftAlert(0.25, 0.10)
    assert feed(a, [0.5, 0.6, 0.7]) == ["raised", None, None]
    assert feed(a, [0.0, 0.0]) == ["cleared", None]


def test_raise_again_after_clear():
    a = DriftAlert(1, 0)
    assert feed(a, [2, -1, 2]) == ["raised", "cleared", "raised"]


def test_equal_thresholds_allowed():
    a = DriftAlert(0.2, 0.2)
    assert feed(a, [0.3, 0.2, 0.1]) == ["raised", None, "cleared"]


def test_bad_thresholds():
    with pytest.raises(ValueError):
        DriftAlert(0.1, 0.2)
