import pytest

from solution import calibration_bins


def _check(got, want):
    assert len(got) == len(want)
    for g, w in zip(got, want):
        assert g[0] == w[0] and g[3] == w[3]
        assert g[1] == pytest.approx(w[1]) and g[2] == pytest.approx(w[2])


def test_two_bins():
    got = calibration_bins([0.1, 0.2, 0.8, 0.9], [0, 1, 1, 1], n_bins=2)
    _check(got, [(0, 0.15, 0.5, 2), (1, 0.85, 1.0, 2)])


def test_empty_bins_skipped():
    got = calibration_bins([0.05, 0.95, 0.97], [0, 1, 0], n_bins=10)
    _check(got, [(0, 0.05, 0.0, 1), (9, 0.96, 0.5, 2)])


def test_one_goes_to_last_bin():
    got = calibration_bins([1.0, 0.0], [1, 0], n_bins=4)
    _check(got, [(0, 0.0, 0.0, 1), (3, 1.0, 1.0, 1)])


def test_bin_edge_goes_up():
    got = calibration_bins([0.5], [1], n_bins=2)
    _check(got, [(1, 0.5, 1.0, 1)])


def test_float_product_rule_and_unsorted_input():
    # 0.3 * 10 is exactly 3.0, so bin 3 (0.3 // 0.1 would wrongly give 2)
    got = calibration_bins([0.95, 0.3], [1, 0], n_bins=10)
    _check(got, [(3, 0.3, 0.0, 1), (9, 0.95, 1.0, 1)])


def test_empty_input():
    assert calibration_bins([], []) == []


def test_bad_input_raises():
    with pytest.raises(ValueError):
        calibration_bins([0.5, 0.6], [1])
    with pytest.raises(ValueError):
        calibration_bins([1.2], [1])
    with pytest.raises(ValueError):
        calibration_bins([-0.1], [0])


def test_bin_is_floor_not_round():
    # 0.26 * 10 = 2.6 floors to bin 2 (rounding would give 3)
    got = calibration_bins([0.26, 0.74], [1, 0], n_bins=10)
    _check(got, [(2, 0.26, 1.0, 1), (7, 0.74, 0.0, 1)])


def test_default_is_ten_bins():
    got = calibration_bins([0.12, 0.18, 0.99], [0, 1, 1])
    _check(got, [(1, 0.15, 0.5, 2), (9, 0.99, 1.0, 1)])


def test_more_labels_than_probs_raises():
    with pytest.raises(ValueError):
        calibration_bins([0.5], [1, 0])
