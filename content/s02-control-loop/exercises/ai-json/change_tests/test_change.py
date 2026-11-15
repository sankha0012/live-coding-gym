def _ns():
    ns = {"__name__": "__main__"}
    exec(open("solution.py").read(), ns)
    return ns


def test_missing_required_key_gives_none():
    f = _ns()["extract_json"]
    assert f('{"intent": "refund"}', ["intent", "confidence"]) is None
    assert f('Sure: {"a": 1}', ["b"]) is None


def test_all_required_keys_present():
    f = _ns()["extract_json"]
    text = 'Here: ```json\n{"intent": "refund", "confidence": 0.9}\n```'
    assert f(text, ["intent", "confidence"]) == {"intent": "refund", "confidence": 0.9}
    assert f('{"a": 1}', ["a"]) == {"a": 1}


def test_default_and_invalid_unchanged():
    f = _ns()["extract_json"]
    assert f('{"a": 1}') == {"a": 1}
    assert f("no json", ["a"]) is None
