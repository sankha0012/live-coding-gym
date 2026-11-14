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
