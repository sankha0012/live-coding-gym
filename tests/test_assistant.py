import json
import re

import pytest
from fastapi.testclient import TestClient

from gym import assistant
from gym.app import create_app

SECRET_SOLUTION = "return sorted(xs)  # SECRET-REFERENCE"
TESTS = "from solution import f\n\ndef test_a():\n    assert f([2, 1]) == [1, 2]\n"


def build(tmp_path):
    """Step 1 (tutor only) and step 4 (interview allowed), each with a python exercise, plus an explain exercise."""
    root = tmp_path / "c"
    layout = {
        "01-a/step.yaml": "title: A\norder: 1\n",
        "04-d/step.yaml": "title: D\norder: 4\n",
        "01-a/exercises/e1/exercise.yaml": "title: Sort it\nkind: python\n",
        "04-d/exercises/e4/exercise.yaml": "title: Sort again\nkind: python\n",
        "04-d/exercises/x4/exercise.yaml": "title: Explain\nkind: explain\n",
        "04-d/exercises/q4/exercise.yaml": "title: Quiz\nkind: quiz\n",
        "04-d/exercises/q4/quiz.yaml": "- q: Q\n  options: [a, b]\n  answer: 0\n",
    }
    for ex in ("e1", "e4"):
        step = "01-a" if ex == "e1" else "04-d"
        layout[f"{step}/exercises/{ex}/solution.py"] = f"def f(xs):\n    {SECRET_SOLUTION}\n"
        layout[f"{step}/exercises/{ex}/starter.py"] = "def f(xs):\n    pass\n"
        layout[f"{step}/exercises/{ex}/tests/test_hidden.py"] = TESTS
    for ex in ("e1", "e4", "x4", "q4"):
        step = "01-a" if ex == "e1" else "04-d"
        layout[f"{step}/exercises/{ex}/prompt.md"] = f"Task text for {ex}. Return the list sorted."
    layout["04-d/exercises/x4/say.md"] = "model answer"
    for name, text in layout.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    return root


@pytest.fixture
def env(tmp_path):
    seen = []

    def fake(prompt, json_mode=True):
        seen.append((prompt, json_mode))
        if json_mode:
            n = int(re.search(r"Return exactly (\d+) scores", prompt).group(1))
            return json.dumps({"scores": [4] * n, "verdict": "ok", "feedback": "fine"})
        return "Here you go:\n```python\ndef f(xs):\n    return sorted(xs)\n```" if "WRITE-CODE" in prompt else "Think about ordering."

    client = TestClient(create_app(build(tmp_path), tmp_path / "p.db", call=fake))
    return client, seen


def chat(client, scope, message, mode="", code="", output=""):
    r = client.post("/api/chat", json={"scope": scope, "message": message, "mode": mode, "code": code, "output": output})
    assert r.status_code == 200, r.text
    return r.json()


def test_prompt_has_task_and_learner_state_but_never_the_reference(env):
    client, seen = env
    chat(client, "e4", "What should I do first?", code="def f(xs):\n    pass", output="FAIL test_a")
    prompt, json_mode = seen[-1]
    assert json_mode is False
    assert "Task text for e4" in prompt and "def f(xs):\n    pass" in prompt and "FAIL test_a" in prompt
    assert "SECRET-REFERENCE" not in prompt and "test_hidden" not in prompt


def test_tutor_only_in_early_steps_interview_allowed_later(env):
    client, _ = env
    assert chat(client, "e1", "WRITE-CODE for me", mode="interview")["mode"] == "tutor"
    assert chat(client, "e4", "hi", mode="interview")["mode"] == "interview"
    assert chat(client, "e4", "hi")["mode"] == "tutor"
    assert chat(client, "x4", "hi", mode="interview")["mode"] == "tutor"  # answer-writing exercises stay tutor-only


def test_history_is_saved_cleared_and_fed_back(env):
    client, seen = env
    chat(client, "e1", "first question")
    chat(client, "e1", "second question")
    assert "first question" in seen[-1][0] and "Think about ordering." in seen[-1][0]
    state = client.get("/api/chat", params={"scope": "e1"}).json()
    assert [m["role"] for m in state["messages"]] == ["user", "assistant", "user", "assistant"]
    assert state["interview_allowed"] is False
    client.post("/api/chat/clear", json={"scope": "e1"})
    assert client.get("/api/chat", params={"scope": "e1"}).json()["messages"] == []


def test_quiz_has_no_assistant_and_empty_message_is_rejected(env):
    client, _ = env
    assert client.get("/api/chat", params={"scope": "q4"}).status_code == 400
    assert client.post("/api/chat", json={"scope": "e1", "message": "  "}).status_code == 400
    assert client.get("/api/chat", params={"scope": "nope"}).status_code == 404


def test_provider_failure_is_a_502_and_keeps_the_history_clean(tmp_path):
    def boom(prompt, json_mode=True):
        raise OSError("offline")

    client = TestClient(create_app(build(tmp_path), tmp_path / "p.db", call=boom))
    assert client.post("/api/chat", json={"scope": "e1", "message": "hi"}).status_code == 502
    assert client.get("/api/chat", params={"scope": "e1"}).json()["messages"] == []


def test_code_from_the_assistant_means_explain_it_back(env):
    client, _ = env
    sub = lambda: client.post("/api/submit", json={"exercise_id": "e4", "code": "def f(xs):\n    return sorted(xs)\n",
                                                    "mode": "blank", "duration_s": 5}).json()
    assert chat(client, "e4", "Tell me about sorting", mode="interview")["assisted"] is False  # no code in the reply
    assert chat(client, "e4", "WRITE-CODE", mode="interview")["assisted"] is True
    first = sub()
    assert first["passed"] and first["status"]["assisted"] and first["status"]["explain"] is False
    assert first["status"]["done"] is False
    assert client.post("/api/review", json={"exercise_id": "e4", "attempt_id": first["attempt_id"], "text": ""}).status_code == 400
    rev = client.post("/api/review", json={"exercise_id": "e4", "attempt_id": first["attempt_id"],
                                           "text": "sorted returns a new sorted list in O(n log n)."}).json()
    assert rev["status"] == "done"
    status = client.get("/api/exercise/e4").json()["status"]
    assert status["explain"] is True and status["done"] is True and status["assisted"] is True
    # clearing the chat does not hide that the assistant helped
    client.post("/api/chat/clear", json={"scope": "e4"})
    assert client.get("/api/exercise/e4").json()["status"]["assisted"] is True


def test_tutor_replies_with_code_do_not_count_as_assisted(env):
    client, _ = env
    chat(client, "e1", "WRITE-CODE", mode="tutor")  # the fake returns code for this wording
    assert client.get("/api/exercise/e1").json()["status"]["assisted"] is False


def test_grade_my_prompts_reviews_only_what_the_learner_typed(env):
    client, seen = env
    assert client.post("/api/chat/grade", json={"scope": "e4"}).status_code == 400
    chat(client, "e4", "Write f(xs) returning the sorted list; handle empty input.", mode="interview")
    rev = client.post("/api/chat/grade", json={"scope": "e4"}).json()
    assert rev["status"] == "done" and len(rev["scores"]) == 4
    graded_prompt = seen[-1][0]
    assert "Prompt 1: Write f(xs) returning the sorted list" in graded_prompt and "Here you go" not in graded_prompt
    assert client.get("/api/exercise/x4").json()["review"] is None  # does not touch the exercise's own reviews


def test_mock_round_uses_typed_prompts_when_there_are_any(tmp_path):
    root = build(tmp_path)
    for step, ex in (("04-d", "m1"), ("04-d", "m2")):
        d = root / step / "exercises" / ex
        d.mkdir(parents=True)
        (d / "prompt.md").write_text(f"Mock task {ex}")
        (d / "hint.md").write_text("h")
        (d / "say.md").write_text("s")
    (root / "04-d/exercises/m1/exercise.yaml").write_text("title: M1\nkind: python\nmock: true\n")
    (root / "04-d/exercises/m1/solution.py").write_text("x = 1\n")
    (root / "04-d/exercises/m1/tests").mkdir()
    (root / "04-d/exercises/m1/tests/test_hidden.py").write_text("def test_a():\n    assert True\n")
    (root / "04-d/exercises/m2/exercise.yaml").write_text("title: M2\nkind: sql\nmock: true\n")
    (root / "04-d/exercises/m2/seed.sql").write_text("CREATE TABLE t (x INTEGER);\nINSERT INTO t VALUES (1);\n")
    (root / "04-d/exercises/m2/solution.sql").write_text("SELECT x FROM t;")
    prompts = []

    def fake(prompt, json_mode=True):
        if not json_mode:
            return "reply"
        prompts.append(prompt)
        if '"questions"' in prompt:
            return json.dumps({"questions": ["a?", "b?", "c?"]})
        n = int(re.search(r"Return exactly (\d+) scores", prompt).group(1))
        return json.dumps({"scores": [4] * n, "verdict": "v", "feedback": "f"})

    client = TestClient(create_app(root, tmp_path / "p.db", call=fake))
    mid = client.post("/api/mock/start").json()["mock_id"]
    ctx = client.post("/api/chat", json={"scope": f"mock:{mid}", "message": "Write the sql query", "mode": "interview"}).json()
    assert ctx["mode"] == "interview"
    client.post(f"/api/mock/{mid}/submit", json={"python_code": "x = 1\n", "sql_code": "SELECT x FROM t;",
                                                  "prompt_text": "BOX TEXT", "duration_s": 5})
    client.post(f"/api/mock/{mid}/answers", json={"answers": ["a", "b", "c"]})
    graded = [p for p in prompts if "Prompt 1: Write the sql query" in p]
    assert graded and not any("BOX TEXT" in p for p in prompts)


def test_build_prompt_and_code_block_detection():
    p = assistant.build_prompt("tutor", "T", "sql", "task", "CREATE TABLE t (x);", "", "", [], "hi")
    assert "Never write the solution" in p and "## Tables" in p and "## The learner's current code" not in p
    assert "Do what the user asks" in assistant.build_prompt("interview", "T", "python", "task", "", "", "", [], "hi")
    assert assistant.has_code_block("a\n```py\nx\n```") and not assistant.has_code_block("no code")
