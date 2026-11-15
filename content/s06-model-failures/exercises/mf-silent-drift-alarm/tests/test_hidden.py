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


def test_mean_uses_k_too():
    # live mean 3 vs reference mean 1, spread unchanged: beyond 0.5 * 1, inside 3 * 1 and 10 * 1
    live = [2.0, 4.0]
    assert drift_alarm(REF, live, k=0.5) == {"alarm": True, "reasons": ["mean"]}
    assert drift_alarm(REF, live) == {"alarm": False, "reasons": []}
    assert drift_alarm(REF, [10.0, 10.0], k=10.0) == {"alarm": False, "reasons": []}


def test_mean_drop_alarms_too():
    assert drift_alarm(REF, [-10.0, -10.0]) == {"alarm": True, "reasons": ["mean"]}


def test_std_exactly_on_limit_is_not_alarm():
    # live std 4, reference std 1, limit 3
    assert drift_alarm(REF, [-4.0, 4.0]) == {"alarm": False, "reasons": []}


def test_zero_spread_reference_std_change():
    # same mean, but live now spreads out: any std change is beyond a zero limit
    assert drift_alarm([5.0, 5.0], [4.0, 6.0]) == {"alarm": True, "reasons": ["std"]}


def test_single_value_windows():
    assert drift_alarm(REF, [1.0]) == {"alarm": False, "reasons": []}
    assert drift_alarm([5.0], [5.0, 5.0]) == {"alarm": False, "reasons": []}
