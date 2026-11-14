import random

import pytest

from solution import sample_ids

IDS = [f"id{i}" for i in range(100)]


def test_same_seed_same_sample():
    assert sample_ids(IDS, 10, 42) == sample_ids(IDS, 10, 42)


def test_independent_of_global_random_use():
    a = sample_ids(IDS, 10, 7)
    random.seed(999)
    random.random()
    random.random()
    assert sample_ids(IDS, 10, 7) == a


def test_shape_and_uniqueness():
    s = sample_ids(IDS, 25, 1)
    assert len(s) == 25 and len(set(s)) == 25 and set(s) <= set(IDS)


def test_different_seeds_differ():
    assert len({tuple(sample_ids(IDS, 10, s)) for s in range(5)}) > 1


def test_does_not_touch_global_state():
    random.seed(123)
    expected = [random.random() for _ in range(3)]
    random.seed(123)
    sample_ids(IDS, 10, 5)
    assert [random.random() for _ in range(3)] == expected


def test_input_not_modified():
    ids = list(IDS)
    sample_ids(ids, 50, 3)
    assert ids == IDS


def test_edges():
    assert sample_ids(IDS, 0, 1) == []
    assert sorted(sample_ids(["a", "b", "c"], 3, 1)) == ["a", "b", "c"]
    assert sample_ids([], 0, 1) == []


def test_bad_k():
    with pytest.raises(ValueError):
        sample_ids(["a", "b"], 3, 1)
    with pytest.raises(ValueError):
        sample_ids(["a", "b"], -1, 1)


def test_duplicate_values_picked_by_position():
    assert sorted(sample_ids(["a", "a", "b"], 3, 1)) == ["a", "a", "b"]
    assert sample_ids(["x", "x"], 2, 4) == ["x", "x"]
