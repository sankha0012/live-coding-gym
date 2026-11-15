from solution import validate_request

RULES = {
    "plan": {"type": str, "required": True, "choices": ["free", "pro"]},
    "level": {"type": int, "choices": [1, 2, 3]},
    "tag": {"type": str},
}


def test_value_in_choices_passes():
    assert validate_request({"plan": "pro", "level": 2}, RULES) == ({"plan": "pro", "level": 2}, [])


def test_value_not_in_choices_is_bad_choice():
    clean, bad = validate_request({"plan": "gold", "level": 9, "tag": "x"}, RULES)
    assert bad == ["bad_choice:plan", "bad_choice:level"]
    assert clean == {"tag": "x"}


def test_type_checked_before_choices():
    clean, bad = validate_request({"plan": 3, "level": "1"}, RULES)
    assert bad == ["bad_type:plan", "bad_type:level"]
    assert clean == {}


def test_missing_fields_skip_choices():
    clean, bad = validate_request({}, RULES)
    assert bad == ["missing:plan"]
    clean, bad = validate_request({"plan": "free", "level": None}, RULES)
    assert bad == [] and clean == {"plan": "free"}


def test_choices_and_range_together_and_float_choices():
    rules = {"n": {"type": int, "choices": [1, 5, 50], "max": 10}, "f": {"type": float, "choices": [0.5, 1.0]}}
    clean, bad = validate_request({"n": 50, "f": 1}, rules)
    assert bad == ["out_of_range:n"]
    assert clean == {"f": 1.0}
    _, bad = validate_request({"n": 2, "f": 0.25}, rules)
    assert bad == ["bad_choice:n", "bad_choice:f"]


def test_rules_without_choices_unchanged():
    clean, bad = validate_request({"tag": "anything"}, {"tag": {"type": str}})
    assert bad == [] and clean == {"tag": "anything"}
