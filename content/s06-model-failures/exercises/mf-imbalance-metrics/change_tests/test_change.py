import pytest

from solution import binary_metrics


def test_positive_zero_metrics():
    m = binary_metrics([0, 0, 0, 0, 1], [0, 0, 0, 0, 0], positive=0)
    assert m["precision"] == pytest.approx(0.8)
    assert m["recall"] == pytest.approx(1.0)
    assert m["f1"] == pytest.approx(8 / 9)
    assert m["accuracy"] == pytest.approx(0.8)


def test_default_is_still_label_one():
    m = binary_metrics([0, 0, 0, 0, 1], [0, 0, 0, 0, 0])
    assert m["precision"] == 0.0 and m["recall"] == 0.0 and m["f1"] == 0.0


def test_positive_zero_second_case():
    m = binary_metrics([1, 1, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0], positive=0)
    assert m["precision"] == pytest.approx(1.0)
    assert m["recall"] == pytest.approx(0.75)
    assert m["f1"] == pytest.approx(6 / 7)


def test_explicit_positive_one_matches_default():
    yt, yp = [1, 1, 0, 0, 1, 0], [1, 0, 0, 1, 1, 0]
    assert binary_metrics(yt, yp, positive=1) == binary_metrics(yt, yp)


def test_no_example_of_chosen_label_gives_zeros():
    m = binary_metrics([1, 1, 1], [1, 1, 1], positive=0)
    assert m["precision"] == 0.0 and m["recall"] == 0.0 and m["f1"] == 0.0
    assert m["accuracy"] == pytest.approx(1.0)


def test_length_mismatch_still_raises():
    with pytest.raises(ValueError):
        binary_metrics([1, 0], [1], positive=0)
