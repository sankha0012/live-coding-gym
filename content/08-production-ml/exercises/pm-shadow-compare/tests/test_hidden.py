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


def test_diff_is_absolute_and_ranking_uses_it():
    scores = {"a": (0.5, 1.5), "b": (0.5, 0.0), "c": (0.5, 0.9)}
    out = compare_shadow(lambda x: scores[x][0], lambda x: scores[x][1], ["b", "c", "a"], tolerance=0.1, top=5)
    assert [w["input"] for w in out["worst"]] == ["a", "b", "c"]
    assert [w["diff"] for w in out["worst"]] == [1.0, 0.5, 0.4]
    assert out["worst"][0] == {"input": "a", "live": 0.5, "shadow": 1.5, "diff": 1.0}


def test_each_model_called_once_per_input():
    live_calls, shadow_calls = [], []

    def lv(x):
        live_calls.append(x)
        return 1.0

    def sh(x):
        shadow_calls.append(x)
        return 1.0

    compare_shadow(lv, sh, [1, 2, 3])
    assert live_calls == [1, 2, 3] and shadow_calls == [1, 2, 3]


def test_any_shadow_exception_is_counted_not_raised():
    def sh(x):
        raise [KeyError, ZeroDivisionError, ValueError][x]("boom")

    out = compare_shadow(lambda x: 0.0, sh, [0, 1, 2])
    assert out["shadow_errors"] == 3 and out["total"] == 3 and out["disagreements"] == 0


def test_worst_is_capped_by_top_and_default_is_three():
    out = compare_shadow(lambda x: 0.0, lambda x: x, [1, 2, 3, 4, 5])
    assert [w["input"] for w in out["worst"]] == [5, 4, 3]
    assert out["disagreements"] == 5
    assert compare_shadow(lambda x: 0.0, lambda x: x, [1, 2, 3], top=0)["worst"] == []


def test_rate_over_compared_with_mixed_errors():
    def sh(x):
        if x in (1, 2):
            raise RuntimeError
        return 1.0 if x == 3 else 0.0

    out = compare_shadow(lambda x: 0.0, sh, [1, 2, 3, 4])
    assert out["shadow_errors"] == 2 and out["disagreements"] == 1 and out["rate"] == 0.5
