import json

from gym import reviewer

RUBRIC = ["Correct", "Readable"]
GOOD = json.dumps({"scores": [5, 3], "verdict": "Solid", "feedback": "Name things better."})


def test_done_review_maps_scores_to_criteria():
    r = reviewer.review("code", RUBRIC, {"code": "x = 1"}, call=lambda p: GOOD)
    assert r == {"status": "done", "scores": {"Correct": 5, "Readable": 3},
                 "verdict": "Solid", "feedback": "Name things better."}


def test_prompt_carries_rubric_and_material():
    seen = []
    reviewer.review("code", RUBRIC, {"code": "x = 1"}, call=lambda p: seen.append(p) or GOOD)
    assert "Return exactly 2 scores" in seen[0]
    assert "- Correct" in seen[0] and "x = 1" in seen[0]


def test_default_rubric_used_when_none_given():
    n = len(reviewer.DEFAULT_RUBRICS["explain"])
    reply = json.dumps({"scores": [4] * n, "verdict": "v", "feedback": "f"})
    r = reviewer.review("explain", None, {"answer": "a"}, call=lambda p: reply)
    assert list(r["scores"]) == reviewer.DEFAULT_RUBRICS["explain"]


def test_malformed_reply_is_retried_once_then_pending():
    calls = []

    def bad(prompt):
        calls.append(1)
        return "not json"

    r = reviewer.review("code", RUBRIC, {"code": "x"}, call=bad)
    assert len(calls) == 2
    assert r["status"] == "pending" and r["scores"] == {}
    assert "Review unavailable" in r["feedback"]


def test_wrong_score_count_or_range_is_rejected():
    short = json.dumps({"scores": [5], "verdict": "v", "feedback": "f"})
    high = json.dumps({"scores": [5, 9], "verdict": "v", "feedback": "f"})
    assert reviewer.review("code", RUBRIC, {}, call=lambda p: short)["status"] == "pending"
    assert reviewer.review("code", RUBRIC, {}, call=lambda p: high)["status"] == "pending"


def test_network_error_becomes_pending():
    def down(prompt):
        raise OSError("no network")

    assert reviewer.review("code", RUBRIC, {}, call=down)["status"] == "pending"


def test_followups_returns_three_questions():
    reply = json.dumps({"questions": ["a?", "b?", "c?", "d?"]})
    assert reviewer.followups("task", "code", call=lambda p: reply) == ["a?", "b?", "c?"]


def test_followups_falls_back_when_gemini_fails():
    qs = reviewer.followups("task", "code", call=lambda p: "garbage")
    assert qs == reviewer.FALLBACK_QUESTIONS and len(qs) == 3
