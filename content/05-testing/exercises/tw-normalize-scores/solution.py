from solution import normalize_scores
import pytest


def test_scales_to_zero_one():
    assert normalize_scores([10, 20, 30]) == pytest.approx([0.0, 0.5, 1.0])


def test_order_kept_and_negative_values():
    assert normalize_scores([5, -5, 0]) == pytest.approx([1.0, 0.0, 0.5])


def test_constant_input_gives_zeros():
    assert normalize_scores([7, 7, 7]) == [0.0, 0.0, 0.0]


def test_single_value():
    assert normalize_scores([3]) == [0.0]


def test_empty_input():
    assert normalize_scores([]) == []


def test_input_not_modified():
    values = [2, 4, 6]
    normalize_scores(values)
    assert values == [2, 4, 6]
