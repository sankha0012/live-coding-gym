import math


def _ns():
    ns = {'__name__': '__main__'}
    exec(open('solution.py').read(), ns)
    return ns


def _close(a, b):
    return abs(a - b) <= 1e-9 + 1e-9 * abs(b)


def _unpooled(x1, n1, x2, n2):
    p1, p2 = x1 / n1, x2 / n2
    return (p2 - p1) / math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)


def test_unpooled_values():
    f = _ns()["two_prop_z"]
    assert _close(f(30, 200, 90, 400, pooled=False), _unpooled(30, 200, 90, 400))
    assert round(f(30, 200, 90, 400, pooled=False), 3) == 2.289
    assert _close(f(120, 1000, 150, 1000, pooled=False), _unpooled(120, 1000, 150, 1000))
    assert _close(f(90, 400, 30, 200, pooled=False), -_unpooled(30, 200, 90, 400))


def test_unpooled_differs_from_pooled_and_equal_rates_zero():
    f = _ns()["two_prop_z"]
    assert not _close(f(30, 200, 90, 400, pooled=False), f(30, 200, 90, 400))
    assert f(50, 500, 50, 500, pooled=False) == 0.0


def test_default_and_pooled_true_unchanged():
    f = _ns()["two_prop_z"]
    assert round(f(120, 1000, 150, 1000), 3) == 1.963
    assert _close(f(30, 200, 90, 400), f(30, 200, 90, 400, pooled=True))
