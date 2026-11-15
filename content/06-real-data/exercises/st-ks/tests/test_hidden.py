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
    got = eval('ks([0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9])', ns)
    assert _close(got, eval('1.0', ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('round(ks([0, 1, 0, 1], [0.1, 0.2, 0.3, 0.4]), 4)', ns)
    assert _close(got, eval('0.5', ns)), repr(got)

def test_unequal_group_sizes_use_shares_not_counts():
    ns = _ns()
    f = ns["ks"]
    # 8 goods fully below 2 bads: the gap is 1.0 (a raw count gap would be 8)
    y = [0] * 8 + [1] * 2
    s = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]
    assert _close(f(y, s), 1.0)
    # goods 1,2,3,4 against bads 3,5 (shuffled): gaps .25 .5 .25 .5 0
    assert _close(f([0, 1, 0, 1, 0, 0], [3, 5, 1, 3, 4, 2]), 0.5)

def test_gap_is_absolute_when_bads_score_lower():
    ns = _ns()
    assert _close(ns["ks"]([1, 1, 0, 0], [0.1, 0.2, 0.8, 0.9]), 1.0)

def test_tied_scores_are_evaluated_together():
    ns = _ns()
    f = ns["ks"]
    assert _close(f([0, 0, 1, 1], [0.5, 0.5, 0.5, 0.5]), 0.0)
    # goods .2 .5 .5, bads .5 .9: at 0.5 goods 3/3 vs bads 1/2
    assert _close(f([0, 0, 0, 1, 1], [0.2, 0.5, 0.5, 0.5, 0.9]), 0.5)
