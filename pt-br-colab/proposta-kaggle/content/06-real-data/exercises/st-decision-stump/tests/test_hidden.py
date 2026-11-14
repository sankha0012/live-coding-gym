import random

import pytest

from solution import fit_stump, predict


def sample(seed, n, rule, noise=0.08, missing=0.05):
    rng = random.Random(seed)
    xs, ys = [], []
    for _ in range(n):
        x = rng.uniform(0, 20)
        y = rule(x)
        if rng.random() < noise:
            y = 1 - y
        xs.append(None if rng.random() < missing else x)
        ys.append(y)
    return xs, ys


def accuracy(model, xs, ys):
    return sum(predict(model, x) == y for x, y in zip(xs, ys)) / len(ys)


def test_learns_upper_threshold():
    rule = lambda x: int(x > 12)
    model = fit_stump(*sample(1, 400, rule))
    assert accuracy(model, *sample(2, 2000, rule)) >= 0.85


def test_learns_lower_threshold():
    rule = lambda x: int(x < 5)
    model = fit_stump(*sample(3, 400, rule))
    assert accuracy(model, *sample(4, 2000, rule)) >= 0.85


def test_missing_input_uses_fallback():
    model = fit_stump([1.0, 2.0, 3.0, None], [1, 1, 0, 1])
    assert predict(model, None) == 1


def test_fallback_tie_is_zero():
    model = fit_stump([1.0, 2.0], [0, 1])
    assert predict(model, None) == 0


def test_single_class():
    model = fit_stump([1.0, 5.0, 9.0], [1, 1, 1])
    assert [predict(model, x) for x in (1.0, 5.0, 9.0, 100.0)] == [1, 1, 1, 1]


def test_deterministic():
    xs, ys = sample(5, 300, lambda x: int(x > 8))
    assert fit_stump(xs, ys) == fit_stump(list(xs), list(ys))


def test_returns_plain_ints():
    model = fit_stump([1.0, 2.0, 3.0, 4.0], [0, 0, 1, 1])
    assert predict(model, 3.5) == 1 and predict(model, 1.5) == 0


def test_bad_input():
    with pytest.raises(ValueError):
        fit_stump([1.0, 2.0], [1])
    with pytest.raises(ValueError):
        fit_stump([None, None], [0, 1])
