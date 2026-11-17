import json
import re

import pytest
from fastapi.testclient import TestClient

from gym.app import create_app

QUIZ = ("- q: Which tool tracks experiments?\n  options: [Docker, MLflow]\n  answer: 1\n  why: MLflow logs runs.\n"
        "- q: Which one is a container tool?\n  options: [Docker, MLflow]\n  answer: 0\n  why: Docker builds containers.\n")
GOOD = "def slugify(s):\n    return '-'.join(s.lower().split())\n"
BAD = "def slugify(s):\n    return '-'.join(s.split())\n"
TESTS = "from solution import slugify\n\ndef test_a():\n    assert slugify('A b') == 'a-b'\n"


def fake_gemini(prompt):
    n = int(re.search(r"Return exactly (\d+) scores", prompt).group(1))
    return json.dumps({"scores": [4] * n, "verdict": "ok", "feedback": "fine"})


@pytest.fixture
def client(tmp_path):
    step = tmp_path / "c" / "01-s"
    (step / "step.yaml").parent.mkdir(parents=True)
    (step / "step.yaml").write_text("title: S\norder: 1\n")
    files = {
        "quiz1/exercise.yaml": "title: Q\nkind: quiz\npass_ratio: 1.0\n",
        "quiz1/prompt.md": "intro", "quiz1/quiz.yaml": QUIZ,
        "t1/exercise.yaml": "title: T\nkind: tests\n", "t1/prompt.md": "Test slugify.",
        "t1/starter.py": "from solution import slugify\n", "t1/solution.py": TESTS,
        "t1/impl_good.py": GOOD, "t1/impl_bad_1.py": BAD,
        "p1/guide.md": "GUIDE", "p1/exercise.yaml": "title: P\nkind: python\n", "p1/prompt.md": "p", "p1/solution.py": "x = 1\n",
        "p1/starter.py": "pass\n", "p1/hint.md": "HINT", "p1/say.md": "SAY", "p1/model_prompt.md": "MP",
        "p1/tests/test_hidden.py": "def test_ok():\n    import solution\n    assert solution.x == 1\n",
    }
    for name, text in files.items():
        path = step / "exercises" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    return TestClient(create_app(tmp_path / "c", tmp_path / "p.db", call=fake_gemini))


def test_quiz_payload_hides_answers_and_grades(client):
    ex = client.get("/api/exercise/quiz1").json()
    assert ex["modes"] == [] and ex["quiz"][0]["options"] == ["Docker", "MLflow"]
    assert "answer" not in ex["quiz"][0] and "why" not in ex["quiz"][0]
    wrong = client.post("/api/quiz", json={"exercise_id": "quiz1", "answers": [0, 0]}).json()
    assert not wrong["passed"] and wrong["correct"] == 1 and wrong["results"][0]["why"] == "MLflow logs runs."
    right = client.post("/api/quiz", json={"exercise_id": "quiz1", "answers": [1, 0]}).json()
    assert right["passed"] and right["status"]["tests"] is True


def test_quiz_bad_requests(client):
    assert client.post("/api/quiz", json={"exercise_id": "quiz1", "answers": [1]}).status_code == 400
    assert client.post("/api/quiz", json={"exercise_id": "p1", "answers": []}).status_code == 400


def test_tests_kind_flow(client):
    ex = client.get("/api/exercise/t1").json()
    assert ex["modes"] == ["blank", "challenge"]
    run = client.post("/api/run", json={"exercise_id": "t1", "code": TESTS}).json()
    assert run["passed"] and [t["name"] for t in run["tests"]] == [
        "passes on the correct implementation", "catches bug 1"]
    assert client.get("/api/exercise/t1").json()["status"]["tests"] is False  # run records nothing
    sub = client.post("/api/submit", json={"exercise_id": "t1", "code": TESTS, "mode": "blank"}).json()
    assert sub["passed"] and sub["status"]["tests"] is True


def test_hint_always_say_and_model_prompt_after_pass(client):
    before = client.get("/api/exercise/p1").json()
    assert before["hint"] == "HINT" and before["say"] == "" and before["model_prompt"] == ""
    client.post("/api/submit", json={"exercise_id": "p1", "code": "x = 1\n", "mode": "blank"})
    after = client.get("/api/exercise/p1").json()
    assert after["say"] == "SAY" and after["model_prompt"] == "MP"
    assert after["guide"] == "GUIDE" and after["reference"] == "x = 1\n"


def test_guide_and_reference_stay_hidden_until_passed(client):
    before = client.get("/api/exercise/p1").json()
    assert before["guide"] == "" and before["reference"] == ""
    client.post("/api/submit", json={"exercise_id": "p1", "code": "x = 2\n", "mode": "blank"})  # fails its test
    assert client.get("/api/exercise/p1").json()["reference"] == ""


def test_reference_for_tests_kind_is_the_reference_test_file(client):
    client.post("/api/submit", json={"exercise_id": "t1", "code": TESTS, "mode": "blank"})
    assert client.get("/api/exercise/t1").json()["reference"] == TESTS


def test_sql_schema_hides_insert_lines(tmp_path):
    step = tmp_path / "c" / "01-s"
    ex = step / "exercises" / "s1"
    ex.mkdir(parents=True)
    (step / "step.yaml").write_text("title: S\norder: 1\n")
    (ex / "exercise.yaml").write_text("title: S\nkind: sql\n")
    (ex / "prompt.md").write_text("p")
    (ex / "solution.sql").write_text("SELECT 1;")
    (ex / "seed.sql").write_text("CREATE TABLE t (x INTEGER);\nINSERT INTO t VALUES (1);\n")
    client = TestClient(create_app(tmp_path / "c", tmp_path / "p.db", call=fake_gemini))
    assert client.get("/api/exercise/s1").json()["schema"] == "CREATE TABLE t (x INTEGER);"
