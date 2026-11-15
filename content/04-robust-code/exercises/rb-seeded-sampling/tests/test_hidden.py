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


def test_returns_a_list_and_accepts_any_items():
    assert isinstance(sample_ids(IDS, 5, 1), list)
    assert isinstance(sample_ids(IDS, 0, 1), list)
    rows = [{"id": i} for i in range(10)]
    got = sample_ids(rows, 4, 2)
    assert len(got) == 4 and all(any(g is r for r in rows) for g in got)
    assert len({id(g) for g in got}) == 4
    assert sample_ids([[1], [2], [3]], 3, 0) != [] and len(sample_ids([[1], [2], [3]], 2, 0)) == 2


def test_sample_is_random_not_a_slice():
    pos = {x: i for i, x in enumerate(IDS)}
    seen_gap = seen_unsorted = False
    covered = set()
    for seed in range(20):
        p = [pos[x] for x in sample_ids(IDS, 5, seed)]
        covered |= set(p)
        if max(p) - min(p) != 4:
            seen_gap = True
        if p != sorted(p):
            seen_unsorted = True
    assert seen_gap and seen_unsorted
    assert len(covered) > 60
    assert min(covered) < 10 and max(covered) > 90


def test_same_seed_repeatable_many_times_and_k_equals_len():
    first = sample_ids(IDS, 7, 11)
    for _ in range(3):
        assert sample_ids(IDS, 7, 11) == first
    full = sample_ids(IDS, len(IDS), 9)
    assert sorted(full) == sorted(IDS)
    assert sample_ids(IDS, len(IDS), 9) == full
