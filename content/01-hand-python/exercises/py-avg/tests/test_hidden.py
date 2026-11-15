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
    got = eval('avg_by_customer([(1, 10), (1, None), (1, 20), (2, None)])', ns)
    assert _close(got, eval('{1: 15.0, 2: None}', ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('avg_by_customer([])', ns)
    assert _close(got, eval('{}', ns)), repr(got)

def test_true_division_and_plain_mean():
    ns = _ns()
    got = ns['avg_by_customer']([(1, 1), (1, 2), (1, 4)])
    assert abs(got[1] - 7 / 3) < 1e-9, repr(got)

def test_zero_is_a_value_not_missing():
    ns = _ns()
    got = ns['avg_by_customer']([(1, 0), (1, 10), (2, 0), (3, None)])
    assert got == {1: 5.0, 2: 0.0, 3: None}, repr(got)
