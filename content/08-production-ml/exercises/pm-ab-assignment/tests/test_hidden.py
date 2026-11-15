import os
import subprocess
import sys

import pytest
from solution import assign

W = {"control": 1, "new": 1}


def test_sticky():
    first = [assign(f"u{i}", "exp-a", W) for i in range(200)]
    again = [assign(f"u{i}", "exp-a", W) for i in range(200)]
    assert first == again


def test_returns_known_variant():
    assert assign("u1", "e", {"a": 1, "b": 2, "c": 3}) in {"a", "b", "c"}


def test_weights_respected():
    n = 5000
    got = [assign(f"user-{i}", "exp-w", {"control": 9, "new": 1}) for i in range(n)]
    share = got.count("new") / n
    assert 0.07 < share < 0.13


def test_even_split():
    n = 4000
    got = [assign(f"user-{i}", "exp-e", W) for i in range(n)]
    assert 0.46 < got.count("new") / n < 0.54


def test_zero_weight_never_assigned():
    for i in range(500):
        assert assign(f"u{i}", "e", {"a": 0, "b": 1, "c": 0}) == "b"


def test_experiments_independent():
    n = 4000
    a = [assign(f"user-{i}", "exp-one", W) for i in range(n)]
    b = [assign(f"user-{i}", "exp-two", W) for i in range(n)]
    same = sum(x == y for x, y in zip(a, b)) / n
    assert 0.42 < same < 0.58


@pytest.mark.parametrize("bad", [{}, {"a": -1, "b": 2}, {"a": 0, "b": 0}])
def test_bad_weights(bad):
    with pytest.raises(ValueError):
        assign("u1", "e", bad)


def test_same_in_every_process():
    here = os.path.dirname(os.path.abspath(__import__("solution").__file__))
    code = (
        "from solution import assign;"
        "print([assign(f'u{i}', 'e', {'a': 1, 'b': 1, 'c': 1}) for i in range(50)])"
    )
    outs = set()
    for seed in ("1", "2", "3"):
        env = dict(os.environ, PYTHONHASHSEED=seed)
        r = subprocess.run([sys.executable, "-c", code], cwd=here, env=env,
                           capture_output=True, text=True, timeout=5)
        assert r.returncode == 0, r.stderr
        outs.add(r.stdout)
    assert len(outs) == 1


def test_fractional_weights():
    n = 4000
    got = [assign(f"user-{i}", "exp-f", {"a": 0.25, "b": 0.75}) for i in range(n)]
    assert 0.21 < got.count("a") / n < 0.29


def test_many_equal_variants_each_get_their_share():
    names = [f"v{i}" for i in range(6)]
    n = 6000
    got = [assign(f"user-{i}", "exp-six", {k: 1 for k in names}) for i in range(n)]
    for k in names:
        assert 0.145 < got.count(k) / n < 0.19, k


def test_uneven_three_way_split():
    n = 6000
    got = [assign(f"user-{i}", "exp-3", {"a": 1, "b": 2, "c": 7}) for i in range(n)]
    for k, want in (("a", 0.1), ("b", 0.2), ("c", 0.7)):
        assert abs(got.count(k) / n - want) < 0.03, k


def test_single_variant():
    assert assign("u", "e", {"only": 5}) == "only"
