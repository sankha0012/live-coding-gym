import math
from fractions import Fraction

from solution import percentiles


def test_custom_percentiles_one_to_hundred():
    assert percentiles(list(range(1, 101)), ps=(10, 90)) == {"p10": 10, "p90": 90}


def test_order_of_keys_follows_ps():
    got = percentiles(list(range(1, 101)), ps=[99, 1, 50])
    assert list(got) == ["p99", "p1", "p50"]
    assert got == {"p99": 99, "p1": 1, "p50": 50}


def test_nearest_rank_with_custom_ps():
    for n in range(1, 60):
        data = list(range(n, 0, -1))
        want = {f"p{p}": math.ceil(Fraction(p * n, 100)) for p in (25, 75, 100)}
        assert percentiles(data, ps=[25, 75, 100]) == want, n


def test_empty_with_custom_ps():
    assert percentiles([], ps=[75]) == {"p75": None}


def test_single_value_and_list_not_mutated():
    assert percentiles([7], ps=[10, 20]) == {"p10": 7, "p20": 7}
    data = [3, 1, 2]
    percentiles(data, ps=[50])
    assert data == [3, 1, 2]


def test_default_unchanged():
    assert percentiles(list(range(1, 101))) == {"p50": 50, "p95": 95, "p99": 99}
