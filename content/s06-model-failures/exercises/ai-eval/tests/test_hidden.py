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
    got = eval("score(['Yes', 'no ', ' maybe'], ['yes', 'No', 'no'], ['a', 'a', 'b'])", ns)
    assert _close(got, eval("{'overall': 2 / 3, 'a': 1.0, 'b': 0.0}", ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('score([], [], [])', ns)
    assert _close(got, eval("{'overall': 0.0}", ns)), repr(got)

def test_gold_is_normalised_too():
    ns = _ns()
    got = eval("score(['yes', 'no'], [' Yes ', 'NO'], ['a', 'b'])", ns)
    assert _close(got, eval("{'overall': 1.0, 'a': 1.0, 'b': 1.0}", ns)), repr(got)

def test_overall_is_pooled_not_mean_of_categories():
    ns = _ns()
    got = eval("score(['x', 'x', 'x', 'q'], ['x', 'x', 'x', 'y'], ['big', 'big', 'big', 'small'])", ns)
    assert _close(got, eval("{'overall': 0.75, 'big': 1.0, 'small': 0.0}", ns)), repr(got)
