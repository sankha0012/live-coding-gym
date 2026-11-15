def _close(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= 1e-6 + 1e-9 * abs(b)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_close(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_close(a[k], b[k]) for k in a)
    return a == b

PRE = ''

def _ns():
    ns = {'__name__': '__main__'}
    exec(open('solution.py').read() + '\n\n' + PRE, ns)
    return ns

def test_check_1():
    ns = _ns()
    got = eval('(lambda r: r[0] <= 3 <= r[1] and r[0] < r[1])(bootstrap_ci([1, 2, 3, 4, 5], 500, 0))', ns)
    assert _close(got, eval('True', ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('(lambda r: 30 < r[0] < r[1] < 50)(bootstrap_ci([35, 38, 41, 44, 39, 42, 37, 40], 500, 1))', ns)
    assert _close(got, eval('True', ns)), repr(got)

def test_same_seed_same_interval_whatever_the_global_state():
    import random
    ns = _ns()
    f = ns["bootstrap_ci"]
    xs = [35, 38, 41, 44, 39, 42, 37, 40]
    random.seed(111)
    a = f(xs, 300, 7)
    random.seed(222)
    b = f(xs, 300, 7)
    assert _close(a, b), (a, b)
    assert len(a) == 2 and a[0] <= a[1]

def test_interval_is_a_95_percent_interval_of_the_bootstrap_means():
    ns = _ns()
    f = ns["bootstrap_ci"]
    xs = list(range(1, 101))  # mean 50.5, standard error of the mean about 2.89, so 95% is about 11.3 wide
    for seed in range(5):
        lo, hi = f(xs, 2000, seed)
        assert lo < 50.5 < hi
        assert 10.4 < hi - lo < 12.1, (seed, lo, hi)

def test_interval_follows_the_skew_of_the_resampled_means():
    # two big values among zeros: the percentile interval reaches much further above the mean than below
    ns = _ns()
    f = ns["bootstrap_ci"]
    xs = [0] * 18 + [10, 60]
    m = sum(xs) / len(xs)
    for seed in range(3):
        lo, hi = f(xs, 2000, seed)
        assert lo < m < hi
        assert (hi - m) > 1.4 * (m - lo), (seed, lo, hi)
