import pytest

from solution import IdempotentRunner


def test_runs_once_per_key():
    calls = []

    def f(p):
        calls.append(p)
        return p * 2

    r = IdempotentRunner(f)
    assert r.run("a", 1) == 2
    assert r.run("a", 99) == 2
    assert r.run("b", 5) == 10
    assert calls == [1, 5]


def test_none_result_is_stored():
    calls = []
    r = IdempotentRunner(lambda p: calls.append(p))
    assert r.run("k", 1) is None
    assert r.run("k", 2) is None
    assert calls == [1]


def test_failure_is_remembered():
    calls = []
    err = ValueError("card declined")

    def f(p):
        calls.append(p)
        raise err

    r = IdempotentRunner(f)
    with pytest.raises(ValueError) as first:
        r.run("k", 1)
    with pytest.raises(ValueError) as second:
        r.run("k", 2)
    assert first.value is err and second.value is err
    assert calls == [1]


def test_other_key_still_works_after_failure():
    def f(p):
        if p == "bad":
            raise RuntimeError("x")
        return p

    r = IdempotentRunner(f)
    with pytest.raises(RuntimeError):
        r.run("k1", "bad")
    assert r.run("k2", "ok") == "ok"


def test_key_not_payload_identifies_request():
    r = IdempotentRunner(lambda p: p)
    assert r.run(("user", 1), "first") == "first"
    assert r.run(("user", 1), "second") == "first"
    assert r.run(("user", 2), "second") == "second"


def test_falsy_results_are_stored():
    for value in (0, "", [], False, 0.0):
        calls = []

        def f(p, value=value):
            calls.append(p)
            return value

        r = IdempotentRunner(f)
        assert r.run("k", 1) == value
        assert r.run("k", 2) == value
        assert calls == [1], value


def test_falsy_keys_are_valid_keys():
    calls = []
    r = IdempotentRunner(lambda p: calls.append(p) or p)
    for key in (0, "", None, ()):
        assert r.run(key, "first") == "first"
        assert r.run(key, "second") == "first"
    assert calls == ["first"] * 4


def test_runners_do_not_share_state():
    calls1, calls2 = [], []
    r1 = IdempotentRunner(lambda p: calls1.append(p) or "one")
    r2 = IdempotentRunner(lambda p: calls2.append(p) or "two")
    assert r1.run("k", 1) == "one"
    assert r2.run("k", 2) == "two"
    assert calls1 == [1] and calls2 == [2]
    assert r1.run("k", 3) == "one" and r2.run("k", 4) == "two"


def test_repeat_after_failure_ignores_new_payload_and_does_not_call():
    calls = []

    def f(p):
        calls.append(p)
        if p == "bad":
            raise KeyError("bad")
        return p

    r = IdempotentRunner(f)
    for _ in range(3):
        with pytest.raises(KeyError):
            r.run("k", "bad")
    with pytest.raises(KeyError):
        r.run("k", "good")
    assert calls == ["bad"]
