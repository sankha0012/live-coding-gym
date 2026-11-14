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
    got = eval("top_features({'b': -3, 'a': 3, 'c': 1})", ns)
    assert _close(got, eval("['a', 'b']", ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval("(lambda b: (normalize(b), b)[1])([{'amount': 5}, {'amount': 10}])", ns)
    assert _close(got, eval("[{'amount': 5}, {'amount': 10}]", ns)), repr(got)

def test_check_3():
    ns = _ns()
    got = eval("normalize([{'amount': 5}, {'amount': 10}])", ns)
    assert _close(got, eval("[{'amount': 0.0}, {'amount': 1.0}]", ns)), repr(got)

def test_check_4():
    ns = _ns()
    got = eval("normalize([{'amount': 7}, {'amount': 7}])", ns)
    assert _close(got, eval("[{'amount': 0.0}, {'amount': 0.0}]", ns)), repr(got)

def test_check_5():
    ns = _ns()
    got = eval('normalize([])', ns)
    assert _close(got, eval('[]', ns)), repr(got)

def test_check_6():
    ns = _ns()
    got = eval('mean_score([1, None, 3])', ns)
    assert _close(got, eval('2.0', ns)), repr(got)

def test_check_7():
    ns = _ns()
    got = eval('mean_score([None])', ns)
    assert _close(got, eval('None', ns)), repr(got)

def test_check_8():
    ns = _ns()
    got = eval('mean_score([])', ns)
    assert _close(got, eval('None', ns)), repr(got)
