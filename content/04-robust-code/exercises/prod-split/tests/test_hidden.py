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
    got = eval("assign_split('user_42')", ns)
    assert _close(got, eval("'test'", ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval("assign_split('user_42', 0)", ns)
    assert _close(got, eval("'train'", ns)), repr(got)

def test_check_3():
    ns = _ns()
    got = eval("assign_split(42) == assign_split('42')", ns)
    assert _close(got, eval('True', ns)), repr(got)

def test_check_4():
    ns = _ns()
    got = eval("abs(sum(assign_split('u%d' % i) == 'test' for i in range(2000)) / 2000 - 0.2) < 0.03", ns)
    assert _close(got, eval('True', ns)), repr(got)
