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
        "t1/step.yaml": "title: Track 1\norder: 1\nsequence: [r1, r3, p1, p2, p3, lib1, b1, tr1, q1]\n",
        "t2/step.yaml": "title: Track 2\norder: 2\n",
        "t2/exercises/t2x/exercise.yaml": "title: T2x\nkind: open\n",
        "t2/exercises/t2x/prompt.md": "p",
        "t2/cards.yaml": "- id: c-track\n  front: What does this do?\n  back: x\n",
        "lib/step.yaml": "title: Extra\norder: 101\noptional: true\n",
        "lib/cards.yaml": "- id: c-lib\n  front: type this\n  back: y\n",
        "t1/exercises/lib1/exercise.yaml": "title: Lib1\nkind: python\n",
        "t1/exercises/lib1/prompt.md": "Return the total of a list.",
        "t1/exercises/lib1/solution.py": SOLUTION,
        "t1/exercises/lib1/starter.py": "def total(xs):\n    pass\n",
        "t1/exercises/lib1/tests/test_hidden.py": TOTAL_TESTS,
        "lib/exercises/lib2/exercise.yaml": "title: Lib2\nkind: open\n",
        "lib/exercises/lib2/prompt.md": "p",
        # a reading exercise
        "t1/exercises/r1/exercise.yaml": "title: Read it\nkind: read\nlevel: 2\nquestions:\n  - What does line 1 do?\n  - What if the list is empty?\n",
        "t1/exercises/r1/prompt.md": "Read the code. Predict what it prints.",
        "t1/exercises/r1/snippet.py": "xs = [1, 2, 3]\nprint(sum(xs))\nprint(len(xs))\n",
        "t1/exercises/r1/expected.txt": "6\n3\n",
        "t1/exercises/r1/say.md": "Sum then length.",
        "t1/exercises/r1/whatif.yaml": (
            "- {change: 'Line 1: the list gets a 4', old: 'xs = [1, 2, 3]', new: 'xs = [1, 2, 3, 4]', answer: different}\n"
            "- {change: 'Line 3: a harmless + 0', old: 'print(len(xs))', new: 'print(len(xs) + 0)', answer: same}\n"
            "- {change: 'Line 2: a typo', old: 'print(sum(xs))', new: 'print(sum(ys))', answer: crash}\n"
            "- {change: 'Line 1: the list is reversed', old: 'xs = [1, 2, 3]', new: 'xs = [3, 2, 1]', answer: same}\n"),
        # python with a plan, prompt grading and a control check
        "t1/exercises/p1/exercise.yaml": "title: Plan it\nkind: python\nlevel: 3\nplan_required: 2\ngrade_prompts: true\n",
        "t1/exercises/p1/prompt.md": "Return the total of a list.",
        "t1/exercises/p1/solution.py": SOLUTION,
        "t1/exercises/p1/starter.py": "# PLAN\n\ndef total(xs):\n    pass\n",
        "t1/exercises/p1/tests/test_hidden.py": TOTAL_TESTS,
        "t1/exercises/p1/change.md": "Add an optional start value (default 0) that the sum starts from.",
        "t1/exercises/p1/change_tests/test_change.py": CHANGE_TESTS,
        "t1/exercises/p1/change_solution.py": CHANGED,
        # a level 3 reading: What if, a fix to make, then a written explanation
        "t1/exercises/r3/exercise.yaml": "title: Fix it read\nkind: read\nlevel: 3\nquestions: [\"What is wrong?\"]\n",
        "t1/exercises/r3/prompt.md": "Read.",
        "t1/exercises/r3/snippet.py": "print(sum([1, 2, 3]) - 1)\n",
        "t1/exercises/r3/expected.txt": "5\n",
        "t1/exercises/r3/say.md": "Off by one.",
        "t1/exercises/r3/fix.md": "Make it print 6.",
        "t1/exercises/r3/fix_expected.txt": "6\n",
        "t1/exercises/r3/fix_solution.py": "print(sum([1, 2, 3]))\n",
        "t1/exercises/r3/whatif.yaml": (
            "- {change: a, old: 'sum(', new: 'max(', answer: different}\n- {change: b, old: ' - 1', new: ' - 0', answer: different}\n"
            "- {change: c, old: '[1, 2, 3]', new: '[1, 2, 3, 0]', answer: same}\n- {change: d, old: 'print(', new: 'prnt(', answer: crash}\n"),
        # builds at level 2 (What if, then a change) and level 1 (What if only)
        "t1/exercises/p2/exercise.yaml": "title: Level two\nkind: python\nlevel: 2\n",
        "t1/exercises/p2/prompt.md": "Return the total of a list.",
        "t1/exercises/p2/solution.py": SOLUTION,
        "t1/exercises/p2/starter.py": "def total(xs):\n    pass\n",
        "t1/exercises/p2/tests/test_hidden.py": TOTAL_TESTS,
        "t1/exercises/p2/change.md": "Add an optional start value.",
        "t1/exercises/p2/change_tests/test_change.py": CHANGE_TESTS,
        "t1/exercises/p2/change_solution.py": CHANGED,
        "t1/exercises/p3/exercise.yaml": "title: Level one\nkind: python\nlevel: 1\n",
        "t1/exercises/p3/prompt.md": "Return the total of a list.",
        "t1/exercises/p3/solution.py": SOLUTION,
        "t1/exercises/p3/starter.py": "def total(xs):\n    pass\n",
        "t1/exercises/p3/tests/test_hidden.py": TOTAL_TESTS,
        # assistant-written buggy code: fix it and name the bug
        "t1/exercises/b1/exercise.yaml": "title: Fix it\nkind: python\nname_bug: true\nassistant: off\n",
        "t1/exercises/b1/prompt.md": "An assistant wrote this. Fix it.",
        "t1/exercises/b1/solution.py": SOLUTION,
        "t1/exercises/b1/starter.py": "def total(xs):\n    result = 0\n    for x in xs[1:]:\n        result += x\n    return result\n",
        "t1/exercises/b1/tests/test_hidden.py": TOTAL_TESTS,
        "t1/exercises/b1/bug.md": "The loop skips the first element (xs[1:]).",
        # a SQL exercise with a control check and a documentation page
        "t1/exercises/q1/exercise.yaml": "title: Count\nkind: sql\nlevel: 3\nserves: [C6]\n",
        "t1/exercises/q1/prompt.md": "Count the orders.",
        "t1/exercises/q1/seed.sql": "CREATE TABLE orders (id INTEGER, city TEXT);\nINSERT INTO orders VALUES (1,'SP'),(2,'SP'),(3,'RJ');\n",
        "t1/exercises/q1/solution.sql": "SELECT COUNT(*) AS n\nFROM orders\nWHERE id > 0;\n",
        "t1/exercises/q1/docs.md": "COUNT(*) counts rows.",
        "t1/exercises/q1/change.md": "Count only the orders in SP.",
        "t1/exercises/q1/change_solution.sql": "SELECT COUNT(*) AS n FROM orders WHERE city = 'SP';\n",
        # accept or reject
        "t1/exercises/tr1/exercise.yaml": "title: Triage\nkind: triage\npass_ratio: 0.5\n",
        "t1/exercises/tr1/prompt.md": "The assistant proposed these changes.",
        "t1/exercises/tr1/script.py": "x = 0\n",
        "t1/exercises/tr1/proposals.yaml": ("- title: Rename a variable\n  code: x = 1\n  correct: accept\n  why: harmless\n"
                                              "- title: Add a new dependency\n  code: import requests\n  correct: reject\n  why: nobody asked\n"),
    }
    return f


@pytest.fixture
def env(tmp_path):
    seen = []

    def fake(prompt, json_mode=True):
        seen.append((prompt, json_mode))
        if "Write exactly" in prompt:  # the interviewer writing questions about the learner's code
            n = int(re.search(r"Write exactly (\d+) interview questions", prompt).group(1))
            sets = sum("Write exactly" in p for p, _ in seen)
            qs = [{"q": f"Set {sets} question {i}?", "strong": f"Notes {i}."} for i in range(1, n + 1)]
            return json.dumps({"questions": qs})
        if "## What a strong answer covers" in prompt:  # the interviewer, steered by words in the candidate's answer
            talk = prompt.split("## Conversation so far")[1]
            if "asks for a hint" in prompt and "(asked for a hint)" not in talk:
                return json.dumps({"reply": "Look at the loop."})
            final = "You have already asked a follow-up" in prompt
            last = [l for l in talk.splitlines() if l.startswith("Candidate:")][-1:] or [""]
            if "WRONG" in last[0]:
                return json.dumps({"verdict": "missed", "reply": "Not quite.", "follow_up": "", "strong": "The real answer."})
            if "VAGUE" in last[0] and not final:
                return json.dumps({"verdict": "probe", "reply": "Hm.", "follow_up": "And then what happens?", "strong": ""})
            return json.dumps({"verdict": "partial" if "VAGUE" in last[0] else "good", "reply": "Right.", "follow_up": "", "strong": "A strong answer."})
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


def test_sequence_orders_exercises(env):
    _, _, root = env
    steps, errors = load_content(root)
    by = {s.id: s for s in steps}
    assert errors == []
    assert [e.id for e in by["t1"].exercises] == ["r1", "r3", "p1", "p2", "p3", "lib1", "b1", "tr1", "q1"]
    assert [e.id for e in by["lib"].exercises] == ["lib2"] and by["lib"].optional


def test_unknown_sequence_entries_are_reported(tmp_path):
    root = tmp_path / "c"
    (root / "a").mkdir(parents=True)
    (root / "a" / "step.yaml").write_text("title: A\norder: 1\nsequence: [also-nope]\n")
    _, errors = load_content(root)
    assert any("unknown exercise also-nope" in e for e in errors)


def test_optional_step_is_open_and_never_blocks_or_feeds_the_deck(env):
    client, _, _ = env
    j = client.get("/api/journey").json()
    rows = {s["id"]: s for s in j["steps"]}
    assert [s["id"] for s in j["steps"]] == ["t1", "t2", "lib"]
    assert rows["t2"]["unlocked"] is False and rows["lib"]["unlocked"] is True and rows["lib"]["optional"]
    assert j["next"]["exercise_id"] == "r1"
    assert [c["id"] for c in client.get("/api/cards/due").json()] == ["c-track"]
    assert client.get("/api/exercise/lib2").json()["next"] is None


def test_step_page_groups_exercises_into_the_four_moves(env):
    client, _, _ = env
    groups = {e["id"]: e["group"] for e in client.get("/api/step/t1").json()["exercises"]}
    assert groups == {"r1": "Read", "r3": "Read", "p1": "Build", "p2": "Build", "p3": "Build", "lib1": "Build", "b1": "Catch", "tr1": "Catch", "q1": "Build"}
    assert client.get("/api/step/t2").json()["exercises"][0]["group"] == "Defend"


READ_ANSWERS = {"Line 1: the list gets a 4": "different", "Line 3: a harmless + 0": "same", "Line 2: a typo": "crash",
                "Line 1: the list is reversed": "same"}


def test_reading_exercise_what_if_then_a_written_answer(env):
    client, seen, _ = env
    ex = client.get("/api/exercise/r1").json()
    assert ex["kind"] == "read" and ex["level"] == 2 and "sum(xs)" in ex["snippet"] and ex["expected"] == ""
    assert ex["questions"] == ["In one sentence: what is the trap or surprise in this code?"] and ex["say"] == ""
    start = post(client, "/api/whatif/start", {"exercise_id": "r1"})["whatif"]
    assert len(start["questions"]) == 3 and start["choices"] == ["same", "different", "crash"] and "answer" not in start["questions"][0]
    assert post(client, "/api/whatif/start", {"exercise_id": "r1"})["whatif"]["questions"] == start["questions"]  # stable
    wrong = post(client, "/api/whatif/answer", {"exercise_id": "r1", "answers": ["crash"] * 3})
    assert wrong["ok"] is False and wrong["status"]["tests"] is False and all("answer" in r for r in wrong["results"])
    fresh = wrong["whatif"]  # a wrong round is replaced at once: seeing the answers must not pass the same set
    assert fresh["started"] and not fresh["ok"]
    right = post(client, "/api/whatif/answer", {"exercise_id": "r1", "answers": [READ_ANSWERS[q["change"]] for q in fresh["questions"]]})
    assert right["ok"] and right["status"]["tests"] is True and right["status"]["done"] is False  # still the written answer
    assert client.get("/api/exercise/r1").json()["expected"].strip() == "6\n3"
    view = client.get("/api/interview", params={"exercise_id": "r1"}).json()
    assert [q["q"] for q in view["qs"]] == ["In one sentence: what is the trap or surprise in this code?"] and view["i"] == 0
    probe = post(client, "/api/interview/answer", {"exercise_id": "r1", "text": "VAGUE: it sums."})
    assert probe["qs"][0]["verdict"] is None and probe["qs"][0]["followups"] == 1 and not probe["done"]
    assert probe["qs"][0]["turns"][-1] == {"who": "interviewer", "text": "Hm. And then what happens?"}
    assert "Sum then length." in seen[-1][0] and "sum(xs)" in seen[-1][0]  # the reference and the code are the interviewer's
    done = post(client, "/api/interview/answer", {"exercise_id": "r1", "text": "VAGUE: it counts too."})
    assert done["done"] and done["passed"] and done["qs"][0]["verdict"] == "partial"  # partial still passes
    assert done["status"]["review"] is True and done["status"]["done"] is True
    st = client.get("/api/exercise/r1").json()
    assert st["say"] == "Sum then length." and st["review"]["scores"] and "answered well" in st["review"]["verdict"]
    assert post(client, "/api/interview/answer", {"exercise_id": "r1", "text": "more"}, status=400)  # finished


def test_triage_scores_decisions_and_shows_the_reasons(env):
    client, _, _ = env
    ex = client.get("/api/exercise/tr1").json()
    assert [p["title"] for p in ex["proposals"]] == ["Rename a variable", "Add a new dependency"]
    assert ex["snippet"] == "x = 0\n"  # the main script, shown in the left pane
    assert "correct" not in ex["proposals"][0] and "why" not in ex["proposals"][0]
    assert post(client, "/api/triage", {"exercise_id": "tr1", "decisions": [{"choice": "accept"}]}, status=400)
    bad = post(client, "/api/triage", {"exercise_id": "tr1", "decisions": [{"choice": "reject"}, {"choice": "accept"}]})
    assert bad["correct"] == 0 and bad["status"]["done"] is False
    good = post(client, "/api/triage", {"exercise_id": "tr1", "decisions": [{"choice": "accept"}, {"choice": "reject"}]})
    assert good["passed"] and good["results"][1]["why"] == "nobody asked"
    assert good["status"]["done"] is True


def test_naming_the_bug_needs_a_pass_and_is_reviewed_against_the_reference(env):
    client, seen, _ = env
    assert client.get("/api/chat", params={"scope": "b1"}).json()["policy"] == "off"
    assert post(client, "/api/interview/answer", {"exercise_id": "b1", "part": "bug", "text": "x"}, status=400)  # fix the code first
    fixed = post(client, "/api/submit", {"exercise_id": "b1", "code": SOLUTION, "mode": "blank", "duration_s": 1})
    assert fixed["passed"] and fixed["status"]["bug"] is False and fixed["status"]["done"] is False
    assert post(client, "/api/interview/answer", {"exercise_id": "b1", "part": "bug", "text": " "}, status=400)
    rev = post(client, "/api/interview/answer", {"exercise_id": "b1", "part": "bug", "text": "It skipped the first element."})
    assert rev["done"] and rev["passed"] and "The loop skips the first element" in seen[-1][0]
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
    assert st["tests"] is True and st["prompts"] is None  # no prompts typed: nothing to grade, so not required
    post(client, "/api/chat", {"scope": "p1", "message": "WRITE-CODE total(xs) that sums a list, 0 for empty."})
    assert client.get("/api/exercise/p1").json()["status"]["prompts"] is False  # asked for code: now they must pass
    post(client, "/api/chat/grade", {"scope": "p1"})
    assert client.get("/api/exercise/p1").json()["status"]["prompts"] is True


def test_questions_and_asks_about_an_answer_are_not_graded_as_prompts(env):
    client, seen, _ = env
    post(client, "/api/submit", {"exercise_id": "p1", "code": "# a\n# b\ndef total(xs):\n    return sum(xs)\n", "mode": "blank"})
    post(client, "/api/chat", {"scope": "p1", "message": "Explain this line in plain words: return sum(xs)"})  # a question, reply has no code
    post(client, "/api/chat", {"scope": "p1", "message": "The interviewer asked: why? I missed it.", "explain_only": True})
    assert client.get("/api/exercise/p1").json()["status"]["prompts"] is None  # nothing that asked for code
    assert post(client, "/api/chat/grade", {"scope": "p1"}, status=400)
    post(client, "/api/chat", {"scope": "p1", "message": "WRITE-CODE the total function"})
    post(client, "/api/chat/grade", {"scope": "p1"})
    graded = seen[-1][0]
    assert "WRITE-CODE the total function" in graded and "Explain this line" not in graded and "The interviewer asked" not in graded


def asked(seen):
    """The prompts the app sent to have interview questions written."""
    return [p for p, _ in seen if "Write exactly" in p]


def test_the_control_check_end_to_end(env):
    client, seen, _ = env
    assert post(client, "/api/control/start", {"exercise_id": "p1"}, status=400)  # pass first
    assert client.get("/api/exercise/p1").json()["control"]["started"] is False
    code = "# a\n# b\ndef total(xs):\n    result = 0\n    for x in xs:\n        result += x\n    return result\n"
    post(client, "/api/submit", {"exercise_id": "p1", "code": code, "mode": "blank"})
    started = post(client, "/api/control/start", {"exercise_id": "p1"})
    ctl = started["control"]
    assert ctl["started"] and ctl["locked"] and "optional start" in ctl["change"] and started["code"] == code
    assert not asked(seen)  # questions are written when the learner opens the exchange
    # the assistant is off while the check is open
    assert post(client, "/api/chat", {"scope": "p1", "message": "just do it"}, status=403)
    assert client.get("/api/chat", params={"scope": "p1"}).json()["locked"] is True
    # part A: the interviewer asks three questions about this code
    talk = client.get("/api/interview", params={"exercise_id": "p1", "part": "defend"}).json()
    assert [q["q"] for q in talk["qs"]] == [f"Set 1 question {i}?" for i in (1, 2, 3)]
    assert len(asked(seen)) == 1 and "3: def total(xs):" in asked(seen)[0]  # numbered lines of the learner's code
    assert client.get("/api/interview", params={"exercise_id": "p1", "part": "defend"}).json()["qs"] == talk["qs"]  # stable
    assert len(asked(seen)) == 1
    assert "Notes 1." not in json.dumps(talk)  # the private notes never reach the browser
    for n in range(2):
        a = post(client, "/api/interview/answer", {"exercise_id": "p1", "part": "defend", "text": "It adds x to the total."})
        assert not a["done"] and a["control"]["a_ok"] is False
    a = post(client, "/api/interview/answer", {"exercise_id": "p1", "part": "defend", "text": "Empty gives zero."})
    assert a["done"] and a["passed"] and a["control"]["a_ok"] is True and "Notes" not in json.dumps(a)
    judged = seen[-1][0]
    assert code in judged and "Notes 3." in judged and "Return the total of a list." in judged  # the interviewer sees task, code and notes
    assert a["status"]["control"] is False and a["status"]["done"] is False  # still needs the change
    # part B: the change by hand, checked by hidden tests
    wrong = post(client, "/api/control/change", {"exercise_id": "p1", "code": code})
    assert wrong["passed"] is False and wrong["control"]["b_ok"] is False
    right = post(client, "/api/control/change", {"exercise_id": "p1", "code": CHANGED})
    assert right["passed"] and right["control"]["complete"] and right["status"]["control"] is True
    assert client.get("/api/chat", params={"scope": "p1"}).json()["locked"] is False  # the assistant is back
    # change attempts never count as the exercise's own pass
    assert client.get("/api/exercise/p1").json()["status"]["tests"] is True


def test_a_missed_question_blocks_the_check_and_a_retry_brings_new_questions(env):
    client, seen, _ = env
    post(client, "/api/submit", {"exercise_id": "p1", "mode": "blank", "code": "# a\n# b\ndef total(xs):\n    return sum(xs)\n"})
    post(client, "/api/control/start", {"exercise_id": "p1"})
    post(client, "/api/interview/answer", {"exercise_id": "p1", "part": "defend", "action": "hint", "text": ""})
    assert post(client, "/api/interview/answer", {"exercise_id": "p1", "part": "defend", "action": "hint"}, status=400)  # one hint each
    post(client, "/api/interview/answer", {"exercise_id": "p1", "part": "defend", "text": "WRONG"})
    post(client, "/api/interview/answer", {"exercise_id": "p1", "part": "defend", "action": "skip"})
    last = post(client, "/api/interview/answer", {"exercise_id": "p1", "part": "defend", "action": "skip"})
    assert last["done"] and last["passed"] is False and last["control"]["a_ok"] is False
    assert [q["verdict"] for q in last["qs"]] == ["missed"] * 3
    assert last["status"]["control"] is False
    fresh = post(client, "/api/interview/reset", {"exercise_id": "p1", "part": "defend"})
    assert not fresh["done"] and fresh["i"] == 0 and all(q["verdict"] is None for q in fresh["qs"])
    assert [q["q"] for q in fresh["qs"]] == [f"Set 2 question {i}?" for i in (1, 2, 3)]  # new questions, not the same ones again
    assert "Set 1 question 1?" in asked(seen)[1]  # the first set is passed in to be avoided


def test_new_passing_code_gets_new_questions(env):
    client, seen, _ = env
    post(client, "/api/submit", {"exercise_id": "p1", "mode": "blank", "code": "# a\n# b\ndef total(xs):\n    return sum(xs)\n"})
    post(client, "/api/control/start", {"exercise_id": "p1"})
    first = client.get("/api/interview", params={"exercise_id": "p1", "part": "defend"}).json()["qs"]
    post(client, "/api/submit", {"exercise_id": "p1", "mode": "blank", "code": "# a\n# b\ndef total(xs):\n    return sum(xs) + 0\n"})
    post(client, "/api/control/start", {"exercise_id": "p1"})
    second = client.get("/api/interview", params={"exercise_id": "p1", "part": "defend"}).json()["qs"]
    assert first != second and "sum(xs) + 0" in asked(seen)[1]


def test_the_interview_needs_passing_code_and_a_working_ai(tmp_path, env):
    client, _, root = env
    assert client.get("/api/interview", params={"exercise_id": "p1", "part": "defend"}).status_code == 400  # pass first
    assert client.get("/api/interview", params={"exercise_id": "lib2", "part": "defend"}).status_code in (400, 404)
    down = TestClient(create_app(root, tmp_path / "down.db", call=lambda p, json_mode=True: "garbage"))
    post(down, "/api/submit", {"exercise_id": "p1", "mode": "blank", "code": "# a\n# b\ndef total(xs):\n    return sum(xs)\n"})
    r = down.get("/api/interview", params={"exercise_id": "p1", "part": "defend"})
    assert r.status_code == 502 and "interviewer" in r.json()["detail"]
    assert down.get("/api/exercise/p1").json()["control"]["a_ok"] is False


def test_a_hint_caps_a_question_at_partial(env):
    client, _, _ = env
    hinted = post(client, "/api/interview/answer", {"exercise_id": "r1", "action": "hint"})
    assert hinted["qs"][0]["hinted"] and hinted["qs"][0]["turns"][-1]["text"] == "Look at the loop."
    done = post(client, "/api/interview/answer", {"exercise_id": "r1", "text": "It sums and counts."})
    assert done["qs"][0]["verdict"] == "partial"  # a good answer after a hint
    assert post(client, "/api/interview/reset", {"exercise_id": "r1"}, status=400)  # passed: nothing to retry


def test_sql_control_check_compares_the_changed_query_with_the_reference_result(env):
    client, seen, _ = env
    ex = client.get("/api/exercise/q1").json()
    assert ex["serves"] == ["C6"] and ex["docs"] == "COUNT(*) counts rows."
    solution = "SELECT COUNT(*) AS n\nFROM orders\nWHERE id > 0;\n"
    post(client, "/api/submit", {"exercise_id": "q1", "code": solution, "mode": "blank"})
    ctl = post(client, "/api/control/start", {"exercise_id": "q1"})["control"]
    assert ctl["started"] and "SP" in ctl["change"]
    for _ in range(3):
        post(client, "/api/interview/answer", {"exercise_id": "q1", "part": "defend", "text": "It filters and counts."})
    assert "WHERE id > 0" in asked(seen)[0]
    wrong = post(client, "/api/control/change", {"exercise_id": "q1", "code": solution})
    assert wrong["passed"] is False
    right = post(client, "/api/control/change", {"exercise_id": "q1", "code": "SELECT COUNT(*) AS n FROM orders WHERE city = 'SP'"})
    assert right["passed"] and right["control"]["b_ok"] and right["status"]["control"] is True


def test_dev_mode_opens_everything_and_reveals_answers(env):
    client, _, _ = env
    j = client.get("/api/journey").json()
    assert j["dev"] is False and j["steps"][1]["unlocked"] is False
    tri, rd, p1 = (client.get(f"/api/exercise/{i}").json() for i in ("tr1", "r1", "p1"))
    assert "correct" not in tri["proposals"][0] and rd["expected"] == "" and p1["reference"] == "" and p1["control"]["change"] == ""
    assert post(client, "/api/dev", {"dev": True})["dev"] is True
    j = client.get("/api/journey").json()
    assert j["dev"] and all(s["unlocked"] for s in j["steps"])
    tri, rd, p1, b1 = (client.get(f"/api/exercise/{i}").json() for i in ("tr1", "r1", "p1", "b1"))
    assert tri["proposals"][1]["correct"] == "reject" and tri["proposals"][1]["why"] == "nobody asked"
    assert rd["expected"].strip() == "6\n3" and "def total" in p1["reference"] and "Add an optional start" in p1["control"]["change"]
    assert "skips the first element" in b1["bug"] and "start=0" in p1["change_solution"]
    assert post(client, "/api/dev", {"dev": False})["dev"] is False


def test_password_protects_a_public_deployment(tmp_path, monkeypatch):
    import base64
    monkeypatch.setenv("GYM_PASSWORD", "s3cret")
    root = tmp_path / "c"
    for name, text in files().items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    client = TestClient(create_app(root, tmp_path / "p.db", call=lambda p, json_mode=True: "x"))
    assert client.get("/api/journey").status_code == 401
    good = {"Authorization": "Basic " + base64.b64encode(b"me:s3cret").decode()}
    bad = {"Authorization": "Basic " + base64.b64encode(b"me:nope").decode()}
    assert client.get("/api/journey", headers=good).status_code == 200
    assert client.get("/api/journey", headers=bad).status_code == 401


def answer_all(client, ex_id, n):
    for _ in range(n):
        r = post(client, "/api/interview/answer", {"exercise_id": ex_id, "part": "defend", "text": "Because it is simplest."})
    return r


def test_level_one_build_is_done_after_the_interviewer_exchange(env):
    client, seen, _ = env
    sub = post(client, "/api/submit", {"exercise_id": "p3", "code": SOLUTION, "mode": "blank"})
    assert sub["status"]["control"] is False and sub["status"]["done"] is False
    ctl = post(client, "/api/control/start", {"exercise_id": "p3"})["control"]
    assert ctl["level"] == 1 and ctl["locked"] and ctl["change"] == ""
    assert len(client.get("/api/interview", params={"exercise_id": "p3", "part": "defend"}).json()["qs"]) == 2
    assert "Design choice" in asked(seen)[0] and "Production" not in asked(seen)[0]
    r = answer_all(client, "p3", 2)
    assert r["done"] and r["control"]["complete"] and r["status"]["control"] is True and r["status"]["done"] is True
    assert post(client, "/api/control/change", {"exercise_id": "p3", "code": CHANGED}, status=400)  # level 1 has no change
    assert post(client, "/api/interview/answer", {"exercise_id": "p3", "part": "lines", "text": "a"}, status=400)  # no such part any more


def test_level_two_build_needs_the_exchange_and_the_change(env):
    client, _, _ = env
    post(client, "/api/submit", {"exercise_id": "p2", "code": SOLUTION, "mode": "blank"})
    ctl = post(client, "/api/control/start", {"exercise_id": "p2"})["control"]
    assert ctl["level"] == 2 and "optional start" in ctl["change"]
    done = answer_all(client, "p2", 3)
    assert done["done"] and done["status"]["control"] is False  # the change is still to do
    right = post(client, "/api/control/change", {"exercise_id": "p2", "code": CHANGED})
    assert right["passed"] and right["status"]["control"] is True and right["status"]["done"] is True


def test_what_if_rounds_are_for_readings_only_and_derived_level_follows_solution_size(env):
    client, _, _ = env
    post(client, "/api/submit", {"exercise_id": "p3", "code": SOLUTION, "mode": "blank"})
    assert post(client, "/api/whatif/start", {"exercise_id": "p3"}, status=400)  # builds are questioned by the interviewer now
    assert post(client, "/api/whatif/start", {"exercise_id": "r1"})["whatif"]["needed"]
    assert "whatif" not in client.get("/api/exercise/p3").json()["control"]
    steps, _ = load_content(env[2])
    by = {e.id: e for s in steps for e in s.exercises}
    assert by["p3"].control_level == 1 and by["lib1"].control_level == 1  # five lines of code
    by["lib1"].solution = "x = 1\n" * 15
    assert by["lib1"].control_level == 2
    by["lib1"].solution = "x = 1\n" * 40
    assert by["lib1"].control_level == 3
    by["lib1"].control = False
    assert by["lib1"].control_level == 0


def test_an_assisted_extra_build_needs_the_interviewer_instead_of_an_explanation(tmp_path):
    root = tmp_path / "c"
    for name, text in files().items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    (root / "t1/exercises/p3/exercise.yaml").write_text("title: Extra\nkind: python\nrequired: false\n")

    def fake(prompt, json_mode=True):
        if "Write exactly" in prompt:
            return json.dumps({"questions": [{"q": f"Why {i}?", "strong": "n"} for i in (1, 2)]})
        if "## Conversation so far" in prompt:
            return json.dumps({"verdict": "good", "reply": "Right.", "follow_up": "", "strong": "s"})
        return "SIZE: small\n\n```python\nx = 1\n```" if not json_mode else "{}"
    client = TestClient(create_app(root, tmp_path / "p.db", call=fake))
    post(client, "/api/chat", {"scope": "p3", "message": "write it"})
    sub = post(client, "/api/submit", {"exercise_id": "p3", "code": SOLUTION, "mode": "blank"})
    assert sub["status"]["assisted"] and sub["status"]["explain"] is False and sub["status"]["done"] is False
    assert len(client.get("/api/interview", params={"exercise_id": "p3", "part": "defend"}).json()["qs"]) == 2
    ok = answer_all(client, "p3", 2)
    assert ok["done"] and ok["status"]["explain"] is True and ok["status"]["done"] is True


def test_what_if_credit_from_before_the_redesign_still_counts(env, tmp_path):
    from gym import db
    client, _, _ = env
    post(client, "/api/submit", {"exercise_id": "p3", "code": SOLUTION, "mode": "blank"})
    conn = db.connect(tmp_path / "p.db")  # the same file the app uses
    db.save_whatif(conn, "p3", 0, [], 0)
    db.set_whatif_ok(conn, "p3", True)
    ctl = client.get("/api/exercise/p3").json()
    assert ctl["status"]["control"] is True and ctl["control"]["asked"] is False  # nothing to ask again


def test_level_three_reading_needs_a_fix_that_prints_the_target(env):
    client, _, _ = env
    ex = client.get("/api/exercise/r3").json()
    assert ex["level"] == 3 and ex["fix"] == "Make it print 6." and ex["questions"] == ["What is wrong?"] and ex["status"]["fix"] is False
    assert post(client, "/api/fix", {"exercise_id": "p3", "code": "x"}, status=400)  # only level 3 readings
    bad = post(client, "/api/fix", {"exercise_id": "r3", "code": "print(sum([1, 2, 3]) - 1)"})
    assert bad["passed"] is False and bad["output"].strip() == "5" and bad["status"]["fix"] is False
    good = post(client, "/api/fix", {"exercise_id": "r3", "code": "print(sum([1, 2, 3]))\n"})
    assert good["passed"] and good["status"]["fix"] is True and good["status"]["done"] is False  # what if and the explanation remain


def test_asking_about_an_answer_works_while_the_check_is_locked_and_never_writes_code(env):
    client, _, _ = env
    post(client, "/api/submit", {"exercise_id": "p3", "code": SOLUTION, "mode": "blank"})
    assert post(client, "/api/control/start", {"exercise_id": "p3"})["control"]["locked"]
    assert post(client, "/api/chat", {"scope": "p3", "message": "why?"}, status=403)  # the assistant is locked
    r = post(client, "/api/chat", {"scope": "p3", "message": "Why did this fail?", "explain_only": True})
    assert r["assisted"] is False and r["locked"] is True and len(r["messages"]) == 2  # still locked for everything else
