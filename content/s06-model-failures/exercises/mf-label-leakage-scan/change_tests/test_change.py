import pytest

from solution import find_leaky_features

LABELS = [0, 1, 0, 1, 1, 0, 1, 0]
FEATS = {
    "c": [0.1, 0.9, 0.2, 0.8, 0.9, 0.1, 0.8, 0.2],  # about 0.98
    "b": [0, 1, 0, 1, 1, 0, 1, 0],
    "a": [1, 0, 1, 0, 0, 1, 0, 1],  # exactly -1
    "noise": [3, 1, 4, 1, 5, 9, 2, 6],
}


def test_unlimited_order_is_as_before():
    assert find_leaky_features(FEATS, LABELS) == ["a", "b", "c"]


def test_top_k_keeps_the_strongest():
    assert find_leaky_features(FEATS, LABELS, top_k=2) == ["a", "b"]
    assert find_leaky_features(FEATS, LABELS, top_k=1) == ["a"]


def test_top_k_larger_than_result():
    assert find_leaky_features(FEATS, LABELS, top_k=10) == ["a", "b", "c"]


def test_top_k_zero_is_empty():
    assert find_leaky_features(FEATS, LABELS, top_k=0) == []


def test_top_k_none_means_all():
    assert find_leaky_features(FEATS, LABELS, top_k=None) == ["a", "b", "c"]


def test_top_k_with_threshold():
    assert find_leaky_features(FEATS, LABELS, threshold=0.995, top_k=1) == ["a"]


def test_length_check_still_applies_with_top_k():
    with pytest.raises(ValueError):
        find_leaky_features({"ok": LABELS, "short": [1, 2]}, LABELS, top_k=1)
