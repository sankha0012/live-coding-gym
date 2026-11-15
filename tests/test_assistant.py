import json
import re

import pytest
from fastapi.testclient import TestClient

from gym import assistant
from gym.app import create_app

SECRET_SOLUTION = "return sorted(xs)  # SECRET-REFERENCE"
TESTS = "from solution import f\n\ndef test_a():\n    assert f([2, 1]) == [1, 2]\n"


def build(tmp_path, extra=None):
    """A python exercise (train), an explain exercise (explain), a locked one (off) and a quiz."""
    root = tmp_path / "c"
    layout = {
        "01-a/step.yaml": "title: A\norder: 1\n",
        "01-a/exercises/e1/exercise.yaml": "title: Sort it\nkind: python\n",
        "01-a/exercises/e1/solution.py": f"def f(xs):\n    {SECRET_SOLUTION}\n",
        "01-a/exercises/e1/starter.py": "def f(xs):\n    pass\n",
        "01-a/exercises/e1/tests/test_hidden.py": TESTS,
        "01-a/exercises/off1/exercise.yaml": "title: Off\nkind: python\nassistant: off\n",
        "01-a/exercises/off1/solution.py": "def f(xs):\n    return xs\n",
        "01-a/exercises/off1/tests/test_hidden.py": TESTS,
        "01-a/exercises/x4/exercise.yaml": "title: Explain\nkind: explain\n",
        "01-a/exercises/x4/say.md": "model answer",
        "01-a/exercises/q4/exercise.yaml": "title: Quiz\nkind: quiz\n",
        "01-a/exercises/q4/quiz.yaml": "- q: Q\n  options: [a, b]\n  answer: 0\n",
    }
    for ex in ("e1", "off1", "x4", "q4"):
        layout[f"01-a/exercises/{ex}/prompt.md"] = f"Task text for {ex}. Return the list sorted."
    layout.update(extra or {})
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
        if "WHOLE" in prompt.split("## New message from the learner")[-1]:
            return "SIZE: large\n\nThat is too big. Split it into pieces and tell me which to start with."
        if "WRITE-CODE" in prompt.split("## New message from the learner")[-1]:
            return "SIZE: small\n\n```python\ndef f(xs):\n    return sorted(xs)\n```\nIt sorts."
        return "SIZE: small\n\nThink about ordering."

    client = TestClient(create_app(build(tmp_path), tmp_path / "p.db", call=fake))
    return client, seen


def chat(client, scope, message, code="", output=""):
    r = client.post("/api/chat", json={"scope": scope, "message": message, "code": code, "output": output})
    assert r.status_code == 200, r.text
    return r.json()


def test_prompt_has_task_and_learner_state_but_never_the_reference(env):
    client, seen = env
    chat(client, "e1", "What should I do first?", code="def f(xs):\n    pass", output="FAIL test_a")
    prompt, json_mode = seen[-1]
    assert json_mode is False
    assert "Task text for e1" in prompt and "def f(xs):\n    pass" in prompt and "FAIL test_a" in prompt
    assert "SECRET-REFERENCE" not in prompt and "test_hidden" not in prompt


def test_policies_change_what_the_assistant_is_told(env):
    client, seen = env
    chat(client, "e1", "hi")
    assert "at most ONE function" in seen[-1][0] and "SIZE:" in seen[-1][0]
    chat(client, "x4", "hi")
    assert "you never write code for them" in seen[-1][0]
    assert client.get("/api/chat", params={"scope": "e1"}).json()["policy"] == "train"
    assert client.get("/api/chat", params={"scope": "x4"}).json()["policy"] == "explain"


def test_an_exercise_can_switch_the_assistant_off(env):
    client, _ = env
    assert client.post("/api/chat", json={"scope": "off1", "message": "hi"}).status_code == 403
    assert client.get("/api/chat", params={"scope": "off1"}).json()["policy"] == "off"


def test_the_size_line_is_stripped_stored_and_oversized_asks_are_sent_back(env):
    client, _ = env
    r = chat(client, "e1", "Write the WHOLE task for me")
    assert r["size"] == "large" and r["reply"].startswith("That is too big") and "SIZE" not in r["reply"]
    r = chat(client, "e1", "WRITE-CODE for one function")
    assert r["size"] == "small" and "```python" in r["reply"]
    state = client.get("/api/chat", params={"scope": "e1"}).json()
    assert all("SIZE" not in m["content"] for m in state["messages"])


def test_history_is_saved_cleared_and_fed_back(env):
    client, seen = env
    chat(client, "e1", "first question")
    chat(client, "e1", "second question")
    assert "first question" in seen[-1][0] and "Think about ordering." in seen[-1][0]
    state = client.get("/api/chat", params={"scope": "e1"}).json()
    assert [m["role"] for m in state["messages"]] == ["user", "assistant", "user", "assistant"]
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
    sub = lambda: client.post("/api/submit", json={"exercise_id": "e1", "code": "def f(xs):\n    return sorted(xs)\n",
                                                    "mode": "blank", "duration_s": 5}).json()
    assert chat(client, "e1", "Tell me about sorting")["assisted"] is False  # no code in the reply
    assert chat(client, "e1", "WRITE-CODE")["assisted"] is True
    first = sub()
    assert first["passed"] and first["status"]["assisted"] and first["status"]["explain"] is False
    assert first["status"]["done"] is False
    assert client.post("/api/review", json={"exercise_id": "e1", "attempt_id": first["attempt_id"], "text": ""}).status_code == 400
    rev = client.post("/api/review", json={"exercise_id": "e1", "attempt_id": first["attempt_id"],
                                           "text": "sorted returns a new sorted list in O(n log n)."}).json()
    assert rev["status"] == "done"
    status = client.get("/api/exercise/e1").json()["status"]
    assert status["explain"] is True and status["done"] is True and status["assisted"] is True
    client.post("/api/chat/clear", json={"scope": "e1"})  # clearing the chat does not hide that the assistant helped
    assert client.get("/api/exercise/e1").json()["status"]["assisted"] is True


def test_explain_only_replies_with_code_do_not_count_as_assisted(env):
    client, _ = env
    chat(client, "x4", "WRITE-CODE")  # an explain exercise: even if the model slipped, nothing was handed over
    assert client.get("/api/exercise/x4").json()["status"].get("assisted") in (False, None)


def test_grade_my_prompts_reviews_only_what_the_learner_typed(env):
    client, seen = env
    assert client.post("/api/chat/grade", json={"scope": "e1"}).status_code == 400
    chat(client, "e1", "Write f(xs) returning the sorted list; handle empty input.")
    rev = client.post("/api/chat/grade", json={"scope": "e1"}).json()
    assert rev["status"] == "done" and len(rev["scores"]) == 4
    graded_prompt = seen[-1][0]
    assert "Prompt 1: Write f(xs) returning the sorted list" in graded_prompt and "Think about ordering" not in graded_prompt
    assert client.get("/api/exercise/x4").json()["review"] is None  # does not touch the exercise's own reviews


def test_build_prompt_and_helpers():
    p = assistant.build_prompt("explain", "T", "sql", "task", "CREATE TABLE t (x);", "", "", [], "hi")
    assert "never write code" in p and "## Tables" in p and "## The learner's current code" not in p
    assert "Do what the user asks" in assistant.build_prompt("free", "T", "python", "task", "", "", "", [], "hi")
    assert assistant.has_code_block("a\n```py\nx\n```") and not assistant.has_code_block("no code")
    assert assistant.split_size("SIZE: large\n\nToo big.") == ("large", "Too big.")
    assert assistant.split_size("no tag") == (None, "no tag")
