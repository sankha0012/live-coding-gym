import pytest

from solution import find_leaky_features

LABELS = [0, 1, 0, 1, 1, 0, 1, 0]


def test_exact_copy_is_leaky():
    feats = {"leak": [0, 1, 0, 1, 1, 0, 1, 0], "noise": [3, 1, 4, 1, 5, 9, 2, 6]}
    assert find_leaky_features(feats, LABELS) == ["leak"]


def test_negative_correlation_counts():
    feats = {"inverted": [1, 0, 1, 0, 0, 1, 0, 1]}
    assert find_leaky_features(feats, LABELS) == ["inverted"]


def test_constant_feature_not_leaky():
    assert find_leaky_features({"const": [7] * 8}, LABELS) == []


def test_threshold_and_order():
    feats = {
        "b": [0, 1, 0, 1, 1, 0, 1, 0],
        "a": [0, 1, 0, 1, 1, 0, 1, 0],
        "aa_close": [0.1, 0.9, 0.2, 0.8, 0.9, 0.1, 0.8, 0.2],
    }
    assert find_leaky_features(feats, LABELS, threshold=0.95) == ["a", "b", "aa_close"]
    assert find_leaky_features(feats, LABELS, threshold=0.995) == ["a", "b"]


def test_constant_labels_never_leaky():
    assert find_leaky_features({"x": [1, 2, 3]}, [1, 1, 1]) == []


def test_empty_features():
    assert find_leaky_features({}, LABELS) == []


def test_length_mismatch_raises():
    with pytest.raises(ValueError):
        find_leaky_features({"x": [1, 2, 3]}, LABELS)
