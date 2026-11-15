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
    got = eval('auc([0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9])', ns)
    assert _close(got, eval('1.0', ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('auc([0, 1], [0.5, 0.5])', ns)
    assert _close(got, eval('0.5', ns)), repr(got)

def test_check_3():
    ns = _ns()
    got = eval('round(auc([0, 1, 0, 1, 1], [0.3, 0.6, 0.7, 0.8, 0.2]), 4)', ns)
    assert _close(got, eval('0.5', ns)), repr(got)

def test_ties_mixed_with_unequal_class_sizes_and_unsorted_input():
    ns = _ns()
    f = ns["auc"]
    # pos scores 0.2, 0.9; neg scores 0.2, 0.5: pairs give 0.5, 0, 1, 1 -> 2.5 / 4
    assert _close(f([0, 1, 1, 0], [0.2, 0.2, 0.9, 0.5]), 0.625)
    # 3 positives, 1 negative: only the 0.4 positive ties the negative -> (1 + 1 + 0.5) / 3
    assert _close(f([1, 0, 1, 1], [0.9, 0.4, 0.4, 0.8]), 2.5 / 3)
    assert _close(f([1, 1, 0, 0, 0], [0.1, 0.2, 0.3, 0.4, 0.5]), 0.0)
