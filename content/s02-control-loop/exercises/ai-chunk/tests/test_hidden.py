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
    got = eval("chunk_words('a b c d e', 2, 1)", ns)
    assert _close(got, eval("['a b', 'b c', 'c d', 'd e']", ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval("chunk_words('a b c d e', 3, 1)", ns)
    assert _close(got, eval("['a b c', 'c d e']", ns)), repr(got)

def test_check_3():
    ns = _ns()
    got = eval("chunk_words('', 3, 1)", ns)
    assert _close(got, eval('[]', ns)), repr(got)

def test_check_4():
    ns = _ns()
    got = eval("chunk_words('a b', 5, 2)", ns)
    assert _close(got, eval("['a b']", ns)), repr(got)


def test_partial_last_chunk_is_kept():
    f = _ns()["chunk_words"]
    assert f("a b c d e f", 4, 1) == ["a b c d", "d e f"]


def test_zero_overlap():
    f = _ns()["chunk_words"]
    assert f("a b c d e", 2, 0) == ["a b", "c d", "e"]
    assert f("a b c d", 2, 0) == ["a b", "c d"]


def test_words_split_on_any_whitespace():
    f = _ns()["chunk_words"]
    assert f("a  b\nc   d e", 3, 1) == ["a b c", "c d e"]
    assert f("   \n ", 3, 1) == []
