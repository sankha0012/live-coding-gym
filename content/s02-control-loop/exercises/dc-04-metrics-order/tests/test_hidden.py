import pytest

from solution import report


def check(got, p, r, f1):
    assert got["precision"] == pytest.approx(p)
    assert got["recall"] == pytest.approx(r)
    assert got["f1"] == pytest.approx(f1)


def test_asymmetric_case():
    # 3 predicted positive, 1 correct; 1 real positive, 1 found
    check(report([1, 0, 0, 0], [1, 1, 1, 0]), 1 / 3, 1.0, 0.5)


def test_other_asymmetry():
    check(report([1, 1, 1, 0], [1, 0, 0, 0]), 1.0, 1 / 3, 0.5)


def test_perfect():
    check(report([1, 0, 1], [1, 0, 1]), 1.0, 1.0, 1.0)


def test_no_predicted_positives():
    check(report([0, 0, 1], [0, 0, 0]), 0.0, 0.0, 0.0)


def test_all_wrong():
    check(report([0, 1], [1, 0]), 0.0, 0.0, 0.0)


def test_recall_only_zero():
    check(report([1, 1, 0], [0, 0, 1]), 0.0, 0.0, 0.0)


def test_empty():
    check(report([], []), 0.0, 0.0, 0.0)


def test_length_mismatch_raises():
    with pytest.raises(ValueError):
        report([1, 0], [1])
