import json
import re

import pytest
from fastapi.testclient import TestClient

from gym.app import create_app
from tests.conftest import FIXTURES

PY_SOLUTION = (FIXTURES / "01-hand-python/exercises/count-words/solution.py").read_text()
SQL_SOLUTION = (FIXTURES / "03-hand-sql/exercises/top-customers/solution.sql").read_text()


def fake_gemini(prompt):
    if '"questions"' in prompt:
        return json.dumps({"questions": ["q1?", "q2?", "q3?"]})
    n = int(re.search(r"Return exactly (\d+) scores", prompt).group(1))
    return json.dumps({"scores": [4] * n, "verdict": "Good", "feedback": "Fine."})


@pytest.fixture
def client(tmp_path):
    return TestClient(create_app(FIXTURES, tmp_path / "p.db", call=fake_gemini))


def post(client, path, body=None):
    r = client.post(path, json=body or {})
    assert r.status_code == 200, r.text
    return r.json()


def test_journey_starts_locked_after_first_step(client):
    j = client.get("/api/journey").json()
    assert [s["unlocked"] for s in j["steps"]] == [True, False]
    assert j["readiness"] is None and j["due_cards"] == 1 and j["errors"] == []


def test_step_lists_lessons_and_exercises(client):
    s = client.get("/api/step/01-hand-python").json()
    assert s["lessons"][0]["title"] == "Counting with a dict"
    assert [e["id"] for e in s["exercises"]] == ["count-words", "explain-count-words"]
    assert client.get("/api/step/nope").status_code == 404


def test_exercise_payload_depends_on_mode(client):
    blank = client.get("/api/exercise/count-words").json()
    assert blank["modes"] == ["retype", "gaps", "blank", "timed"]
    assert blank["code"].endswith("pass\n") and blank["solution"] == ""
    retype = client.get("/api/exercise/count-words?mode=retype").json()
    assert "counts.get" in retype["solution"] and retype["code"] == ""
    gaps = client.get("/api/exercise/count-words?mode=gaps").json()
    assert "____" in gaps["code"]
    sql = client.get("/api/exercise/top-customers").json()
    assert sql["modes"] == ["retype", "blank", "timed"] and "CREATE TABLE" in sql["schema"]
    assert client.get("/api/exercise/explain-count-words").json()["modes"] == []


def test_run_does_not_record_an_attempt(client):
    r = post(client, "/api/run", {"exercise_id": "count-words", "code": "print('hi')"})
    assert r["output"].strip() == "hi"
    r = post(client, "/api/run", {"exercise_id": "top-customers", "code": "SELECT COUNT(*) FROM orders"})
    assert r["output"].splitlines()[-1] == "5"
    assert client.get("/api/exercise/count-words").json()["status"]["tests"] is False


def test_full_step_flow_passes_gate_and_unlocks_next(client):
    sub = post(client, "/api/submit", {"exercise_id": "count-words", "code": PY_SOLUTION,
                                       "mode": "timed", "duration_s": 120})
    assert sub["passed"] and sub["status"]["tests"] and sub["status"]["timed"]
    rev = post(client, "/api/review", {"exercise_id": "count-words", "attempt_id": sub["attempt_id"],
                                       "text": "I count with dict.get."})
    assert rev["status"] == "done" and min(rev["scores"].values()) == 4
    post(client, "/api/review", {"exercise_id": "explain-count-words", "text": "It splits and counts."})
    j = client.get("/api/journey").json()
    assert j["steps"][0]["passed"] and j["steps"][1]["unlocked"]
    assert client.get("/api/exercise/count-words").json()["review"]["verdict"] == "Good"


def test_failed_submission_is_recorded_but_not_passed(client):
    sub = post(client, "/api/submit", {"exercise_id": "count-words", "code": "def count_words(t): return {}",
                                       "mode": "blank", "duration_s": 5})
    assert not sub["passed"] and sub["status"]["tests"] is False


def test_sql_submit(client):
    sub = post(client, "/api/submit", {"exercise_id": "top-customers", "code": SQL_SOLUTION,
                                       "mode": "blank", "duration_s": 30})
    assert sub["passed"] and sub["status"]["done"]


def test_bad_requests(client):
    assert client.post("/api/submit", json={"exercise_id": "nope", "code": ""}).status_code == 404
    assert client.post("/api/submit", json={"exercise_id": "explain-count-words", "code": ""}).status_code == 400
    assert client.post("/api/review", json={"exercise_id": "count-words", "attempt_id": 999}).status_code == 404


def test_pending_review_can_be_retried(tmp_path):
    state = {"down": True}

    def flaky(prompt):
        if state["down"]:
            raise OSError("offline")
        return fake_gemini(prompt)

    client = TestClient(create_app(FIXTURES, tmp_path / "p.db", call=flaky))
    rev = post(client, "/api/review", {"exercise_id": "explain-count-words", "text": "answer"})
    assert rev["status"] == "pending"
    state["down"] = False
    again = post(client, f"/api/reviews/{rev['review_id']}/retry")
    assert again["status"] == "done" and again["review_id"] == rev["review_id"]


def test_cards_and_unlock(client):
    due = client.get("/api/cards/due").json()
    assert due[0]["id"] == "dict-count"
    assert post(client, "/api/cards/grade", {"card_id": "dict-count", "correct": True})["box"] == 1
    assert client.get("/api/cards/due").json() == []
    post(client, "/api/unlock", {"step_id": "03-hand-sql"})
    assert client.get("/api/journey").json()["steps"][1]["unlocked"]


def test_mock_round(client):
    start = post(client, "/api/mock/start")
    assert start["python"]["id"] == "count-words" and start["sql"]["id"] == "top-customers"
    mid = start["mock_id"]
    sub = post(client, f"/api/mock/{mid}/submit", {
        "python_code": PY_SOLUTION, "sql_code": SQL_SOLUTION,
        "prompt_text": "Write count_words with validation.", "duration_s": 600})
    assert sub["python"]["passed"] and sub["sql"]["passed"] and sub["questions"] == ["q1?", "q2?", "q3?"]
    done = post(client, f"/api/mock/{mid}/answers", {"answers": ["a", "b", "c"]})
    assert done["score"]["total"] == round(100 * (0.5 + 0.4 * 4 / 5 + 0.1))
    assert len(done["reviews"]) == 3 and done["readiness"] is None
    j = client.get("/api/journey").json()
    assert j["mocks"][0]["total"] == done["score"]["total"]
    assert client.post("/api/mock/999/submit", json={
        "python_code": "", "sql_code": "", "prompt_text": "", "duration_s": 0}).status_code == 404


def test_journey_next_up_points_to_first_unfinished_exercise(client):
    j = client.get("/api/journey").json()
    assert j["next"]["exercise_id"] == "count-words" and j["next"]["step_id"] == "01-hand-python"
    post(client, "/api/submit", {"exercise_id": "count-words", "code": PY_SOLUTION, "mode": "timed", "duration_s": 60})
    post(client, "/api/review", {"exercise_id": "count-words", "attempt_id": 1, "text": "x"})
    assert client.get("/api/journey").json()["next"]["exercise_id"] == "explain-count-words"


def test_exercise_payload_points_to_the_next_exercise(client):
    assert client.get("/api/exercise/count-words").json()["next"]["id"] == "explain-count-words"
    # last exercise of step 1 leads to the first exercise of the next step
    assert client.get("/api/exercise/explain-count-words").json()["next"]["id"] == "top-customers"
    assert client.get("/api/exercise/top-customers").json()["next"] is None


def test_responses_are_never_cached(client):
    assert client.get("/api/journey").headers["cache-control"] == "no-store"
    assert client.get("/app.js").headers["cache-control"] == "no-store"
