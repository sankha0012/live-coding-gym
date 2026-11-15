import pytest

from solution import sample_ids

IDS = [f"id{i}" for i in range(100)]


def test_excluded_never_picked():
    banned = IDS[:50]
    for seed in range(10):
        got = sample_ids(IDS, 20, seed, exclude=banned)
        assert len(got) == 20 and len(set(got)) == 20
        assert not set(got) & set(banned)


def test_everything_left_is_picked_when_k_matches():
    got = sample_ids(IDS, 10, 3, exclude=IDS[:90])
    assert sorted(got) == sorted(IDS[90:])


def test_k_is_checked_against_remaining_items():
    with pytest.raises(ValueError):
        sample_ids(["a", "b", "c"], 3, 1, exclude=["b"])
    assert sorted(sample_ids(["a", "b", "c"], 2, 1, exclude=["b"])) == ["a", "c"]
    with pytest.raises(ValueError):
        sample_ids(IDS, 11, 1, exclude=IDS[:90])


def test_exclude_values_not_in_ids_are_ignored():
    got = sample_ids(["a", "b", "c"], 3, 1, exclude=["zzz"])
    assert sorted(got) == ["a", "b", "c"]


def test_repeatable_and_input_not_modified():
    ids = list(IDS)
    a = sample_ids(ids, 10, 5, exclude=IDS[:30])
    assert ids == IDS
    assert sample_ids(ids, 10, 5, exclude=IDS[:30]) == a


def test_excluding_every_copy_of_a_value():
    got = sample_ids(["a", "a", "b", "c"], 2, 2, exclude=["a"])
    assert sorted(got) == ["b", "c"]


def test_empty_exclude_still_works():
    assert len(sample_ids(IDS, 5, 1, exclude=[])) == 5
