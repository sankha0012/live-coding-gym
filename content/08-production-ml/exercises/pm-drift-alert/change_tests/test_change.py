from solution import DriftAlert


def test_starts_at_zero():
    assert DriftAlert(0.25, 0.1).raised_count == 0


def test_counts_each_raise():
    a = DriftAlert(0.25, 0.10)
    for s in [0.3, 0.05, 0.3, 0.4]:
        a.update(s)
    assert a.raised_count == 2


def test_none_and_clear_do_not_count():
    a = DriftAlert(0.25, 0.10)
    for s in [0.05, 0.2, 0.25]:
        assert a.update(s) is None
    assert a.raised_count == 0
    assert a.update(0.5) == "raised"
    assert a.raised_count == 1
    assert a.update(0.0) == "cleared"
    assert a.raised_count == 1


def test_count_never_goes_down_and_matches_events():
    a = DriftAlert(1, 0)
    events = [a.update(s) for s in [2, 3, -1, -2, 2, -1, 2, 5]]
    assert events == ["raised", None, "cleared", None, "raised", "cleared", "raised", None]
    assert a.raised_count == 3


def test_counts_are_per_instance():
    a, b = DriftAlert(1, 0), DriftAlert(1, 0)
    a.update(2)
    assert a.raised_count == 1 and b.raised_count == 0
