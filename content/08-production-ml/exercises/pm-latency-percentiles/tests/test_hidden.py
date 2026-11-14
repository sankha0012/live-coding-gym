import random

from solution import percentiles


def test_one_to_hundred():
    assert percentiles(list(range(1, 101))) == {"p50": 50, "p95": 95, "p99": 99}


def test_one_to_ten():
    assert percentiles(list(range(1, 11))) == {"p50": 5, "p95": 10, "p99": 10}


def test_unsorted_and_not_mutated():
    data = list(range(1, 101))
    random.Random(7).shuffle(data)
    snapshot = list(data)
    assert percentiles(data) == {"p50": 50, "p95": 95, "p99": 99}
    assert data == snapshot


def test_single_value():
    assert percentiles([42]) == {"p50": 42, "p95": 42, "p99": 42}


def test_empty():
    assert percentiles([]) == {"p50": None, "p95": None, "p99": None}


def test_outlier_drives_tail():
    data = [10.0] * 99 + [900.0]
    r = percentiles(data)
    assert r["p50"] == 10.0 and r["p95"] == 10.0 and r["p99"] == 10.0
    data = [10.0] * 98 + [900.0, 900.0]
    assert percentiles(data)["p99"] == 900.0


def test_returns_observed_values():
    data = [1, 100]
    assert set(percentiles(data).values()) <= {1, 100}


def test_rank_is_ceiling_not_round():
    assert percentiles([1, 2, 3, 4, 5])["p50"] == 3
    assert percentiles([1, 2, 3, 4, 5, 6, 7])["p50"] == 4
    assert percentiles([1, 2, 3])["p50"] == 2
