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
