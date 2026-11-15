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
    got = eval('new_or_returning([3, 1, 3, 2, 1])', ns)
    assert _close(got, eval("['new', 'new', 'returning', 'new', 'returning']", ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('new_or_returning([])', ns)
    assert _close(got, eval('[]', ns)), repr(got)

def test_repeated_customer_stays_returning():
    ns = _ns()
    got = ns['new_or_returning']([1, 1, 1, 2, 1])
    assert got == ['new', 'returning', 'returning', 'new', 'returning'], repr(got)
