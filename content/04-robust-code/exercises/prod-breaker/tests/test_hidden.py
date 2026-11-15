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

PRE = 'class Clock:\n    def __init__(self):\n        self.t = 0\n    def __call__(self):\n        return self.t\n\ndef _scenario():\n    clk, calls = Clock(), []\n    def bad():\n        calls.append("bad")\n        raise RuntimeError("down")\n    def good():\n        calls.append("good")\n        return "model"\n    cb = CircuitBreaker(max_failures=2, cooldown=30, clock=clk)\n    out = [cb.call(bad, "fb"), cb.call(bad, "fb"), cb.call(good, "fb")]\n    clk.t = 31\n    out.append(cb.call(good, "fb"))\n    out.append(cb.call(bad, "fb"))\n    return out, calls\n\ndef _scenario2():\n    clk, n = Clock(), []\n    def bad():\n        n.append(1)\n        raise RuntimeError("down")\n    cb = CircuitBreaker(max_failures=1, cooldown=10, clock=clk)\n    cb.call(bad, 0)\n    clk.t = 11\n    cb.call(bad, 0)\n    clk.t = 15\n    cb.call(bad, 0)\n    return len(n)'

def _ns():
    ns = {'__name__': '__main__'}
    exec(open('solution.py').read() + '\n\n' + PRE, ns)
    return ns

def test_check_1():
    ns = _ns()
    got = eval('_scenario()', ns)
    assert _close(got, eval("(['fb', 'fb', 'fb', 'model', 'fb'], ['bad', 'bad', 'good', 'bad'])", ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('_scenario2()', ns)
    assert _close(got, eval('2', ns)), repr(got)


def _mk(ns, max_failures, cooldown):
    class Clk:
        t = 0
        def __call__(self):
            return self.t
    clk, calls = Clk(), []
    def bad():
        calls.append("bad")
        raise RuntimeError("down")
    def good():
        calls.append("good")
        return "model"
    return ns['CircuitBreaker'](max_failures=max_failures, cooldown=cooldown, clock=clk), clk, calls, bad, good


def test_failed_trial_restarts_full_cooldown():
    ns = _ns()
    cb, clk, calls, bad, good = _mk(ns, 3, 30)
    for _ in range(3):
        assert cb.call(bad, "fb") == "fb"
    assert calls == ["bad"] * 3
    clk.t = 31
    assert cb.call(bad, "fb") == "fb"          # trial fails -> reopen at t=31
    assert len(calls) == 4
    assert cb.call(good, "fb") == "fb"         # still open, fn not called
    clk.t = 60
    assert cb.call(good, "fb") == "fb"         # only 29s since reopen
    assert len(calls) == 4
    clk.t = 61
    assert cb.call(good, "fb") == "model"      # 30s elapsed: trial allowed
    assert cb.call(good, "fb") == "model" and len(calls) == 6


def test_success_resets_failure_count():
    ns = _ns()
    cb, clk, calls, bad, good = _mk(ns, 3, 30)
    cb.call(bad, "fb"); cb.call(bad, "fb")
    assert cb.call(good, "fb") == "model"
    cb.call(bad, "fb"); cb.call(bad, "fb")
    assert cb.call(good, "fb") == "model"      # only 2 failures since success: still closed
    assert calls == ["bad", "bad", "good", "bad", "bad", "good"]


def test_cooldown_boundary_and_exact_threshold():
    ns = _ns()
    cb, clk, calls, bad, good = _mk(ns, 3, 30)
    cb.call(bad, "fb"); cb.call(bad, "fb")
    assert cb.call(good, "fb") == "model"      # 2 failures < 3: closed
    for _ in range(3):
        cb.call(bad, "fb")
    clk.t = 29
    assert cb.call(good, "fb") == "fb"         # 29 < 30: still open
    clk.t = 30
    assert cb.call(good, "fb") == "model"      # exactly cooldown seconds: trial allowed
