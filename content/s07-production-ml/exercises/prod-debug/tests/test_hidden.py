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

def test_top_features_respects_k():
    ns = _ns()
    assert _close(eval("top_features({'a': 1, 'b': -5, 'c': 3}, k=1)", ns), ['b'])
    assert _close(eval("top_features({'a': 1, 'b': -5, 'c': 3}, k=3)", ns), ['b', 'c', 'a'])

def test_top_features_tie_by_name_and_input_untouched():
    ns = _ns()
    got = eval("(lambda w: (top_features(w, 3), w))({'z': 2, 'y': -2, 'x': 2, 'q': 9})", ns)
    assert got[0] == ['q', 'x', 'y'], got
    assert got[1] == {'z': 2, 'y': -2, 'x': 2, 'q': 9}

def test_normalize_keeps_other_keys_and_scales_negative():
    ns = _ns()
    got = eval("normalize([{'id': 'a', 'amount': -2}, {'id': 'b', 'amount': 4}, {'id': 'c', 'amount': 1}])", ns)
    assert _close(got, [{'id': 'a', 'amount': 0.0}, {'id': 'b', 'amount': 1.0}, {'id': 'c', 'amount': 0.5}]), repr(got)

def test_normalize_constant_keeps_other_keys():
    ns = _ns()
    got = eval("normalize([{'id': 1, 'amount': 7}, {'id': 2, 'amount': 7}])", ns)
    assert _close(got, [{'id': 1, 'amount': 0.0}, {'id': 2, 'amount': 0.0}]), repr(got)

def test_mean_score_counts_zero():
    ns = _ns()
    assert _close(eval('mean_score([0, 2, None])', ns), 1.0)
    assert eval('mean_score([0])', ns) == 0.0
    assert eval('mean_score([0, None])', ns) == 0.0
