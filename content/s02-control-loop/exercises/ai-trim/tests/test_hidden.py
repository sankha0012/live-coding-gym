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

PRE = 'MSGS = [("system", "be brief"), ("user", "hi there"), ("assistant", "hello how can I help"), ("user", "refund my order please")]'

def _ns():
    ns = {'__name__': '__main__'}
    exec(open('solution.py').read() + '\n\n' + PRE, ns)
    return ns

def test_check_1():
    ns = _ns()
    got = eval('trim_history(MSGS, 6)', ns)
    assert _close(got, eval("[('system', 'be brief'), ('user', 'refund my order please')]", ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('trim_history(MSGS, 11)', ns)
    assert _close(got, eval("[('system', 'be brief'), ('assistant', 'hello how can I help'), ('user', 'refund my order please')]", ns)), repr(got)

def test_check_3():
    ns = _ns()
    got = eval('trim_history(MSGS, 3)', ns)
    assert _close(got, eval("[('system', 'be brief')]", ns)), repr(got)


def test_stops_at_first_message_that_does_not_fit():
    ns = _ns()
    # the 5-word message does not fit, so the older 2-word one must not sneak back in
    got = ns["trim_history"](ns["MSGS"], 8)
    assert got == [("system", "be brief"), ("user", "refund my order please")]


def test_system_message_kept_even_over_budget():
    ns = _ns()
    assert ns["trim_history"](ns["MSGS"], 1) == [("system", "be brief")]


def test_no_system_message_and_empty():
    f = _ns()["trim_history"]
    assert f([], 5) == []
    msgs = [("user", "a b c"), ("assistant", "d e")]
    assert f(msgs, 4) == [("assistant", "d e")]
    assert f(msgs, 5) == msgs


def test_only_a_leading_system_message_is_special():
    f = _ns()["trim_history"]
    msgs = [("user", "a b"), ("system", "x y z"), ("user", "q")]
    assert f(msgs, 1) == [("user", "q")]


def test_input_not_modified():
    ns = _ns()
    before = list(ns["MSGS"])
    ns["trim_history"](ns["MSGS"], 6)
    assert ns["MSGS"] == before
