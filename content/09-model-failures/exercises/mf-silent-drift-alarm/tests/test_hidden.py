from solution import drift_alarm

REF = [0.0, 2.0]  # mean 1, population std 1


def test_no_drift():
    assert drift_alarm(REF, [0.0, 2.0, 1.0]) == {"alarm": False, "reasons": []}


def test_mean_shift():
    assert drift_alarm(REF, [10.0, 10.0]) == {"alarm": True, "reasons": ["mean"]}


def test_uses_population_std():
    # diff 3.5 > 3 * 1.0, but would be < 3 * 1.414 with the sample std
    assert drift_alarm(REF, [4.5, 4.5])["alarm"] is True


def test_std_blowup():
    got = drift_alarm(REF, [-10.0, 12.0])
    assert got == {"alarm": True, "reasons": ["std"]}


def test_exactly_on_limit_is_not_alarm():
    assert drift_alarm(REF, [4.0, 4.0]) == {"alarm": False, "reasons": []}


def test_empty_windows_never_raise():
    want = {"alarm": False, "reasons": ["no_data"]}
    assert drift_alarm(REF, []) == want
    assert drift_alarm([], [1.0]) == want


def test_zero_spread_reference():
    assert drift_alarm([5.0, 5.0], [5.0, 5.0]) == {"alarm": False, "reasons": []}
    assert drift_alarm([5.0, 5.0], [6.0, 6.0]) == {"alarm": True, "reasons": ["mean"]}


def test_std_collapse_and_custom_k():
    # reference std 5; live is constant, so the std dropped by 5 > 0.5 * 5
    got = drift_alarm([0.0, 10.0], [5.0, 5.0], k=0.5)
    assert got == {"alarm": True, "reasons": ["std"]}
    assert drift_alarm([0.0, 10.0], [5.0, 5.0]) == {"alarm": False, "reasons": []}


def test_both_reasons_in_order():
    got = drift_alarm(REF, [50.0, 100.0])
    assert got == {"alarm": True, "reasons": ["mean", "std"]}
