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
    got = eval('round(psi([0.5, 0.5], [0.5, 0.5]), 4)', ns)
    assert _close(got, eval('0.0', ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('round(psi([0.25, 0.25, 0.5], [0.2, 0.3, 0.5]), 4)', ns)
    assert _close(got, eval('0.0203', ns)), repr(got)

def test_check_3():
    ns = _ns()
    got = eval('psi([0.5, 0.5], [1.0, 0.0]) > 0.25', ns)
    assert _close(got, eval('True', ns)), repr(got)

def test_zero_bin_is_clamped_not_skipped():
    ns = _ns()
    assert _close(eval('round(psi([0.5, 0.5], [1.0, 0.0]), 3)', ns), 4.604)
    assert _close(eval('round(psi([0.0, 1.0], [0.5, 0.5]), 3)', ns), 4.604)

def test_unequal_shift():
    ns = _ns()
    assert _close(eval('round(psi([0.4, 0.6], [0.1, 0.9]), 4)', ns), 0.5375)
