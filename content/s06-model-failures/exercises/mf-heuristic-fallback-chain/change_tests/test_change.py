from solution import predict_with_fallback


def in_unit(v):
    return 0 <= v <= 1


def boom(_):
    raise RuntimeError("down")


def test_invalid_model_value_falls_to_rule():
    assert predict_with_fallback({}, lambda f: 1.7, lambda f: 0.4, 0.1, valid=in_unit) == (0.4, "rule")


def test_both_invalid_use_default():
    assert predict_with_fallback({}, lambda f: 1.7, lambda f: -2, 0.1, valid=in_unit) == (0.1, "default")


def test_valid_model_value_kept_and_rule_not_called():
    calls = []

    def rule(f):
        calls.append(1)
        return 0.4

    assert predict_with_fallback({}, lambda f: 0.0, rule, 0.1, valid=in_unit) == (0.0, "model")
    assert calls == []


def test_valid_not_applied_to_default():
    assert predict_with_fallback({}, boom, lambda f: 5, 9.9, valid=in_unit) == (9.9, "default")


def test_valid_not_called_for_none():
    seen = []

    def valid(v):
        seen.append(v)
        return True

    assert predict_with_fallback({}, lambda f: None, lambda f: 0.5, 0.1, valid=valid) == (0.5, "rule")
    assert seen == [0.5]


def test_valid_receives_the_value():
    seen = []

    def valid(v):
        seen.append(v)
        return True

    predict_with_fallback({}, lambda f: 0.3, lambda f: 0.5, 0.1, valid=valid)
    assert seen == [0.3]


def test_without_valid_unchanged():
    assert predict_with_fallback({}, lambda f: 1.7, lambda f: 0.4, 0.1) == (1.7, "model")
