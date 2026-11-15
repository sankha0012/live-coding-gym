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
    got = eval('tuple(round(v, 4) for v in mean_std([2, 4, 4, 4, 5, 5, 7, 9]))', ns)
    assert _close(got, eval('(5.0, 2.1381)', ns)), repr(got)

def test_non_integer_mean_and_other_shapes():
    import statistics
    ns = _ns()
    f = ns["mean_std"]
    for xs in ([1, 2, 4], [3, 5], [-2.5, 0.5, 7.25, 1.0], [10.0, 10.0, 10.0]):
        m, sd = f(xs)
        assert _close(m, statistics.mean(xs)), xs
        assert _close(sd, statistics.stdev(xs)), xs
