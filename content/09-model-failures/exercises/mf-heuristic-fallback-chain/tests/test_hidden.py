from solution import predict_with_fallback


def boom(_):
    raise RuntimeError("model down")


def test_model_answers():
    assert predict_with_fallback({"x": 1}, lambda f: 0.9, lambda f: 0.5, 0.1) == (0.9, "model")


def test_exception_falls_to_rule():
    assert predict_with_fallback({}, boom, lambda f: 0.5, 0.1) == (0.5, "rule")


def test_none_falls_through():
    assert predict_with_fallback({}, lambda f: None, lambda f: None, 0.1) == (0.1, "default")


def test_both_fail_use_default():
    assert predict_with_fallback({}, boom, boom, 0.1) == (0.1, "default")


def test_zero_is_a_real_answer():
    assert predict_with_fallback({}, lambda f: 0.0, lambda f: 0.5, 0.1) == (0.0, "model")
    assert predict_with_fallback({}, boom, lambda f: 0, 0.1) == (0, "rule")


def test_later_stage_not_called_when_earlier_answers():
    calls = []

    def rule(f):
        calls.append(1)
        return 0.5

    predict_with_fallback({}, lambda f: 0.9, rule, 0.1)
    assert calls == []


def test_features_passed_through():
    seen = []
    predict_with_fallback({"a": 1}, lambda f: seen.append(f) or 0.3, lambda f: 0.5, 0.1)
    assert seen == [{"a": 1}]


def test_default_returned_as_is_even_none():
    assert predict_with_fallback({}, boom, lambda f: None, None) == (None, "default")


def test_any_exception_type_is_caught():
    def raiser(exc):
        def f(_):
            raise exc

        return f

    for exc in (KeyError("k"), ZeroDivisionError(), TypeError("t"), OSError("io")):
        assert predict_with_fallback({}, raiser(exc), lambda f: 0.5, 0.1) == (0.5, "rule")
        assert predict_with_fallback({}, raiser(exc), raiser(exc), 0.1) == (0.1, "default")


def test_rule_gets_the_features():
    seen = []
    assert predict_with_fallback({"a": 2}, lambda f: None, lambda f: seen.append(f) or 0.5, 0.1) == (0.5, "rule")
    assert seen == [{"a": 2}]
