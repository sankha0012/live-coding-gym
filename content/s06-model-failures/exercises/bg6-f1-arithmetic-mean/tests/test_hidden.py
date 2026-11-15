import pytest

from solution import binary_metrics


def test_mixed():
    m = binary_metrics([1, 1, 0, 0, 1, 0], [1, 0, 0, 1, 1, 0])
    assert m["accuracy"] == pytest.approx(4 / 6)
    assert m["precision"] == pytest.approx(2 / 3)
    assert m["recall"] == pytest.approx(2 / 3)
    assert m["f1"] == pytest.approx(2 / 3)


def test_f1_is_harmonic_mean():
    m = binary_metrics([1, 1, 1, 1, 0], [1, 0, 0, 0, 0])
    assert m["precision"] == pytest.approx(1.0)
    assert m["recall"] == pytest.approx(0.25)
    assert m["f1"] == pytest.approx(0.4)


def test_always_negative_on_imbalanced():
    y_true = [0] * 98 + [1, 1]
    m = binary_metrics(y_true, [0] * 100)
    assert m["accuracy"] == pytest.approx(0.98)
    assert m["precision"] == 0.0 and m["recall"] == 0.0 and m["f1"] == 0.0


def test_no_positives_in_truth():
    m = binary_metrics([0, 0, 0], [1, 0, 0])
    assert m["recall"] == 0.0 and m["precision"] == 0.0
    assert m["accuracy"] == pytest.approx(2 / 3)


def test_empty():
    assert binary_metrics([], []) == {"accuracy": 0.0, "precision": 0.0, "recall": 0.0, "f1": 0.0}


def test_length_mismatch_raises():
    with pytest.raises(ValueError):
        binary_metrics([1, 0], [1])
