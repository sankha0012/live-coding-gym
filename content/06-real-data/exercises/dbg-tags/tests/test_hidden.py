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
    got = eval("(lambda: (add_tag({}, 'x'), add_tag({}, 'y'))[1])()", ns)
    assert _close(got, eval("['y']", ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('top_restaurants({10: 2, 20: 2, 30: 1}, 2)', ns)
    assert _close(got, eval('[10, 20]', ns)), repr(got)
