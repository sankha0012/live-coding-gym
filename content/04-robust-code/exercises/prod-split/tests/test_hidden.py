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


def test_bucket_boundary_is_strict():
    # md5 bucket of 'u1' is 4, of 'user_42' is 12, of 'a' is 97
    ns = _ns()
    f = ns['assign_split']
    assert f('u1', 4) == 'train' and f('u1', 5) == 'test'
    assert f('user_42', 12) == 'train' and f('user_42', 13) == 'test'
    assert f('a', 97) == 'train' and f('a', 98) == 'test'
    assert f('a') == 'train' and f('u1') == 'test'


def test_extremes_and_exact_buckets():
    ns = _ns()
    f = ns['assign_split']
    users = ['u%d' % i for i in range(40)]
    assert all(f(u, 0) == 'train' for u in users)
    assert all(f(u, 100) == 'test' for u in users)
    got50 = ''.join('T' if f(u, 50) == 'test' else 'r' for u in users)
    assert got50 == 'TTTTrTrrrrTrrTrrrrrTTrTrTrTTTTrrTrTTrrTT'
    got20 = ''.join('T' if f(u) == 'test' else 'r' for u in users)
    assert got20 == 'rTrTrTrrrrTrrrrrrrrTTrrrrrTTrrrrrrrTrrTr'
    assert f(7) == f('7') and f(7, 56) == 'test' and f(7, 55) == 'train'
