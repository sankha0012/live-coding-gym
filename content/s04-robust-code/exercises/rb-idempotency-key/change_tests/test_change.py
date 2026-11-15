import pytest

from solution import IdempotentRunner


def test_forget_allows_a_new_call():
    calls = []
    r = IdempotentRunner(lambda p: calls.append(p) or p * 2)
    assert r.run("a", 1) == 2
    r.forget("a")
    assert r.run("a", 5) == 10
    assert r.run("a", 7) == 10
    assert calls == [1, 5]


def test_forget_clears_a_stored_failure():
    calls = []

    def f(p):
        calls.append(p)
        if p == "bad":
            raise ValueError("no")
        return p

    r = IdempotentRunner(f)
    with pytest.raises(ValueError):
        r.run("k", "bad")
    r.forget("k")
    assert r.run("k", "good") == "good"
    assert calls == ["bad", "good"]


def test_forget_unknown_key_is_harmless():
    r = IdempotentRunner(lambda p: p)
    r.forget("never-seen")
    assert r.run("never-seen", 3) == 3


def test_forget_leaves_other_keys_alone():
    calls = []
    r = IdempotentRunner(lambda p: calls.append(p) or p)
    r.run("a", 1)
    r.run("b", 2)
    r.forget("a")
    assert r.run("b", 99) == 2
    assert calls == [1, 2]


def test_forget_works_for_none_result_and_falsy_keys():
    calls = []
    r = IdempotentRunner(lambda p: calls.append(p))
    for key in (0, "", None):
        r.run(key, "x")
        r.forget(key)
        r.run(key, "y")
    assert calls == ["x", "y"] * 3
