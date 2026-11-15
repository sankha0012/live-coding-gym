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
    got = eval('extract_json(\'Sure! ```json\\n{"intent": "refund", "confidence": 0.9}\\n``` Hope it helps\')', ns)
    assert _close(got, eval("{'intent': 'refund', 'confidence': 0.9}", ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval("extract_json('no json here')", ns)
    assert _close(got, eval('None', ns)), repr(got)

def test_check_3():
    ns = _ns()
    got = eval('extract_json(\'{"a": 1\')', ns)
    assert _close(got, eval('None', ns)), repr(got)

def test_check_4():
    ns = _ns()
    got = eval('extract_json(\'Result: {"a": {"b": 2}}\')', ns)
    assert _close(got, eval("{'a': {'b': 2}}", ns)), repr(got)


def test_braces_but_not_json():
    f = _ns()["extract_json"]
    assert f("see {not json} here") is None
    assert f("{'a': 1}") is None


def test_multiline_object_in_fence():
    f = _ns()["extract_json"]
    text = 'Here you go:\n```json\n{\n  "a": 1,\n  "b": {"c": [1, 2]}\n}\n```\nDone.'
    assert f(text) == {"a": 1, "b": {"c": [1, 2]}}


def test_plain_object_and_only_objects():
    f = _ns()["extract_json"]
    assert f('{"a": "}"}') == {"a": "}"}
    assert f("[1, 2, 3]") is None
    assert f("42") is None
