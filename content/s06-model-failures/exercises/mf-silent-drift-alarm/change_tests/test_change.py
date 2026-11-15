from solution import drift_alarm

REF = [0.0, 2.0]  # mean 1, population std 1
NO_DATA = {"alarm": False, "reasons": ["no_data"]}


def test_window_below_minimum_is_no_data():
    assert drift_alarm(REF, [10.0, 10.0], min_live=3) == NO_DATA
    assert drift_alarm(REF, [10.0], min_live=2) == NO_DATA


def test_window_at_minimum_is_judged():
    assert drift_alarm(REF, [10.0, 10.0, 10.0], min_live=3) == {"alarm": True, "reasons": ["mean"]}
    assert drift_alarm(REF, [1.0, 1.0], min_live=2) == {"alarm": False, "reasons": []}


def test_empty_live_is_still_no_data():
    assert drift_alarm(REF, [], min_live=5) == NO_DATA
    assert drift_alarm(REF, [], min_live=0) == NO_DATA


def test_default_keeps_old_behaviour():
    assert drift_alarm(REF, [10.0]) == {"alarm": True, "reasons": ["mean"]}


def test_works_together_with_k():
    assert drift_alarm(REF, [2.0, 4.0], k=0.5, min_live=2) == {"alarm": True, "reasons": ["mean"]}
    assert drift_alarm(REF, [2.0, 4.0], k=0.5, min_live=3) == NO_DATA
