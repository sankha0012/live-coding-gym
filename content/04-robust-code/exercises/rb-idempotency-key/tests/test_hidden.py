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
