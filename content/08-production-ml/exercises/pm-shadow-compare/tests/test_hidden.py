import pytest
from solution import compare_shadow


def live(x):
    return {"a": 0.5, "b": 0.5, "c": 0.5, "d": 0.5, "e": 0.5}[x]


def shadow(x):
    return {"a": 0.5, "b": 0.75, "c": 0.0, "d": 1.0, "e": 0.625}[x]


def test_rate_and_worst_order():
    out = compare_shadow(live, shadow, list("abcde"), tolerance=0.25, top=1)
    assert out["total"] == 5
    assert out["disagreements"] == 2
    assert out["rate"] == 2 / 5
    assert out["shadow_errors"] == 0
    assert [w["input"] for w in out["worst"]] == ["c"]
    out = compare_shadow(live, shadow, list("abcde"), tolerance=0.25, top=5)
    assert [w["input"] for w in out["worst"]] == ["c", "d"]
    assert out["worst"][0] == {"input": "c", "live": 0.5, "shadow": 0.0, "diff": 0.5}


def test_tolerance_boundary_is_not_disagreement():
    out = compare_shadow(live, shadow, ["b"], tolerance=0.25)
    assert out["disagreements"] == 0 and out["worst"] == []


def test_shadow_errors_are_excluded():
    def flaky(x):
        if x == "a":
            raise TimeoutError("shadow down")
        return 0.0

    out = compare_shadow(lambda x: 1.0, flaky, ["a", "b"], tolerance=0.1)
    assert out["total"] == 2 and out["shadow_errors"] == 1
    assert out["disagreements"] == 1 and out["rate"] == 1.0


def test_all_shadow_errors_gives_zero_rate():
    def broken(x):
        raise RuntimeError

    out = compare_shadow(lambda x: 1.0, broken, [1, 2, 3])
    assert out["rate"] == 0.0 and out["shadow_errors"] == 3 and out["worst"] == []


def test_empty_inputs():
    out = compare_shadow(live, shadow, [])
    assert out == {"total": 0, "shadow_errors": 0, "disagreements": 0, "rate": 0.0, "worst": []}


def test_ties_keep_input_order():
    out = compare_shadow(lambda x: 0.0, lambda x: 1.0, [3, 1, 2], top=5)
    assert [w["input"] for w in out["worst"]] == [3, 1, 2]


def test_live_error_propagates():
    def bad_live(x):
        raise ValueError("live down")

    with pytest.raises(ValueError):
        compare_shadow(bad_live, shadow, ["a"])
