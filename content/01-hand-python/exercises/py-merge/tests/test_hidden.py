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
    got = eval('merge_shifts([[9, 12], [11, 14], [16, 18]])', ns)
    assert _close(got, eval('[[9, 14], [16, 18]]', ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('merge_shifts([[1, 5], [2, 3]])', ns)
    assert _close(got, eval('[[1, 5]]', ns)), repr(got)

def test_check_3():
    ns = _ns()
    got = eval('merge_shifts([[5, 6], [1, 2]])', ns)
    assert _close(got, eval('[[1, 2], [5, 6]]', ns)), repr(got)

def test_check_4():
    ns = _ns()
    got = eval('merge_shifts([])', ns)
    assert _close(got, eval('[]', ns)), repr(got)

def test_touching_shifts_merge():
    ns = _ns()
    assert ns['merge_shifts']([[1, 2], [2, 3]]) == [[1, 3]]

def test_inner_shifts_after_a_long_one():
    ns = _ns()
    assert ns['merge_shifts']([[1, 10], [2, 3], [5, 6]]) == [[1, 10]]

def test_input_not_mutated():
    ns = _ns()
    shifts = [[5, 8], [1, 6], [20, 21]]
    got = ns['merge_shifts'](shifts)
    assert got == [[1, 8], [20, 21]]
    assert shifts == [[5, 8], [1, 6], [20, 21]]
