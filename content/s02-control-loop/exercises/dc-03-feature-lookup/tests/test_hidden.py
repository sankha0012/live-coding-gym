from solution import feature_row


def test_all_known():
    assert feature_row(["u1", "u3"], -1.0) == [0.5, 12.0]


def test_unknown_gets_fallback():
    assert feature_row(["u1", "u9"], -1.0) == [0.5, -1.0]


def test_order_follows_keys():
    assert feature_row(["u4", "zz", "u1"], -1.0) == [3.5, -1.0, 0.5]


def test_stored_zero_is_kept():
    assert feature_row(["u2", "u9"], -1.0) == [0.0, -1.0]


def test_duplicates_keep_length():
    assert feature_row(["u1", "u1", "u9"], 7.0) == [0.5, 0.5, 7.0]


def test_fallback_none_is_allowed():
    assert feature_row(["u3", "u9"], None) == [12.0, None]


def test_empty_keys():
    assert feature_row([], -1.0) == []
