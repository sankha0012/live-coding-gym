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

PRE = 'class Flaky:\n    def __init__(self, fails):\n        self.fails, self.calls = fails, 0\n    def __call__(self):\n        self.calls += 1\n        if self.calls <= self.fails:\n            raise RuntimeError("timeout")\n        return "ok"\n\ndef _run(fails, tries):\n    waits = []\n    f = Flaky(fails)\n    try:\n        r = call_with_retry(f, max_tries=tries, base=1.0, sleep=waits.append)\n    except RuntimeError:\n        r = "raised"\n    return r, f.calls, waits'

def _ns():
    ns = {'__name__': '__main__'}
    exec(open('solution.py').read() + '\n\n' + PRE, ns)
    return ns

def test_check_1():
    ns = _ns()
    got = eval('_run(2, 3)', ns)
    assert _close(got, eval("('ok', 3, [1.0, 2.0])", ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('_run(3, 3)', ns)
    assert _close(got, eval("('raised', 3, [1.0, 2.0])", ns)), repr(got)

def test_check_3():
    ns = _ns()
    got = eval('_run(0, 3)', ns)
    assert _close(got, eval("('ok', 1, [])", ns)), repr(got)


def test_other_base_and_tries():
    ns = _ns()
    f = ns['call_with_retry']
    for tries, expect in [(5, [0.5, 1.0, 2.0, 4.0]), (1, []), (2, [0.5])]:
        waits, calls = [], []
        def boom():
            calls.append(1)
            raise RuntimeError("x")
        try:
            f(boom, max_tries=tries, base=0.5, sleep=waits.append)
            assert False, "should raise"
        except RuntimeError:
            pass
        assert len(calls) == tries and waits == expect, (tries, calls, waits)


def test_success_late_and_last_error_raised():
    ns = _ns()
    f = ns['call_with_retry']
    waits, n = [], []
    def flaky():
        n.append(1)
        if len(n) < 5:
            raise RuntimeError("fail %d" % len(n))
        return "ok"
    assert f(flaky, max_tries=5, base=2.0, sleep=waits.append) == "ok"
    assert len(n) == 5 and waits == [2.0, 4.0, 8.0, 16.0]
    n.clear()
    def bad():
        n.append(1)
        raise ValueError("err %d" % len(n))
    try:
        f(bad, max_tries=3, base=1.0, sleep=lambda s: None)
        assert False
    except ValueError as e:
        assert str(e) == "err 3"
