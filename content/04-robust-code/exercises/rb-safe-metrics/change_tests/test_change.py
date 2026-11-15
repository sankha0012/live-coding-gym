import math

from solution import safe_mean


def test_default_for_empty_and_all_invalid():
    assert safe_mean([], 0.0) == 0.0
    assert safe_mean([None, float("nan")], default=-1) == -1
    assert safe_mean([None], default="n/a") == "n/a"


def test_default_ignored_when_there_are_valid_values():
    assert safe_mean([1, 3], 99) == 2
    assert safe_mean([0, None], default=99) == 0.0
    assert safe_mean([float("nan"), 4.0], default=99) == 4.0


def test_default_none_is_the_old_behaviour():
    assert safe_mean([]) is None
    assert safe_mean([], None) is None
    assert safe_mean([None, float("nan")], default=None) is None


def test_nan_default_is_returned_as_given():
    assert math.isnan(safe_mean([], float("nan")))
