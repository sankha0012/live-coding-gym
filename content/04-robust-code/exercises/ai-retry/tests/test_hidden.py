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
