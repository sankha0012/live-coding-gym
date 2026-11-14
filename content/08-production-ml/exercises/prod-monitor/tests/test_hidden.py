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
    got = eval('check_batch([10, 11, 9, 10], 10, 2)', ns)
    assert _close(got, eval('[]', ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('check_batch([10, None, 11, None], 10, 2)', ns)
    assert _close(got, eval("['null_rate']", ns)), repr(got)

def test_check_3():
    ns = _ns()
    got = eval('check_batch([20] * 25, 10, 2)', ns)
    assert _close(got, eval("['mean_shift']", ns)), repr(got)

def test_check_4():
    ns = _ns()
    got = eval('check_batch([], 10, 2)', ns)
    assert _close(got, eval("['empty']", ns)), repr(got)

def test_check_5():
    ns = _ns()
    got = eval("check_batch([None, float('nan')], 10, 2)", ns)
    assert _close(got, eval("['null_rate']", ns)), repr(got)

def test_check_6():
    ns = _ns()
    got = eval('check_batch([20] * 10 + [None] * 5, 10, 2)', ns)
    assert _close(got, eval("['mean_shift', 'null_rate']", ns)), repr(got)
