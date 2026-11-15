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
    got = eval("top_k([1, 0], {'a': [1, 0], 'b': [0, 1], 'c': [1, 1]}, 2)", ns)
    assert _close(got, eval("['a', 'c']", ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval("top_k([1, 1], {'x': [0, 0], 'y': [2, 2]}, 5)", ns)
    assert _close(got, eval("['y']", ns)), repr(got)

def test_check_3():
    ns = _ns()
    got = eval('top_k([0, 1], {}, 3)', ns)
    assert _close(got, eval('[]', ns)), repr(got)


def test_ties_broken_by_id():
    f = _ns()["top_k"]
    docs = {"b": [2, 0], "c": [0, 1], "a": [1, 0], "d": [3, 0]}
    assert f([1, 0], docs, 3) == ["a", "b", "d"]
    assert f([1, 0], docs, 1) == ["a"]


def test_cosine_not_dot_or_distance():
    f = _ns()["top_k"]
    docs = {"far": [5, 0], "mid": [2, 1], "big": [10, 10], "tiny": [0.1, 0.3]}
    assert f([1, 0], docs, 4) == ["far", "mid", "big", "tiny"]
    assert f([1, 0], docs, 2) == ["far", "mid"]
