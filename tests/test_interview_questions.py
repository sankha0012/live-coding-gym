import json

import pytest

from gym import interview


def reply(n):
    return json.dumps({"questions": [{"q": f"Question {i}?", "strong": f"Notes {i}."} for i in range(n)]})


def test_make_questions_parses_and_numbers_the_code():
    seen = []
    qs = interview.make_questions(lambda p: seen.append(p) or reply(3), "Sum a list.", "a = 1\nb = 2", "robust code", 3, reference="SECRET")
    assert qs == [{"q": f"Question {i}?", "ref": f"Notes {i}."} for i in range(3)]
    assert "1: a = 1" in seen[0] and "2: b = 2" in seen[0] and "Sum a list." in seen[0] and "robust code" in seen[0] and "SECRET" in seen[0]


def test_two_questions_drop_the_production_one():
    seen = []
    interview.make_questions(lambda p: seen.append(p) or reply(2), "t", "c", "f", 2)
    assert "Production" not in seen[0] and "Design choice" in seen[0]


def test_retry_prompt_lists_questions_to_avoid():
    seen = []
    interview.make_questions(lambda p: seen.append(p) or reply(2), "t", "c", "f", 2, avoid=["Why a set?"])
    assert "Why a set?" in seen[0]


def test_bad_json_or_wrong_count_retries_once_then_raises():
    calls = []
    answers = iter(["garbage", reply(2)])  # the second try has the wrong count too: 2 asked for 3
    with pytest.raises(RuntimeError):
        interview.make_questions(lambda p: calls.append(p) or next(answers), "t", "c", "f", 3)
    assert len(calls) == 2
    good = iter(["garbage", reply(3)])
    assert len(interview.make_questions(lambda p: next(good), "t", "c", "f", 3)) == 3


def test_new_state_keeps_the_reference_per_question():
    state = interview.new_state([{"q": "A?", "ref": "r"}, "B?"])
    assert [(q["q"], q.get("ref", "")) for q in state["qs"]] == [("A?", "r"), ("B?", "")]
