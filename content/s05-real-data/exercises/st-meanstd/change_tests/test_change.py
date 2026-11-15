import statistics


def _ns():
    ns = {'__name__': '__main__'}
    exec(open('solution.py').read(), ns)
    return ns


def _close(a, b):
    return abs(a - b) <= 1e-9 + 1e-9 * abs(b)


def test_population_std():
    f = _ns()["mean_std"]
    m, sd = f([2, 4, 4, 4, 5, 5, 7, 9], ddof=0)
    assert _close(m, 5.0) and _close(sd, 2.0)


def test_ddof_matches_statistics_module():
    f = _ns()["mean_std"]
    for xs in ([1, 2, 4], [3, 5], [-2.5, 0.5, 7.25, 1.0], [10.0, 10.0, 10.0]):
        m, sd = f(xs, ddof=0)
        assert _close(m, statistics.mean(xs)), xs
        assert _close(sd, statistics.pstdev(xs)), xs
        m, sd = f(xs, ddof=1)
        assert _close(sd, statistics.stdev(xs)), xs


def test_single_value_with_ddof_zero_and_default():
    f = _ns()["mean_std"]
    assert f([7], ddof=0) == (7.0, 0.0)
    m, sd = f([2, 4, 4, 4, 5, 5, 7, 9])
    assert _close(sd, statistics.stdev([2, 4, 4, 4, 5, 5, 7, 9]))
