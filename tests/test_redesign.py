import json
import re

import pytest
from fastapi.testclient import TestClient

from gym.app import create_app
from gym.content import load_content

TOTAL_TESTS = "from solution import total\n\ndef test_sum():\n    assert total([1, 2, 3]) == 6\n\ndef test_empty():\n    assert total([]) == 0\n"
CHANGE_TESTS = ("from solution import total\n\ndef test_start():\n    assert total([1, 2], start=10) == 13\n\n"
                "def test_default():\n    assert total([1, 2]) == 3\n")
SOLUTION = "def total(xs):\n    result = 0\n    for x in xs:\n        result += x\n    return result\n"
CHANGED = "def total(xs, start=0):\n    result = start\n    for x in xs:\n        result += x\n    return result\n"


def files():
    f = {
        "t1/step.yaml": "title: Track 1\norder: 1\nincludes: [lib1]\nsequence: [r1, p1, lib1, b1, tr1]\n",
        "t2/step.yaml": "title: Track 2\norder: 2\n",
        "t2/exercises/t2x/exercise.yaml": "title: T2x\nkind: open\n",
        "t2/exercises/t2x/prompt.md": "p",
        "t2/cards.yaml": "- id: c-track\n  front: What does this do?\n  back: x\n",
        "lib/step.yaml": "title: Library\norder: 101\nshelf: true\n",
        "lib/cards.yaml": "- id: c-lib\n  front: type this\n  back: y\n",
        "lib/exercises/lib1/exercise.yaml": "title: Lib1\nkind: python\n",
        "lib/exercises/lib1/prompt.md": "Return the total of a list.",
        "lib/exercises/lib1/solution.py": SOLUTION,
        "lib/exercises/lib1/starter.py": "def total(xs):\n    pass\n",
        "lib/exercises/lib1/tests/test_hidden.py": TOTAL_TESTS,
        "lib/exercises/lib2/exercise.yaml": "title: Lib2\nkind: open\n",
        "lib/exercises/lib2/prompt.md": "p",
        # a reading exercise
        "t1/exercises/r1/exercise.yaml": "title: Read it\nkind: read\nquestions:\n  - What does line 1 do?\n  - What if the list is empty?\n",
        "t1/exercises/r1/prompt.md": "Read the code. Predict what it prints.",
        "t1/exercises/r1/snippet.py": "xs = [1, 2, 3]\nprint(sum(xs))\nprint(len(xs))\n",
        "t1/exercises/r1/expected.txt": "6\n3\n",
        "t1/exercises/r1/say.md": "Sum then length.",
        # python with a plan, prompt grading and a control check
        "t1/exercises/p1/exercise.yaml": "title: Plan it\nkind: python\nplan_required: 2\ngrade_prompts: true\n",
        "t1/exercises/p1/prompt.md": "Return the total of a list.",
        "t1/exercises/p1/solution.py": SOLUTION,
        "t1/exercises/p1/starter.py": "# PLAN\n\ndef total(xs):\n    pass\n",
        "t1/exercises/p1/tests/test_hidden.py": TOTAL_TESTS,
        "t1/exercises/p1/change.md": "Add an optional start value (default 0) that the sum starts from.",
        "t1/exercises/p1/change_tests/test_change.py": CHANGE_TESTS,
        "t1/exercises/p1/change_solution.py": CHANGED,
        # assistant-written buggy code: fix it and name the bug
        "t1/exercises/b1/exercise.yaml": "title: Fix it\nkind: python\nname_bug: true\nassistant: off\n",
        "t1/exercises/b1/prompt.md": "An assistant wrote this. Fix it.",
        "t1/exercises/b1/solution.py": SOLUTION,
        "t1/exercises/b1/starter.py": "def total(xs):\n    result = 0\n    for x in xs[1:]:\n        result += x\n    return result\n",
        "t1/exercises/b1/tests/test_hidden.py": TOTAL_TESTS,
        "t1/exercises/b1/bug.md": "The loop skips the first element (xs[1:]).",
        # accept or reject
        "t1/exercises/tr1/exercise.yaml": "title: Triage\nkind: triage\npass_ratio: 0.5\n",
        "t1/exercises/tr1/prompt.md": "The assistant proposed these changes.",
        "t1/exercises/tr1/proposals.yaml": ("- title: Rename a variable\n  code: x = 1\n  correct: accept\n  why: harmless\n"
                                              "- title: Add a new dependency\n  code: import requests\n  correct: reject\n  why: nobody asked\n"),
    }
    return f


@pytest.fixture
def env(tmp_path):
    seen = []

    def fake(prompt, json_mode=True):
        seen.append((prompt, json_mode))
        if json_mode:
            n = int(re.search(r"Return exactly (\d+) scores", prompt).group(1))
            return json.dumps({"scores": [4] * n, "verdict": "ok", "feedback": "fine"})
        return "SIZE: small\n\n```python\ndef f(): pass\n```" if "WRITE-CODE" in prompt else "SIZE: small\n\nok"

    root = tmp_path / "c"
    for name, text in files().items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    return TestClient(create_app(root, tmp_path / "p.db", call=fake)), seen, root


def post(client, path, body=None, status=200):
    r = client.post(path, json=body or {})
    assert r.status_code == status, r.text
    return r.json()


def test_includes_move_exercises_and_sequence_orders_them(env):
    _, _, root = env
    steps, errors = load_content(root)
    by = {s.id: s for s in steps}
    assert errors == []
    assert [e.id for e in by["t1"].exercises] == ["r1", "p1", "lib1", "b1", "tr1"]
    assert [e.id for e in by["lib"].exercises] == ["lib2"] and by["lib"].shelf
    assert next(e for e in by["t1"].exercises if e.id == "lib1").step_id == "t1"


def test_unknown_include_or_sequence_entries_are_reported(tmp_path):
    root = tmp_path / "c"
    (root / "a").mkdir(parents=True)
    (root / "a" / "step.yaml").write_text("title: A\norder: 1\nincludes: [nope]\nsequence: [also-nope]\n")
    _, errors = load_content(root)
    assert any("includes unknown exercise nope" in e for e in errors) and any("unknown exercise also-nope" in e for e in errors)


def test_library_is_open_and_off_the_track(env):
    client, _, _ = env
    j = client.get("/api/journey").json()
    assert [s["id"] for s in j["steps"]] == ["t1", "t2"] and [s["id"] for s in j["library"]] == ["lib"]
    assert j["steps"][1]["unlocked"] is False and j["library"][0]["unlocked"] is True
    assert j["next"]["exercise_id"] == "r1"
    assert [c["id"] for c in client.get("/api/cards/due").json()] == ["c-track"]  # the daily deck is the track's cards
    assert client.get("/api/exercise/lib2").json()["next"] is None  # the shelf does not lead into the track


def test_reading_exercise_prediction_reveal_and_review(env):
    client, seen, _ = env
    ex = client.get("/api/exercise/r1").json()
    assert ex["kind"] == "read" and "sum(xs)" in ex["snippet"] and ex["expected"] == "" and len(ex["questions"]) == 2
    assert post(client, "/api/predict/reveal", {"exercise_id": "r1"}, status=400)  # predict first
    wrong = post(client, "/api/predict", {"exercise_id": "r1", "prediction": "7\n3"})
    assert wrong["passed"] is False and wrong["status"]["tests"] is False
    assert post(client, "/api/predict/reveal", {"exercise_id": "r1"})["output"].strip() == "6\n3"
    assert client.get("/api/exercise/r1").json()["expected"].strip() == "6\n3"
    ok = post(client, "/api/predict", {"exercise_id": "r1", "prediction": "6 \n3\n\n"})  # trailing whitespace does not matter
    assert ok["passed"] and ok["status"]["tests"] is True and ok["status"]["done"] is False  # still needs the explanation
    rev = post(client, "/api/review", {"exercise_id": "r1", "text": "Line 1 sums; empty list gives 0."})
    assert rev["status"] == "done"
    prompt = seen[-1][0]
    assert "sum(xs)" in prompt and "What if the list is empty?" in prompt and "Sum then length." in prompt
    assert client.get("/api/exercise/r1").json()["status"]["done"] is True


def test_triage_scores_decisions_and_reviews_reasons(env):
    client, _, _ = env
    ex = client.get("/api/exercise/tr1").json()
    assert [p["title"] for p in ex["proposals"]] == ["Rename a variable", "Add a new dependency"]
    assert "correct" not in ex["proposals"][0] and "why" not in ex["proposals"][0]
    assert post(client, "/api/triage", {"exercise_id": "tr1", "decisions": [{"choice": "accept"}]}, status=400)
    bad = post(client, "/api/triage", {"exercise_id": "tr1", "decisions": [
        {"choice": "reject", "reason": ""}, {"choice": "accept", "reason": ""}]})
    assert bad["correct"] == 0 and bad["review"] is None and bad["status"]["done"] is False
    good = post(client, "/api/triage", {"exercise_id": "tr1", "decisions": [
        {"choice": "accept", "reason": "just a rename"}, {"choice": "reject", "reason": "nobody asked for a dependency"}]})
    assert good["passed"] and good["review"]["status"] == "done" and good["results"][1]["why"] == "nobody asked"
    assert good["status"]["done"] is True


def test_naming_the_bug_needs_a_pass_and_is_reviewed_against_the_reference(env):
    client, seen, _ = env
    assert client.get("/api/chat", params={"scope": "b1"}).json()["policy"] == "off"
    assert post(client, "/api/bug", {"exercise_id": "b1", "text": "x"}, status=400)  # fix the code first
    fixed = post(client, "/api/submit", {"exercise_id": "b1", "code": SOLUTION, "mode": "blank", "duration_s": 1})
    assert fixed["passed"] and fixed["status"]["bug"] is False and fixed["status"]["done"] is False
    assert post(client, "/api/bug", {"exercise_id": "b1", "text": " "}, status=400)
    rev = post(client, "/api/bug", {"exercise_id": "b1", "text": "It skipped the first element."})
    assert rev["status"] == "done" and "The loop skips the first element" in seen[-1][0]
    assert client.get("/api/exercise/b1").json()["status"]["done"] is True


def test_a_plan_is_required_before_the_code_runs(env):
    client, _, _ = env
    r = post(client, "/api/submit", {"exercise_id": "p1", "code": "def total(xs):\n    return sum(xs)\n", "mode": "blank"})
    assert r["passed"] is False and r["plan_missing"] and "at least 2 plan lines" in r["output"]
    assert client.get("/api/exercise/p1").json()["status"]["tests"] is False  # nothing was recorded
    ok = post(client, "/api/submit", {"exercise_id": "p1", "mode": "blank",
                                      "code": "# 1. start at zero\n# 2. add each item\ndef total(xs):\n    return sum(xs)\n"})
    assert ok["passed"]


def test_prompt_grading_is_a_gate_when_the_exercise_asks_for_it(env):
    client, _, _ = env
    code = "# a\n# b\ndef total(xs):\n    return sum(xs)\n"
    st = post(client, "/api/submit", {"exercise_id": "p1", "code": code, "mode": "blank"})["status"]
    assert st["tests"] is True and st["prompts"] is False and st["done"] is False
    post(client, "/api/chat", {"scope": "p1", "message": "Write total(xs) that sums a list, 0 for empty."})
    post(client, "/api/chat/grade", {"scope": "p1"})
    assert client.get("/api/exercise/p1").json()["status"]["prompts"] is True


def test_the_control_check_end_to_end(env):
    client, seen, _ = env
    assert post(client, "/api/control/start", {"exercise_id": "p1"}, status=400)  # pass first
    assert client.get("/api/exercise/p1").json()["control"]["started"] is False
    code = "# a\n# b\ndef total(xs):\n    result = 0\n    for x in xs:\n        result += x\n    return result\n"
    post(client, "/api/submit", {"exercise_id": "p1", "code": code, "mode": "blank"})
    started = post(client, "/api/control/start", {"exercise_id": "p1"})
    ctl = started["control"]
    assert ctl["started"] and ctl["locked"] and len(ctl["lines"]) == 2 and "optional start" in ctl["change"]
    assert started["code"] == code
    assert post(client, "/api/control/start", {"exercise_id": "p1"})["control"]["lines"] == ctl["lines"]  # stable
    # the assistant is off while the check is open
    assert post(client, "/api/chat", {"scope": "p1", "message": "just do it"}, status=403)
    assert client.get("/api/chat", params={"scope": "p1"}).json()["locked"] is True
    # part A: explain the two lines
    assert post(client, "/api/control/explain", {"exercise_id": "p1", "explanations": ["only one"]}, status=400)
    a = post(client, "/api/control/explain", {"exercise_id": "p1", "explanations": ["It adds x to the total.", "It starts at zero."]})
    assert a["a_ok"] and a["review"]["status"] == "done"
    assert ctl["lines"][0]["text"].strip() in seen[-1][0]
    assert a["status"]["control"] is False and a["status"]["done"] is False  # still needs the change
    # part B: the change by hand, checked by hidden tests
    wrong = post(client, "/api/control/change", {"exercise_id": "p1", "code": code})
    assert wrong["passed"] is False and wrong["control"]["b_ok"] is False
    right = post(client, "/api/control/change", {"exercise_id": "p1", "code": CHANGED})
    assert right["passed"] and right["control"]["complete"] and right["status"]["control"] is True
    assert client.get("/api/chat", params={"scope": "p1"}).json()["locked"] is False  # the assistant is back
    # change attempts never count as the exercise's own pass
    assert client.get("/api/exercise/p1").json()["status"]["tests"] is True


def test_a_low_line_explanation_review_does_not_open_the_change(tmp_path):
    def stingy(prompt, json_mode=True):
        n = int(re.search(r"Return exactly (\d+) scores", prompt).group(1))
        return json.dumps({"scores": [1] * n, "verdict": "no", "feedback": "weak"})

    root = tmp_path / "c"
    for name, text in files().items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    client = TestClient(create_app(root, tmp_path / "p.db", call=stingy))
    post(client, "/api/submit", {"exercise_id": "p1", "mode": "blank", "code": "# a\n# b\ndef total(xs):\n    return sum(xs)\n"})
    post(client, "/api/control/start", {"exercise_id": "p1"})
    a = post(client, "/api/control/explain", {"exercise_id": "p1", "explanations": ["x", "y"]})
    assert a["a_ok"] is False and a["control"]["a_ok"] is False
