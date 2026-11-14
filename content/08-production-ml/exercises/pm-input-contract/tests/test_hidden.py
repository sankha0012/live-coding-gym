import copy
from solution import validate_request

CONTRACT = {
    "user_id": {"type": str, "required": True},
    "age": {"type": int, "required": True, "min": 0, "max": 120},
    "score": {"type": float, "min": 0.0, "max": 1.0},
}


def test_happy_path_drops_unknown_and_converts_int_to_float():
    clean, bad = validate_request({"user_id": "u1", "age": 30, "score": 1, "extra": 5}, CONTRACT)
    assert bad == []
    assert clean == {"user_id": "u1", "age": 30, "score": 1.0}
    assert isinstance(clean["score"], float)


def test_missing_required_and_optional():
    clean, bad = validate_request({"age": None}, CONTRACT)
    assert bad == ["missing:user_id", "missing:age"]
    assert clean == {}
    clean, bad = validate_request({"user_id": "u", "age": 1}, CONTRACT)
    assert bad == [] and clean == {"user_id": "u", "age": 1}


def test_bad_type_and_bool_is_not_a_number():
    clean, bad = validate_request({"user_id": 7, "age": True, "score": "0.5"}, CONTRACT)
    assert bad == ["bad_type:user_id", "bad_type:age", "bad_type:score"]
    assert clean == {}
    _, bad = validate_request({"user_id": "u", "age": 3.0}, CONTRACT)
    assert bad == ["bad_type:age"]


def test_range_is_inclusive_and_nan_fails():
    clean, bad = validate_request({"user_id": "u", "age": 120, "score": 0.0}, CONTRACT)
    assert bad == [] and clean["age"] == 120
    _, bad = validate_request({"user_id": "u", "age": 121, "score": float("nan")}, CONTRACT)
    assert bad == ["out_of_range:age", "out_of_range:score"]
    _, bad = validate_request({"user_id": "u", "age": -1, "score": 1.01}, CONTRACT)
    assert bad == ["out_of_range:age", "out_of_range:score"]


def test_reports_all_problems_and_keeps_good_fields():
    clean, bad = validate_request({"user_id": "u", "age": 500, "score": 0.3}, CONTRACT)
    assert bad == ["out_of_range:age"]
    assert clean == {"user_id": "u", "score": 0.3}


def test_empty_request_and_inputs_not_mutated():
    req = {"user_id": "u", "age": 1, "x": 1}
    before = copy.deepcopy(req)
    validate_request(req, CONTRACT)
    assert req == before
    assert validate_request({}, {}) == ({}, [])


def test_zero_and_empty_string_are_values_not_missing():
    clean, bad = validate_request({"user_id": "", "age": 0, "score": 0}, CONTRACT)
    assert bad == []
    assert clean == {"user_id": "", "age": 0, "score": 0.0}
    _, bad = validate_request({"user_id": "u", "age": "5"}, CONTRACT)
    assert bad == ["bad_type:age"]
