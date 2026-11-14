# Live Coding Gym Content Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. Also follow `CLAUDE.md`: ponytail, graphify (`graphify update .` before every commit that touches files), caveman replies.

**Goal:** Fill the finished app with the full 12-step learning journey: extend the app so it can host every kind of exercise the journey needs, migrate the 55 drills, 12 lessons and 40 flashcards of the old single-file gym, and author the new content so that a learner who finishes every gate is ready for the target interview.

**Architecture:** Content stays plain files under `content/<NN-step>/` (spec section 5). Part 1 adds the few app features content needs (hint and "say it" panels, shared datasets, quizzes, test-writing exercises, stronger content checks). Part 2 builds a shared synthetic dataset and a one-off migration script. Part 3 is authoring: one task per step, each gated by `uv run python -m gym.check_content`.

**Tech Stack:** unchanged (Python 3.12 via uv, FastAPI, pytest, SQLite, pandas, scikit-learn, Gemini over REST, plain JS page).

**Spec:** `docs/superpowers/specs/2026-11-14-live-coding-gym-design.md`. App plan already executed: `docs/superpowers/plans/2026-11-14-live-coding-gym-app.md`.

## Global Constraints

- Run all commands from `/Users/surface/Documents/Monica/live-coding-gym` with `uv` (Python 3.12). Never use the system Python 3.9.
- Never print, log, commit or copy the Gemini key in `.env`.
- Content lives in `content/` as plain files. App code never contains lesson or exercise text.
- **No exercise ships if its own solution fails its own tests.** `uv run python -m gym.check_content` must print `content ok` before every content commit. If it fails, fix the content, never the checker (unless the checker itself is wrong, and then add a test first).
- Run `uv run pytest` before every commit. A failing test blocks the commit.
- Learner profile (drives every content decision): knows Python and SQL theory, has coded with AI tools from the start, cannot yet write code by hand. Target: iFood live coding on Coderbyte, robust deterministic ML-systems code in Python, AI assistant allowed but the prompt and the explanation are judged.
- Content language is English. Prompts, lessons and model answers use plain, short sentences. Step 11 adds an optional Portuguese phrase bank, because the interview may be held in Portuguese.
- Exercise ids are global (the app keys on them): every id is unique across all steps. Use the prefixes given in each task.
- Code runs under CPython 3.12 in a temp directory with a 10 second limit. Hidden tests must be deterministic: no network, no wall-clock sleeps, no unseeded randomness. Inject clocks and sleeps instead.
- SQL runs on SQLite (window functions work). Lessons say where other dialects differ.
- Commit messages end with: `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` (use whichever model attribution the session's reminder gives).

## Journey (fixed folder names and gates)

| Folder | Step | Gate (`min_score`, `timed_required`) |
|---|---|---|
| `01-hand-python` | Hand-coding Python from zero | 4, true |
| `02-live-routine` | The live-coding routine | 4, true |
| `03-hand-sql` | Hand-coding SQL | 4, true |
| `04-robust-code` | Robust code | 4, false |
| `05-testing` | Testing your own code | 4, false |
| `06-real-data` | Real data behaviour and statistics | 4, false |
| `07-ml-tools` | AI/ML engineering tools tour (theory and examples) | 4, false |
| `08-production-ml` | Production ML systems | 4, false |
| `09-model-failures` | Common model failures | 4, false |
| `10-ai-assistant` | Using an AI assistant while observed | 4, false |
| `11-explaining` | Explaining your code | 4, false |
| `12-mock-rounds` | Mock rounds and readiness | n/a (no required exercises; the readiness score from three finished mocks is its gate) |

## Priority order

The interview date is not known, so build in the order that attacks the biggest gap first and keeps the app usable after every phase.

1. Phase 1: Part 1 (app extensions), Part 2 (dataset and migration). After this the learner can already practise 51 migrated drills.
2. Phase 2: steps 1, 2, 3 (hand-coding gap).
3. Phase 3: steps 4, 8, 9, 10, 11 (what the interview actually tests).
4. Phase 4: steps 5, 6, 7, 12.

If the interview is within a week, stop after Phase 3 and use the mock rounds.

## File Structure

| File | Responsibility |
|---|---|
| `gym/content.py` | Modify: new exercise fields and kinds. |
| `gym/runner.py` | Modify: data files for Python tests, test-writing runner. |
| `gym/gates.py`, `gym/reviewer.py`, `gym/app.py` | Modify: quiz and tests kinds, extras in payload. |
| `gym/check_content.py` | Modify: stricter checks. |
| `web/app.js` | Modify: quiz view, hint and "say it" panels. |
| `tools/make_delivery_data.py` | Create: deterministic shared dataset. |
| `tools/extract_old_gym.js`, `tools/old_gym.json` | Create: one-off export of the old gym's content. |
| `tools/migrate_old_gym.py` | Create: one-off migration into `content/`. |
| `content/_shared/` | Create: `delivery.sql`, `orders.csv`, `restaurants.csv`, `customers.csv`, `couriers.csv`. |
| `content/<NN-step>/` | Create: all journey content. |
| `tests/test_content_extras.py`, `tests/test_runner_tests_kind.py`, `tests/test_app_kinds.py`, `tests/test_delivery_data.py`, `tests/test_migrate.py` | Create. |

---

# Part 1: App extensions

### Task 1: Content model

**Files:**
- Modify: `gym/content.py`
- Test: `tests/test_content_extras.py`

**Interfaces:**
- Produces: `Exercise` gains `hint: str`, `say: str`, `model_prompt: str` (read from `hint.md`, `say.md`, `model_prompt.md`, empty if absent), `files: list[Path]` (from `files:` in `exercise.yaml`, paths relative to the exercise folder, must exist), `wrong: dict[str, str]` (python only; every `wrong/*.py`, name without extension), `quiz: list[dict]` and `pass_ratio: float` (quiz only), `impl_good: str` and `impls_bad: dict[str, str]` (tests kind only).
- Produces: new kinds `quiz` and `tests` in `KINDS`. SQL exercises may use `seed_file: <relative path>` instead of `seed.sql`. `tests` exercises use `starter.py` (a test-file skeleton) and `solution.py` (the reference test file).
- A `quiz.yaml` is a list of `{q, options, answer, why}` where `answer` is the index into `options`.

- [ ] **Step 1: Write the failing test**

`tests/test_content_extras.py`:

```python
import pytest

from gym.content import load_content


def build(tmp_path, kind, files, meta=""):
    """One step with one exercise 'e1'. files maps path-under-exercise -> text."""
    step = tmp_path / "01-s"
    ex = step / "exercises" / "e1"
    ex.mkdir(parents=True, exist_ok=True)
    (step / "step.yaml").write_text("title: S\norder: 1\n")
    (ex / "exercise.yaml").write_text(f"title: E\nkind: {kind}\n{meta}")
    (ex / "prompt.md").write_text("p")
    for name, text in files.items():
        path = ex / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    return tmp_path


def load_one(tmp_path):
    steps, errors = load_content(tmp_path)
    return (steps[0].exercises[0] if steps[0].exercises else None), errors


PY = {"solution.py": "x = 1\n", "tests/test_hidden.py": "def test_a():\n    pass\n"}


def test_extras_and_wrong_solutions(tmp_path):
    build(tmp_path, "python", {**PY, "hint.md": "H", "say.md": "S", "model_prompt.md": "M",
                               "wrong/off_by_one.py": "x = 2\n"})
    ex, errors = load_one(tmp_path)
    assert errors == []
    assert (ex.hint, ex.say, ex.model_prompt) == ("H", "S", "M")
    assert ex.wrong == {"off_by_one": "x = 2\n"}


def test_files_are_resolved_and_must_exist(tmp_path):
    (tmp_path / "_shared").mkdir()
    (tmp_path / "_shared" / "data.csv").write_text("a\n1\n")
    build(tmp_path, "python", PY, meta="files:\n  - ../../../_shared/data.csv\n")
    ex, errors = load_one(tmp_path)
    assert errors == [] and [p.name for p in ex.files] == ["data.csv"]
    build(tmp_path, "python", PY, meta="files:\n  - ../../../_shared/missing.csv\n")
    ex, errors = load_one(tmp_path)
    assert ex is None and "missing.csv" in errors[0]


def test_sql_seed_file(tmp_path):
    (tmp_path / "_shared").mkdir()
    (tmp_path / "_shared" / "s.sql").write_text("CREATE TABLE t (x);\n")
    build(tmp_path, "sql", {"solution.sql": "SELECT 1;"}, meta="seed_file: ../../../_shared/s.sql\n")
    ex, errors = load_one(tmp_path)
    assert errors == [] and "CREATE TABLE t" in ex.seed


def test_quiz_loads_and_rejects_bad_answer_index(tmp_path):
    good = "- q: Which?\n  options: [a, b]\n  answer: 1\n  why: because\n"
    build(tmp_path, "quiz", {"quiz.yaml": good}, meta="pass_ratio: 1.0\n")
    ex, errors = load_one(tmp_path)
    assert errors == [] and ex.pass_ratio == 1.0 and ex.quiz[0]["answer"] == 1
    build(tmp_path, "quiz", {"quiz.yaml": good.replace("answer: 1", "answer: 5")})
    ex, errors = load_one(tmp_path)
    assert ex is None and "answer out of range" in errors[0]


def test_tests_kind_needs_good_and_bad_implementations(tmp_path):
    files = {"starter.py": "from solution import f\n", "solution.py": "from solution import f\n",
             "impl_good.py": "def f(): return 1\n", "impl_bad_1.py": "def f(): return 2\n"}
    build(tmp_path, "tests", files)
    ex, errors = load_one(tmp_path)
    assert errors == [] and ex.impl_good.startswith("def f") and list(ex.impls_bad) == ["impl_bad_1"]
    (tmp_path / "01-s" / "exercises" / "e1" / "impl_bad_1.py").unlink()
    ex, errors = load_one(tmp_path)
    assert ex is None and "impl_bad" in errors[0]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_content_extras.py -v`
Expected: FAIL (`AttributeError: ... 'hint'` and `unknown kind 'quiz'`)

- [ ] **Step 3: Write the implementation**

In `gym/content.py` change the constants and the `Exercise` dataclass:

```python
KINDS = {"python", "sql", "open", "prompt", "explain", "quiz", "tests"}
EXT = {"python": "py", "sql": "sql", "tests": "py"}
```

Add these fields at the end of `Exercise` (after `rubric`):

```python
    hint: str = ""
    say: str = ""
    model_prompt: str = ""
    files: list = field(default_factory=list)
    wrong: dict = field(default_factory=dict)
    quiz: list = field(default_factory=list)
    pass_ratio: float = 0.8
    impl_good: str = ""
    impls_bad: dict = field(default_factory=dict)
```

Replace `load_exercise` entirely:

```python
def _existing(path):
    if not path.exists():
        raise ValueError(f"file not found: {path}")
    return path


def load_exercise(d, step_id):
    meta = yaml.safe_load((d / "exercise.yaml").read_text())
    kind = meta["kind"]
    if kind not in KINDS:
        raise ValueError(f"unknown kind {kind!r}")
    ex = Exercise(
        id=d.name,
        step_id=step_id,
        title=meta["title"],
        kind=kind,
        prompt=(d / "prompt.md").read_text(),
        dir=d,
        time_limit_s=meta.get("time_limit_s", 600),
        required=meta.get("required", True),
        review=meta.get("review", False),
        mock=meta.get("mock", False),
        ordered=meta.get("ordered", False),
        rubric=meta.get("rubric") or [],
        hint=_read(d / "hint.md"),
        say=_read(d / "say.md"),
        model_prompt=_read(d / "model_prompt.md"),
        pass_ratio=meta.get("pass_ratio", 0.8),
        files=[_existing((d / f).resolve()) for f in meta.get("files", [])],
    )
    ext = EXT.get(kind)
    if ext:
        ex.starter = _read(d / f"starter.{ext}")
        ex.solution = (d / f"solution.{ext}").read_text()
        ex.gaps = _read(d / f"gaps.{ext}")
    if kind == "python":
        if not (d / "tests" / "test_hidden.py").exists():
            raise ValueError("missing tests/test_hidden.py")
        ex.wrong = {p.stem: p.read_text() for p in sorted((d / "wrong").glob("*.py"))}
    if kind == "sql":
        seed = d / meta["seed_file"] if "seed_file" in meta else d / "seed.sql"
        ex.seed = _existing(seed.resolve()).read_text()
    if kind == "tests":
        ex.impl_good = (d / "impl_good.py").read_text()
        ex.impls_bad = {p.stem: p.read_text() for p in sorted(d.glob("impl_bad_*.py"))}
        if not ex.impls_bad:
            raise ValueError("a tests exercise needs at least one impl_bad_*.py")
    if kind == "quiz":
        ex.quiz = yaml.safe_load((d / "quiz.yaml").read_text())
        for i, q in enumerate(ex.quiz, 1):
            if not 0 <= q["answer"] < len(q["options"]):
                raise ValueError(f"quiz question {i}: answer out of range")
    return ex
```

- [ ] **Step 4: Run test to verify it passes, then the whole suite**

Run: `uv run pytest -q`
Expected: all pass (64 existing + 5 new)

- [ ] **Step 5: Commit**

```bash
graphify update .
git add -A && git commit -m "feat: content model for hints, shared data, quiz and tests kinds"
```

---

### Task 2: Runner extensions

**Files:**
- Modify: `gym/runner.py`
- Test: `tests/test_runner_tests_kind.py`

**Interfaces:**
- Consumes: `RunResult` (existing).
- Produces: `run_python_tests(code, tests_dir, timeout=10, files=())`: every path in `files` is copied beside `solution.py`, so tests can open it by file name. `run_test_writing(test_code: str, good: str, bads: dict[str, str], timeout: int = 10) -> RunResult`: runs the learner's test file against the good implementation (must pass with at least one test collected, pytest exit code 0) and against each bad one (must fail, exit code 1). `tests` is `[{"name": "passes on the correct implementation", ...}, {"name": "catches bug 1", ...}, ...]` (bug names come from `impl_bad_N`); `output` is the pytest output of the good run; `timed_out` is true if the good run timed out. A bad implementation only counts as caught when the good run passed.

- [ ] **Step 1: Write the failing test**

`tests/test_runner_tests_kind.py`:

```python
from gym.runner import run_python_tests, run_test_writing

GOOD = "def slugify(s):\n    return '-'.join(s.lower().split())\n"
BADS = {
    "impl_bad_1": "def slugify(s):\n    return '-'.join(s.split())\n",
    "impl_bad_2": "def slugify(s):\n    return s.lower().replace(' ', '-')\n",
}
FULL = ("from solution import slugify\n\n"
        "def test_lower():\n    assert slugify('Hello World') == 'hello-world'\n\n"
        "def test_spaces():\n    assert slugify('a  b') == 'a-b'\n")
WEAK = ("from solution import slugify\n\n"
        "def test_lower():\n    assert slugify('Hello World') == 'hello-world'\n")


def names(r):
    return {t["name"]: t["passed"] for t in r.tests}


def test_complete_tests_catch_every_bug():
    r = run_test_writing(FULL, GOOD, BADS)
    assert r.passed
    assert names(r) == {"passes on the correct implementation": True, "catches bug 1": True, "catches bug 2": True}


def test_weak_tests_miss_a_bug():
    r = run_test_writing(WEAK, GOOD, BADS)
    assert not r.passed
    assert names(r)["catches bug 1"] is True and names(r)["catches bug 2"] is False


def test_tests_that_fail_on_the_good_implementation_earn_nothing():
    wrong = "from solution import slugify\n\ndef test_x():\n    assert slugify('A b') == 'A_b'\n"
    r = run_test_writing(wrong, GOOD, BADS)
    assert not any(names(r).values()) and "assert" in r.output


def test_empty_or_broken_test_files_fail():
    assert not run_test_writing("x = 1\n", GOOD, BADS).passed
    assert not run_test_writing("def (:\n", GOOD, BADS).passed


def test_hanging_test_times_out():
    r = run_test_writing("while True:\n    pass\n", GOOD, BADS, timeout=3)
    assert not r.passed and r.timed_out


def test_data_files_are_copied_beside_the_solution(tmp_path):
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_hidden.py").write_text(
        "def test_reads():\n    assert open('data.txt').read() == 'hi'\n")
    data = tmp_path / "data.txt"
    data.write_text("hi")
    assert run_python_tests("x = 1\n", tests, files=[data]).passed
    assert not run_python_tests("x = 1\n", tests).passed
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_runner_tests_kind.py -v`
Expected: FAIL (`ImportError: cannot import name 'run_test_writing'`)

- [ ] **Step 3: Write the implementation**

In `gym/runner.py` change the signature and add the copy loop in `run_python_tests`:

```python
def run_python_tests(code, tests_dir, timeout=10, files=()):
    """Run hidden pytest tests against a submission saved as solution.py."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "solution.py").write_text(code)
        shutil.copytree(tests_dir, tmp / "tests")
        for f in files:
            shutil.copy(f, tmp / Path(f).name)
```

(the rest of the function is unchanged). Append:

```python
def _pytest(files, timeout):
    """Run pytest on test_candidate.py in a temp dir holding `files` (name -> text)."""
    with tempfile.TemporaryDirectory() as tmp:
        for name, text in files.items():
            (Path(tmp) / name).write_text(text)
        cmd = [sys.executable, "-m", "pytest", "-q", "--tb=short", "-p", "no:cacheprovider", "test_candidate.py"]
        try:
            proc = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return None, f"Timed out after {timeout}s"
        return proc.returncode, proc.stdout + proc.stderr


def run_test_writing(test_code, good, bads, timeout=10):
    """Grade a learner's test file: it must pass on `good` and fail on every `bads` implementation."""
    rc, output = _pytest({"solution.py": good, "test_candidate.py": test_code}, timeout)
    good_ok = rc == 0  # exit code 5 (no tests collected) and 2 (import error) do not count
    tests = [{"name": "passes on the correct implementation", "passed": good_ok}]
    for name, bad in bads.items():
        caught = False
        if good_ok:
            bad_rc, _ = _pytest({"solution.py": bad, "test_candidate.py": test_code}, timeout)
            caught = bad_rc == 1
        tests.append({"name": "catches " + name.replace("impl_bad_", "bug "), "passed": caught})
    return RunResult(all(t["passed"] for t in tests), tests, output, rc is None)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest -q`
Expected: all pass

- [ ] **Step 5: Commit**

```bash
graphify update .
git add -A && git commit -m "feat: data files for Python tests and the test-writing runner"
```

---

### Task 3: Quiz and tests kinds in the API and gates

**Files:**
- Modify: `gym/gates.py`, `gym/reviewer.py`, `gym/app.py`
- Test: `tests/test_app_kinds.py`

**Interfaces:**
- Consumes: Task 1 fields, Task 2 runners.
- Produces: `reviewer.REVIEW_KIND["tests"] = "code"` (quiz has no review kind). `gates` treats `python`, `sql`, `quiz`, `tests` as tested kinds. API: `POST /api/quiz {exercise_id, answers: [int]}` returns `{passed, correct, total, results: [{correct, answer, why}], attempt_id, status}` (400 if the exercise is not a quiz or the answer count is wrong). The exercise payload gains `hint`, `say` and `model_prompt` (the last two are `""` until the exercise has a passing tests result or a finished review), `quiz` (`[{q, options}]`, answers withheld) and `pass_ratio`; `schema` now holds only the non-INSERT lines of the seed. Modes: python `retype, gaps (if gaps file), blank, timed`; sql the same; tests `blank, timed`; others none. `POST /api/run` on a tests exercise runs the grader without recording an attempt. `POST /api/submit` accepts python, sql, tests. `POST /api/review` on a kind with no review returns 400.

- [ ] **Step 1: Write the failing test**

`tests/test_app_kinds.py`:

```python
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
        "p1/exercise.yaml": "title: P\nkind: python\n", "p1/prompt.md": "p", "p1/solution.py": "x = 1\n",
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
    assert client.post("/api/review", json={"exercise_id": "quiz1"}).status_code == 400


def test_tests_kind_flow(client):
    ex = client.get("/api/exercise/t1").json()
    assert ex["modes"] == ["blank", "timed"]
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_app_kinds.py -v`
Expected: FAIL (`KeyError`/404 on `/api/quiz`, missing `hint`)

- [ ] **Step 3: Write the implementation**

`gym/reviewer.py`: change `REVIEW_KIND` to

```python
REVIEW_KIND = {"python": "code", "sql": "code", "tests": "code", "explain": "explain",
               "prompt": "prompt", "open": "open"}
```

`gym/gates.py`: replace `coded = ex.kind in ("python", "sql")` with `coded = ex.kind in TESTED` and add `TESTED = ("python", "sql", "quiz", "tests")` below the imports. (`_review_ok` stays: it is only called for kinds that have a review kind.)

`gym/app.py`:

1. `CODED = ("python", "sql", "tests")` and add `MODES = {"python": ["retype", "gaps", "blank", "timed"], "sql": ["retype", "gaps", "blank", "timed"], "tests": ["blank", "timed"]}` below it. Add the body model:

```python
class QuizBody(BaseModel):
    exercise_id: str
    answers: list[int]
```

2. Replace `payload`:

```python
    def payload(ex, mode="blank"):
        st = status_of(ex)
        revealed = st["tests"] is True or st["review"] is True
        rk = reviewer.REVIEW_KIND.get(ex.kind)
        modes = [m for m in MODES.get(ex.kind, []) if m != "gaps" or ex.gaps]
        code = {"retype": "", "gaps": ex.gaps}.get(mode, ex.starter)
        schema = "\n".join(l for l in ex.seed.splitlines() if not l.startswith("INSERT"))
        return {"id": ex.id, "title": ex.title, "kind": ex.kind, "prompt": ex.prompt,
                "time_limit_s": ex.time_limit_s, "modes": modes, "mode": mode, "code": code,
                "solution": ex.solution if mode == "retype" else "", "schema": schema,
                "hint": ex.hint, "say": ex.say if revealed else "",
                "model_prompt": ex.model_prompt if revealed else "",
                "quiz": [{"q": q["q"], "options": q["options"]} for q in ex.quiz],
                "pass_ratio": ex.pass_ratio, "status": st,
                "review": review_dict(db.latest_review(conn, ex.id, rk)) if rk else None}
```

3. Replace `grade`:

```python
    def grade(ex, code):
        if ex.kind == "python":
            return runner.run_python_tests(code, ex.dir / "tests", files=ex.files)
        if ex.kind == "tests":
            return runner.run_test_writing(code, ex.impl_good, ex.impls_bad)
        return runner.check_sql(ex.seed, code, ex.solution, ex.ordered)
```

4. In `run`, add as the first line after `ex = get_ex(...)`: `if ex.kind == "tests": return asdict(grade(ex, body.code))`.

5. In `review`, replace the first two lines with:

```python
        ex = get_ex(body.exercise_id)
        kind = reviewer.REVIEW_KIND.get(ex.kind)
        if kind is None:
            raise HTTPException(400, "this exercise has no review")
```

   and use `kind` where the function currently calls `reviewer.REVIEW_KIND[ex.kind]`. In `retry`, change `reviewer.REVIEW_KIND[ex.kind] == row["kind"]` to `reviewer.REVIEW_KIND.get(ex.kind) == row["kind"]`.

6. Add the quiz route (before `cards_due`):

```python
    @app.post("/api/quiz")
    def quiz(body: QuizBody):
        ex = get_ex(body.exercise_id)
        if ex.kind != "quiz":
            raise HTTPException(400, "this exercise is not a quiz")
        if len(body.answers) != len(ex.quiz):
            raise HTTPException(400, "answer every question")
        results = [{"correct": a == q["answer"], "answer": q["answer"], "why": q.get("why", "")}
                   for q, a in zip(ex.quiz, body.answers)]
        correct = sum(r["correct"] for r in results)
        passed = correct / len(ex.quiz) >= ex.pass_ratio
        attempt_id = db.record_attempt(conn, ex.id, "blank", json.dumps(body.answers), passed,
                                       0, f"{correct}/{len(ex.quiz)}")
        return {"passed": passed, "correct": correct, "total": len(ex.quiz), "results": results,
                "attempt_id": attempt_id, "status": status_of(ex)}
```

- [ ] **Step 4: Run the whole suite**

Run: `uv run pytest -q`
Expected: all pass (the existing `test_app.py` assertions still hold: `modes` for the fixture python and sql exercises are unchanged, `schema` still contains `CREATE TABLE`).

- [ ] **Step 5: Commit**

```bash
graphify update .
git add -A && git commit -m "feat: quiz and test-writing exercises, hint and say-it payload"
```

---

### Task 4: Stricter content checker

**Files:**
- Modify: `gym/check_content.py`
- Modify fixtures: add `hint.md` and `say.md` to `tests/fixtures/content/01-hand-python/exercises/count-words/`, `tests/fixtures/content/03-hand-sql/exercises/top-customers/` (both files each) and `say.md` to `tests/fixtures/content/01-hand-python/exercises/explain-count-words/`; add `wrong/forgets_lowercase.py` (`def count_words(text):\n    counts = {}\n    for w in text.split():\n        counts[w] = counts.get(w, 0) + 1\n    return counts\n`) to `count-words`.
- Test: `tests/test_check_content.py` (extend)

**Interfaces:**
- Consumes: Task 1 fields, Task 2 runners.
- Produces: `check(content_dir) -> list[str]` now also reports: duplicate exercise ids across steps, duplicate card ids across steps, a `wrong/` solution that passes the tests, a `tests` exercise whose reference test file do not catch every bug or whose starter already passes, a missing `say.md` on any non-quiz exercise, a missing `hint.md` on python, sql and tests exercises.

- [ ] **Step 1: Add the fixture files, then write the failing tests**

Append to `tests/test_check_content.py`:

```python
def test_duplicate_exercise_id_is_reported(tmp_path):
    shutil.copytree(FIXTURES, tmp_path / "c")
    shutil.copytree(tmp_path / "c" / "01-hand-python" / "exercises" / "count-words",
                    tmp_path / "c" / "03-hand-sql" / "exercises" / "count-words")
    assert any("duplicate exercise id" in p for p in check(tmp_path / "c"))


def test_wrong_solution_that_passes_is_reported(tmp_path):
    shutil.copytree(FIXTURES, tmp_path / "c")
    ex = tmp_path / "c" / "01-hand-python" / "exercises" / "count-words"
    shutil.copy(ex / "solution.py", ex / "wrong" / "actually_right.py")
    problems = check(tmp_path / "c")
    assert len(problems) == 1 and "wrong solution actually_right passes" in problems[0]


def test_missing_say_and_hint_are_reported(tmp_path):
    shutil.copytree(FIXTURES, tmp_path / "c")
    ex = tmp_path / "c" / "01-hand-python" / "exercises" / "count-words"
    (ex / "say.md").unlink()
    (ex / "hint.md").unlink()
    problems = check(tmp_path / "c")
    assert sorted(p.split(": ", 1)[1] for p in problems) == ["missing hint.md", "missing say.md"]


def test_tests_kind_checks(tmp_path):
    step = tmp_path / "c" / "01-s"
    ex = step / "exercises" / "t1"
    ex.mkdir(parents=True)
    (step / "step.yaml").write_text("title: S\norder: 1\n")
    files = {"exercise.yaml": "title: T\nkind: tests\n", "prompt.md": "p", "hint.md": "h", "say.md": "s",
             "starter.py": "from solution import f\n",
             "solution.py": "from solution import f\n\ndef test_f():\n    assert f() == 1\n",
             "impl_good.py": "def f(): return 1\n", "impl_bad_1.py": "def f(): return 2\n"}
    for name, text in files.items():
        (ex / name).write_text(text)
    assert check(tmp_path / "c") == []
    (ex / "solution.py").write_text("from solution import f\n\ndef test_f():\n    assert f() in (1, 2)\n")
    assert any("do not catch every bug" in p for p in check(tmp_path / "c"))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_check_content.py -v`
Expected: FAIL on the four new tests

- [ ] **Step 3: Write the implementation**

Replace `gym/check_content.py`:

```python
import sys

from . import config
from .content import load_content
from .runner import check_sql, run_python_tests, run_test_writing


def check_exercise(ex):
    p = []
    if ex.kind != "quiz" and not ex.say:
        p.append(f"{ex.id}: missing say.md")
    if ex.kind in ("python", "sql", "tests") and not ex.hint:
        p.append(f"{ex.id}: missing hint.md")
    if ex.kind == "python":
        if not run_python_tests(ex.solution, ex.dir / "tests", files=ex.files).passed:
            p.append(f"{ex.id}: reference solution fails its own tests")
        if ex.starter and run_python_tests(ex.starter, ex.dir / "tests", files=ex.files).passed:
            p.append(f"{ex.id}: starter already passes the tests")
        for name, code in ex.wrong.items():
            if run_python_tests(code, ex.dir / "tests", files=ex.files).passed:
                p.append(f"{ex.id}: wrong solution {name} passes the tests")
    elif ex.kind == "sql":
        if not check_sql(ex.seed, ex.solution, ex.solution, ex.ordered).passed:
            p.append(f"{ex.id}: reference solution fails to run")
    elif ex.kind == "tests":
        if not run_test_writing(ex.solution, ex.impl_good, ex.impls_bad).passed:
            p.append(f"{ex.id}: reference tests do not catch every bug (or fail on the good implementation)")
        if ex.starter and run_test_writing(ex.starter, ex.impl_good, ex.impls_bad).passed:
            p.append(f"{ex.id}: starter already passes")
    return p


def check(content_dir):
    steps, problems = load_content(content_dir)
    problems = list(problems)
    seen_ex, seen_cards = {}, {}
    for step in steps:
        for card in step.cards:
            if card["id"] in seen_cards:
                problems.append(f"card {card['id']}: duplicate id (also in {seen_cards[card['id']]})")
            seen_cards[card["id"]] = step.id
        for ex in step.exercises:
            if ex.id in seen_ex:
                problems.append(f"{ex.id}: duplicate exercise id (also in {seen_ex[ex.id]})")
            seen_ex[ex.id] = step.id
            problems += check_exercise(ex)
    return problems


if __name__ == "__main__":
    found = check(config.CONTENT_DIR)
    print("\n".join(found) if found else "content ok")
    sys.exit(1 if found else 0)
```

The three existing tests in `tests/test_check_content.py` keep passing because of the fixture additions in Step 1. Also copy the new fixture files into `content/` (`cp -R tests/fixtures/content/. content/` is wrong: only copy the five new files into the same paths under `content/`).

- [ ] **Step 4: Run test to verify it passes, then commit**

Run: `uv run pytest -q && uv run python -m gym.check_content`
Expected: all pass, `content ok`

```bash
graphify update .
git add -A && git commit -m "feat: stricter content checks"
```

---

### Task 5: Page updates (quiz, hint, say-it panels)

**Files:**
- Modify: `web/app.js`

No automated tests (plain page); verified by hand in Step 3.

- [ ] **Step 1: Add the helpers**

Insert after the `reviewBox` function in `web/app.js`:

```javascript
function extrasPanel(ex) {
  const wrap = h("div");
  if (ex.hint) wrap.append(h("details", {}, h("summary", {}, "Hint"), md(ex.hint)));
  if (ex.say) wrap.append(h("details", {}, h("summary", {}, "How to say it out loud"), md(ex.say)));
  if (ex.model_prompt) wrap.append(h("details", {}, h("summary", {}, "A good prompt for an AI assistant"), md(ex.model_prompt)));
  return wrap;
}

function quizView(ex) {
  const picks = ex.quiz.map(() => null);
  const note = h("div");
  const boxes = ex.quiz.map((q, i) => h("div", { class: "review" },
    h("p", {}, h("strong", {}, `${i + 1}. ${q.q}`)),
    q.options.map((o, j) => h("label", { style: "display:block" },
      h("input", { type: "radio", name: `q${i}`, onchange: () => { picks[i] = j; } }), " " + o))));
  main.append(...boxes, h("div", { class: "bar" },
    h("button", { onclick: async () => {
      if (picks.includes(null)) { note.replaceChildren(h("p", { class: "bad" }, "Answer every question.")); return; }
      const r = await api("/quiz", { exercise_id: ex.id, answers: picks });
      r.results.forEach((res, i) => boxes[i].append(h("p", { class: res.correct ? "ok" : "bad" },
        (res.correct ? "✓ " : `✗ right answer: ${ex.quiz[i].options[res.answer]}. `) + res.why)));
      note.replaceChildren(h("p", {}, `${r.correct}/${r.total}. ` +
        (r.passed ? "Passed." : "Not yet: read the explanations, then try again."),
        h("button", { onclick: route }, "Try again")));
    } }, "Submit answers")), note);
}
```

- [ ] **Step 2: Wire them into `exView`**

Make these exact edits in `exView`:

1. After `const ex = await api(...)` and `const coded = ...` add:

```javascript
  if (ex.kind === "quiz") { main.append(h("h1", {}, ex.title), md(ex.prompt)); return quizView(ex); }
```

2. After `const reviewSlot = h("div");` add:

```javascript
  const extras = h("div");
  const refreshExtras = async () => extras.replaceChildren(extrasPanel(await api(`/exercise/${id}?mode=${mode}`)));
  refreshExtras();
```

3. Replace the `showReview` definition with:

```javascript
  const showReview = (rev) => {
    reviewSlot.replaceChildren(reviewBox(rev, async () => {
      showReview(await api(`/reviews/${rev.review_id}/retry`, {}));
    }) || "");
    if (rev && rev.status === "done") refreshExtras();
  };
```

4. Change `"Submit for review")), reviewSlot);` to `"Submit for review")), reviewSlot, extras);` and change `h("div", { class: "bar" }, reviewBtn), reviewSlot);` to `h("div", { class: "bar" }, reviewBtn), reviewSlot, extras);`.
5. In the Submit handler change `if (r.passed) { lastPassed = r.attempt_id; reviewBtn.disabled = false; }` to `if (r.passed) { lastPassed = r.attempt_id; reviewBtn.disabled = false; refreshExtras(); }`.

- [ ] **Step 3: Verify by hand**

Start the server (`uv run python -m gym.app`). Using the sample content, check: the count-words page shows a "Hint" section from the start and "How to say it out loud" only after a passing submit. Then add a throwaway quiz exercise folder under `content/01-hand-python/exercises/zz-quiz/` (`exercise.yaml`: `title: Quiz`, `kind: quiz`, `pass_ratio: 1.0`; `prompt.md`; `quiz.yaml` with two questions), reload, and check: radio buttons render, an unanswered submit shows "Answer every question.", a wrong submit shows ✗ with the right answer and the explanation, a right submit shows Passed. Delete `zz-quiz` afterwards. Stop the server.

- [ ] **Step 4: Commit**

```bash
graphify update .
git add -A && git commit -m "feat: quiz view and hint and say-it panels"
```

---

# Part 2: Shared dataset and migration

### Task 6: Deterministic shared dataset

**Files:**
- Create: `tools/make_delivery_data.py`, `tests/test_delivery_data.py`
- Create (generated, committed): `content/_shared/delivery.sql`, `orders.csv`, `restaurants.csv`, `customers.csv`, `couriers.csv`

**Interfaces:**
- Produces: `make_delivery_data.generate(out_dir: Path) -> None` writing the five files. Tables (SQLite): `restaurants(restaurant_id, name, city, cuisine)` 24 rows; `customers(customer_id, name, city, signup_date)` 400 rows; `couriers(courier_id, name, vehicle)` 80 rows; `orders(order_id, customer_id, restaurant_id, courier_id, created_at, subtotal, delivery_fee, coupon_code, status, promised_minutes, actual_minutes)` 1500 rows from 2026-08-01 for 92 days. About 8% of orders are `cancelled` (then `courier_id` and `actual_minutes` are NULL); about 1% of `subtotal` values are NULL; restaurants with `restaurant_id % 5 == 0` are about 25% slower than promised. `delivery.sql` holds `CREATE TABLE` statements followed by one single-line `INSERT INTO ... VALUES (...);` per row. CSVs have a header row and empty cells for NULL. Same output every run.

- [ ] **Step 1: Write the failing test**

`tests/test_delivery_data.py`:

```python
import csv
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from make_delivery_data import generate  # noqa: E402


def test_dataset_shape_and_determinism(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    generate(a)
    generate(b)
    for name in ("delivery.sql", "orders.csv", "restaurants.csv", "customers.csv", "couriers.csv"):
        assert (a / name).read_bytes() == (b / name).read_bytes()
    db = sqlite3.connect(":memory:")
    db.executescript((a / "delivery.sql").read_text())
    count = lambda q: db.execute(q).fetchone()[0]
    assert count("SELECT COUNT(*) FROM restaurants") == 24
    assert count("SELECT COUNT(*) FROM customers") == 400
    assert count("SELECT COUNT(*) FROM couriers") == 80
    assert count("SELECT COUNT(*) FROM orders") == 1500
    cancelled = count("SELECT COUNT(*) FROM orders WHERE status = 'cancelled'")
    assert 60 <= cancelled <= 180
    assert count("SELECT COUNT(*) FROM orders WHERE status = 'cancelled' AND (courier_id IS NOT NULL OR actual_minutes IS NOT NULL)") == 0
    assert 1 <= count("SELECT COUNT(*) FROM orders WHERE subtotal IS NULL") <= 40
    assert count("SELECT MIN(created_at) >= '2026-08-01' FROM orders") == 1
    slow = db.execute("SELECT AVG(actual_minutes / promised_minutes) FROM orders o WHERE status = 'delivered' AND restaurant_id % 5 = 0").fetchone()[0]
    fast = db.execute("SELECT AVG(actual_minutes / promised_minutes) FROM orders o WHERE status = 'delivered' AND restaurant_id % 5 != 0").fetchone()[0]
    assert slow > fast * 1.1
    rows = list(csv.DictReader((a / "orders.csv").open()))
    assert len(rows) == 1500 and rows[0].keys() >= {"order_id", "subtotal", "status"}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_delivery_data.py -v`
Expected: FAIL (`ModuleNotFoundError: No module named 'make_delivery_data'`)

- [ ] **Step 3: Write the implementation**

`tools/make_delivery_data.py`:

```python
"""Generate the shared food-delivery dataset used by SQL and pandas exercises.

Run: uv run python tools/make_delivery_data.py   (writes content/_shared/)
"""
import csv
import math
import random
from datetime import datetime, timedelta
from pathlib import Path

CITIES = ["Sao Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba"]
CITY_WEIGHTS = [0.4, 0.25, 0.2, 0.15]
CUISINES = ["japanese", "pizza", "brazilian", "burger", "healthy", "arabic"]
VEHICLES = ["bike", "motorbike", "car"]
COUPONS = [None, "BEMVINDO10", "FRETEGRATIS", "PIZZA20"]
COUPON_WEIGHTS = [0.7, 0.1, 0.15, 0.05]

SCHEMA = """CREATE TABLE restaurants (restaurant_id INTEGER PRIMARY KEY, name TEXT, city TEXT, cuisine TEXT);
CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT, signup_date TEXT);
CREATE TABLE couriers (courier_id INTEGER PRIMARY KEY, name TEXT, vehicle TEXT);
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, restaurant_id INTEGER, courier_id INTEGER, created_at TEXT, subtotal REAL, delivery_fee REAL, coupon_code TEXT, status TEXT, promised_minutes INTEGER, actual_minutes REAL);
"""

TABLE_COLUMNS = {
    "restaurants": ["restaurant_id", "name", "city", "cuisine"],
    "customers": ["customer_id", "name", "city", "signup_date"],
    "couriers": ["courier_id", "name", "vehicle"],
    "orders": ["order_id", "customer_id", "restaurant_id", "courier_id", "created_at", "subtotal",
               "delivery_fee", "coupon_code", "status", "promised_minutes", "actual_minutes"],
}


def build_rows():
    rnd = random.Random(2026)
    pick = lambda items, weights=None: rnd.choices(items, weights)[0]
    restaurants = [(i, f"Rest {i:02d}", pick(CITIES, CITY_WEIGHTS), CUISINES[(i * 7) % 6]) for i in range(1, 25)]
    start = datetime(2026, 8, 1)
    customers = [(i, f"Customer {i:03d}", pick(CITIES, CITY_WEIGHTS),
                  (start - timedelta(days=rnd.randrange(1, 400))).strftime("%Y-%m-%d")) for i in range(1, 401)]
    couriers = [(i, f"Courier {i:02d}", pick(VEHICLES)) for i in range(1, 81)]
    orders = []
    for i in range(1500):
        created = start + timedelta(minutes=rnd.randrange(92 * 24 * 60))
        rid = 1 + int(rnd.random() * rnd.random() * 24 + rnd.random() * 6) % 24
        delivered = rnd.random() >= 0.08
        promised = pick([30, 40, 50])
        slow = 1.25 if rid % 5 == 0 else 1.0
        noise = math.exp((rnd.random() + rnd.random() + rnd.random() - 1.5) * 0.35)
        actual = round(promised * slow * noise, 1) if delivered else None
        subtotal = round(20 + rnd.random() * 60 + rnd.random() * rnd.random() * 120, 2)
        if rnd.random() < 0.01:
            subtotal = None
        customer = 1 + int(rnd.random() * rnd.random() * 400)
        courier = 1 + rnd.randrange(80) if delivered else None
        orders.append((100001 + i, customer, rid, courier, created.strftime("%Y-%m-%d %H:%M:%S"), subtotal,
                       pick([0, 4.99, 6.99, 8.99]), pick(COUPONS, COUPON_WEIGHTS),
                       "delivered" if delivered else "cancelled", promised, actual))
    return {"restaurants": restaurants, "customers": customers, "couriers": couriers, "orders": orders}


def sql_value(v):
    if v is None:
        return "NULL"
    if isinstance(v, str):
        return "'" + v.replace("'", "''") + "'"
    return repr(v)


def generate(out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    tables = build_rows()
    lines = [SCHEMA.rstrip()]
    for name, rows in tables.items():
        cols = ", ".join(TABLE_COLUMNS[name])
        lines += [f"INSERT INTO {name} ({cols}) VALUES ({', '.join(sql_value(v) for v in row)});" for row in rows]
        with (out_dir / f"{name}.csv").open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(TABLE_COLUMNS[name])
            writer.writerows([["" if v is None else v for v in row] for row in rows])
    (out_dir / "delivery.sql").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    generate(Path(__file__).resolve().parent.parent / "content" / "_shared")
```

- [ ] **Step 4: Run the test, generate the files, commit**

Run: `uv run pytest tests/test_delivery_data.py -v`
Expected: 1 passed. If a range assertion fails by a little, read the actual value and widen the range only if it is still a sensible dataset; do not change the generator's seed to chase a number.

Run: `uv run python tools/make_delivery_data.py && ls content/_shared`
Expected: five files.

```bash
graphify update .
git add -A && git commit -m "feat: deterministic shared food-delivery dataset"
```

---

### Task 7: Journey skeleton and migration of the old gym

**Files:**
- Create: `tools/extract_old_gym.js`, `tools/old_gym.json` (generated), `tools/migrate_old_gym.py`, `tests/test_migrate.py`
- Create (generated): the 12 `content/<step>/step.yaml`, 51 exercise folders, 11 lessons per step mapping below, cards.

**Interfaces:**
- Produces: `migrate_old_gym.STEPS` (list of `(folder, title, order, min_score, timed_required)` for the 12 steps), `migrate(old: dict, out: Path, only_missing: bool = True) -> list[str]` returning the ids of drills left for hand conversion (the four `pd-*` drills), and `main()` that loads `tools/old_gym.json` and migrates into `content/`.
- Mapping (drill id to step folder): `01-hand-python`: py-second, py-avg, py-newret, py-city, py-latest, py-topk, py-session, py-merge, py-window, py-assign. `02-live-routine`: cb-fact, cb-longest, cb-rle, cb-brackets, cb-sumkeys, cb-pairsum, cb-movavg, cb-wordfreq. `03-hand-sql`: sql-cancel, sql-slow, sql-top2, sql-second, sql-mom, sql-coupon, sql-loyal, sql-second-order, sql-late, sql-churn. `04-robust-code`: prod-validate, prod-batch, prod-split, prod-breaker, prod-events, ai-retry. `06-real-data`: st-meanstd, st-auc, st-z, st-ks, st-boot, dbg-avg, dbg-late, dbg-tags. `08-production-ml`: prod-monitor, prod-debug, ai-psi, ai-eval, ai-prf. `10-ai-assistant`: ai-topk, ai-chunk, ai-json, ai-trim. The four `pd-*` drills are converted by hand in Task 17.
- Lessons: `routine`, `coderbyte`, `patterns` to `02-live-routine`; `python` to `01-hand-python`; `sql` to `03-hand-sql`; `robust` to `04-robust-code`; `pandas`, `traps`, `stats` to `06-real-data`; `ai` to `10-ai-assistant`; `senior`, `phrases` to `11-explaining`. Written as `lessons/NN-<id>.md` (NN is the old order, two digits). Lesson HTML is embedded as is (the page's markdown renderer passes HTML through). Cards: prefix `Python` to step 1, `SQL` to step 3, `pandas` and `Stats` to step 6; card id is the slugified front text.
- Time limit per exercise: `round(mins * 60 * factor)` seconds with factor 2 for steps 1 and 3, 1.5 for everything else.
- `mock: true` for every drill listed in any old mock.
- Converters: `checks` drills become a pytest file that, like the old gym, executes the submitted code followed by the drill's `pre` code in one namespace (name `__main__`) and compares each `eval(expr)` to `eval(want)` with the old tolerant comparison; `io` drills become a parametrized pytest that runs `solution.py` as a script with the input on stdin and compares stripped stdout; SQL drills use `seed_file: ../../../_shared/delivery.sql`, `solution.sql` from `ref`, `ordered` flag preserved, and the old text schema in the prompt. `hint.md`, `say.md`, `model_prompt.md` come from `hint`, `say`, `prompt`.

- [ ] **Step 1: Export the old content**

`tools/extract_old_gym.js`:

```javascript
// One-off: export the content constants of the old single-file gym to JSON.
// Run: node tools/extract_old_gym.js live-coding-gym.html tools/old_gym.json
const fs = require("fs");
const html = fs.readFileSync(process.argv[2], "utf8");
const at = (n) => html.indexOf("const " + n + " ");
const code = html.slice(at("SCHEMA"), at("VIEWS")).replace(/const runnable[\s\S]*?\n\}\n/, "const runnable = () => true;\n");
const out = new Function(code + "\nreturn {SCHEMA, DRILLS, TRACKS, LESSONS, CARDS, MOCKS, RUBRIC, STEPS};")();
fs.writeFileSync(process.argv[3], JSON.stringify(out, null, 1));
console.log(Object.keys(out).map((k) => `${k}: ${Array.isArray(out[k]) ? out[k].length : typeof out[k]}`).join("\n"));
```

Run: `node tools/extract_old_gym.js live-coding-gym.html tools/old_gym.json`
Expected: `DRILLS: 55`, `LESSONS: 12`, `CARDS: 40`, `MOCKS: 8`.

- [ ] **Step 2: Write the failing test**

`tests/test_migrate.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from migrate_old_gym import STEPS, migrate  # noqa: E402

from gym.check_content import check  # noqa: E402
from gym.content import load_content  # noqa: E402

OLD = {
    "SCHEMA": "restaurants(restaurant_id, city)",
    "TRACKS": {},
    "DRILLS": [
        {"id": "py-city", "track": "py", "title": "GMV by city", "mins": 6, "pt": "Return totals.", "en": "Group-by.",
         "starter": "def total(xs):\n    pass\n", "pre": "DATA = [1, 2, 3]\n",
         "checks": [["total(DATA)", "6"], ["total([])", "0"]], "hint": "Use sum.",
         "solution": "def total(xs):\n    return sum(xs)\n", "say": "It is a sum."},
        {"id": "cb-fact", "track": "cb", "title": "Factorial", "mins": 4, "pt": "Factorial.", "en": "Warm-up.",
         "starter": "n = int(input())\nprint(n)\n", "io": [["3", "6"], ["1", "1"]], "hint": "Loop.",
         "solution": "n = int(input())\nr = 1\nfor i in range(2, n + 1):\n    r *= i\nprint(r)\n", "say": "Loop."},
        {"id": "sql-cancel", "track": "sql", "title": "Cities", "mins": 6, "ordered": True, "pt": "List cities.",
         "en": "Select.", "starter": "SELECT\n", "ref": "SELECT city FROM restaurants ORDER BY city;",
         "hint": "ORDER BY.", "say": "Sorted."},
        {"id": "pd-gmv", "track": "pd", "title": "Manual", "mins": 6, "pt": "x", "en": "y", "keys": [], "solution": "", "say": ""},
    ],
    "LESSONS": [{"id": "python", "title": "2 · Python core", "html": "<p>Hello</p>"}],
    "CARDS": [["Python · count", "d.get(k, 0) + 1"]],
    "MOCKS": [{"id": "m", "title": "M", "mins": 10, "blurb": "", "drills": ["py-city"]}],
}


def test_migrate_writes_a_checkable_journey(tmp_path):
    shared = tmp_path / "_shared"
    shared.mkdir()
    (shared / "delivery.sql").write_text(
        "CREATE TABLE restaurants (restaurant_id INTEGER, city TEXT);\n"
        "INSERT INTO restaurants VALUES (1, 'B');\nINSERT INTO restaurants VALUES (2, 'A');\n")
    manual = migrate(OLD, tmp_path)
    assert manual == ["pd-gmv"]
    assert len(list(tmp_path.glob("*/step.yaml"))) == len(STEPS) == 12
    steps, errors = load_content(tmp_path)
    assert errors == []
    by_id = {ex.id: ex for s in steps for ex in s.exercises}
    assert by_id["py-city"].time_limit_s == 720 and by_id["py-city"].mock is True      # 6 min * 60 * 2
    assert by_id["cb-fact"].time_limit_s == 360 and by_id["cb-fact"].mock is False     # 4 * 60 * 1.5
    assert by_id["sql-cancel"].ordered is True and "ORDER BY" in by_id["sql-cancel"].solution
    assert by_id["py-city"].say == "It is a sum." and by_id["py-city"].hint == "Use sum."
    py_step = next(s for s in steps if s.id == "01-hand-python")
    assert py_step.lessons[0]["title"] == "Python core" and "<p>Hello</p>" in py_step.lessons[0]["body"]
    assert py_step.cards[0]["id"] == "python-count"
    assert check(tmp_path) == []


def test_migrate_does_not_overwrite_existing_work(tmp_path):
    (tmp_path / "_shared").mkdir()
    (tmp_path / "_shared" / "delivery.sql").write_text("CREATE TABLE restaurants (restaurant_id INTEGER, city TEXT);\n")
    migrate(OLD, tmp_path)
    solution = tmp_path / "01-hand-python" / "exercises" / "py-city" / "solution.py"
    solution.write_text("def total(xs):\n    return 6 if xs else 0\n")
    migrate(OLD, tmp_path)
    assert "return 6" in solution.read_text()
```

- [ ] **Step 3: Run test to verify it fails**

Run: `uv run pytest tests/test_migrate.py -v`
Expected: FAIL (`ModuleNotFoundError: No module named 'migrate_old_gym'`)

- [ ] **Step 4: Write the migration script**

`tools/migrate_old_gym.py`:

```python
"""One-off: convert tools/old_gym.json (export of the old single-file gym) into content/ folders.

Run: uv run python tools/migrate_old_gym.py
Existing files are never overwritten, so it is safe to re-run after hand edits.
"""
import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

STEPS = [
    ("01-hand-python", "Hand-coding Python from zero", 1, 4, True),
    ("02-live-routine", "The live-coding routine", 2, 4, True),
    ("03-hand-sql", "Hand-coding SQL", 3, 4, True),
    ("04-robust-code", "Robust code", 4, 4, False),
    ("05-testing", "Testing your own code", 5, 4, False),
    ("06-real-data", "Real data behaviour and statistics", 6, 4, False),
    ("07-ml-tools", "AI/ML engineering tools tour", 7, 4, False),
    ("08-production-ml", "Production ML systems", 8, 4, False),
    ("09-model-failures", "Common model failures", 9, 4, False),
    ("10-ai-assistant", "Using an AI assistant while observed", 10, 4, False),
    ("11-explaining", "Explaining your code", 11, 4, False),
    ("12-mock-rounds", "Mock rounds and readiness", 12, 4, False),
]

DRILL_STEP = {}
for step, ids in {
    "01-hand-python": "py-second py-avg py-newret py-city py-latest py-topk py-session py-merge py-window py-assign",
    "02-live-routine": "cb-fact cb-longest cb-rle cb-brackets cb-sumkeys cb-pairsum cb-movavg cb-wordfreq",
    "03-hand-sql": "sql-cancel sql-slow sql-top2 sql-second sql-mom sql-coupon sql-loyal sql-second-order sql-late sql-churn",
    "04-robust-code": "prod-validate prod-batch prod-split prod-breaker prod-events ai-retry",
    "06-real-data": "st-meanstd st-auc st-z st-ks st-boot dbg-avg dbg-late dbg-tags",
    "08-production-ml": "prod-monitor prod-debug ai-psi ai-eval ai-prf",
    "10-ai-assistant": "ai-topk ai-chunk ai-json ai-trim",
}.items():
    DRILL_STEP.update({i: step for i in ids.split()})

LESSON_STEP = {"routine": "02-live-routine", "coderbyte": "02-live-routine", "patterns": "02-live-routine",
               "python": "01-hand-python", "sql": "03-hand-sql", "robust": "04-robust-code",
               "pandas": "06-real-data", "traps": "06-real-data", "stats": "06-real-data",
               "ai": "10-ai-assistant", "senior": "11-explaining", "phrases": "11-explaining"}
CARD_STEP = {"Python": "01-hand-python", "SQL": "03-hand-sql", "pandas": "06-real-data", "Stats": "06-real-data"}
FACTOR = {"01-hand-python": 2, "03-hand-sql": 2}

CLOSE = '''def _close(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= 1e-6 + 1e-9 * abs(b)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_close(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_close(a[k], b[k]) for k in a)
    return a == b
'''


def checks_tests(d):
    """Old behaviour: exec the submission, then the drill's setup code, in one namespace; eval each check."""
    out = [CLOSE, "PRE = " + repr(d.get("pre", "")), "",
           "def _ns():", "    ns = {'__name__': '__main__'}",
           "    exec(open('solution.py').read() + '\\n\\n' + PRE, ns)", "    return ns", ""]
    for i, (expr, want) in enumerate(d["checks"], 1):
        out += [f"def test_check_{i}():", "    ns = _ns()", f"    got = eval({expr!r}, ns)",
                f"    assert _close(got, eval({want!r}, ns)), repr(got)", ""]
    return "\n".join(out)


def io_tests(d):
    return ("import subprocess\nimport sys\n\nimport pytest\n\n"
            "CASES = " + repr(d["io"]) + "\n\n\n"
            "@pytest.mark.parametrize('stdin, want', CASES, ids=[f'input_{i + 1}' for i in range(len(CASES))])\n"
            "def test_io(stdin, want):\n"
            "    p = subprocess.run([sys.executable, 'solution.py'], input=stdin + '\\n',\n"
            "                       capture_output=True, text=True, timeout=5)\n"
            "    assert p.stdout.strip() == want, p.stderr or p.stdout\n")


def write(path, text, only_missing):
    if only_missing and path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def write_drill(out, step, d, is_mock, schema, only_missing):
    ex = out / step / "exercises" / d["id"]
    kind = "sql" if "ref" in d else "python"
    meta = {"title": d["title"], "kind": kind, "required": True, "mock": is_mock,
            "time_limit_s": round(d["mins"] * 60 * FACTOR.get(step, 1.5))}
    prompt = d["pt"] + ("\n\n*" + d["en"] + "*" if d.get("en") else "")
    if kind == "sql":
        meta.update(ordered=bool(d.get("ordered")), seed_file="../../../_shared/delivery.sql")
        prompt += "\n\nTables:\n\n```\n" + schema + "\n```"
        write(ex / "starter.sql", d["starter"], only_missing)
        write(ex / "solution.sql", d["ref"], only_missing)
    else:
        write(ex / "starter.py", d["starter"], only_missing)
        write(ex / "solution.py", d["solution"], only_missing)
        write(ex / "tests" / "test_hidden.py", io_tests(d) if "io" in d else checks_tests(d), only_missing)
    write(ex / "exercise.yaml", yaml.safe_dump(meta, sort_keys=False), only_missing)
    write(ex / "prompt.md", prompt + "\n", only_missing)
    for name, key in (("hint.md", "hint"), ("say.md", "say"), ("model_prompt.md", "prompt")):
        if d.get(key):
            write(ex / name, d[key] + "\n", only_missing)


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def migrate(old, out, only_missing=True):
    out = Path(out)
    for folder, title, order, min_score, timed in STEPS:
        meta = {"title": title, "order": order, "gate": {"min_score": min_score, "timed_required": timed}}
        write(out / folder / "step.yaml", yaml.safe_dump(meta, sort_keys=False), only_missing)
    mock_ids = {i for m in old["MOCKS"] for i in m["drills"]}
    manual = []
    for d in old["DRILLS"]:
        step = DRILL_STEP.get(d["id"])
        if step is None:
            manual.append(d["id"])
            continue
        write_drill(out, step, d, d["id"] in mock_ids, old["SCHEMA"], only_missing)
    for n, lesson in enumerate(old["LESSONS"], 1):
        step = LESSON_STEP[lesson["id"]]
        title = re.sub(r"^\d+b? · ", "", lesson["title"])
        write(out / step / "lessons" / f"{n:02d}-{lesson['id']}.md", f"# {title}\n\n{lesson['html']}\n", only_missing)
    cards = {}
    for front, back in old["CARDS"]:
        step = CARD_STEP[front.split(" · ")[0]]
        cards.setdefault(step, []).append({"id": slug(front), "front": front, "back": back})
    for step, items in cards.items():
        write(out / step / "cards.yaml", yaml.safe_dump(items, sort_keys=False, allow_unicode=True), only_missing)
    return manual


def main():
    old = json.loads((ROOT / "tools" / "old_gym.json").read_text())
    manual = migrate(old, ROOT / "content")
    print("left for hand conversion:", ", ".join(manual))


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Run the unit test**

Run: `uv run pytest tests/test_migrate.py -v`
Expected: 2 passed

- [ ] **Step 6: Run the real migration and check it**

```bash
uv run python tools/migrate_old_gym.py
uv run python -m gym.check_content
```

Expected: `left for hand conversion: pd-gmv, pd-agg, pd-gap, pd-coupon`, then `content ok`. (While writing this plan, the converters were already run against all 47 Python drills: every old solution passes its generated tests and every starter fails them, and all 10 old SQL reference queries run on the generated dataset. Any problem listed now is therefore new, so investigate it.) If the checker does list problems, the usual causes are:
- `<id>: reference solution fails its own tests`: the old solution or checks relied on browser Python behaviour. Run that exercise's tests by hand (`cd /tmp/x && cp solution.py tests ...`, or read the failing assertion through `uv run python -c "from gym.runner import run_python_tests; ..."`) and fix the **solution or test file**, never the checker.
- `<id>: starter already passes the tests`: the old starter returned something that happens to satisfy the checks. Change the starter so it does not.
- `prod-split` and anything using `hash()`: CPython randomises string hashes per process, so a solution using `hash()` is not deterministic. Fix the solution to use `hashlib` (e.g. `int(hashlib.md5(key.encode()).hexdigest(), 16)`) and mention in its `say.md` why.
- `missing hint.md` for a drill that had no hint in the old gym: write a one-sentence hint.

Re-run until `content ok`.

- [ ] **Step 7: Verify in the browser, then commit**

Start the server. Check: the journey lists 12 steps; step 1 shows its lesson and 10 exercises; open `cb-fact` (reads stdin, passes with the reference solution), `sql-top2` (schema panel shows four CREATE TABLE lines only), `prod-validate` (passes with the reference solution). Stop the server.

```bash
graphify update .
git add -A && git commit -m "feat: migrate the old gym into the journey (51 drills, 11 lessons, 40 cards)"
```

---

# Part 3: Authoring

## Authoring protocol (applies to Tasks 8 to 19)

Each authoring task is executed as: split the step's deliverables into batches of at most 8 exercises (lessons and cards are their own batch), dispatch one subagent per batch with (a) this protocol and kit, (b) the batch's rows from the task, (c) `CLAUDE.md`, then run the gate commands, fix, commit. Use a mid-size model for authoring subagents to keep token use down. Subagents write files only; the controller runs the gate.

**Quality rules for every exercise**

1. One idea per exercise. Time limit in `exercise.yaml` is for a competent beginner (steps 1 to 3 use roughly twice interview pace).
2. Python: at least 3 hidden tests, including an empty or edge input and (for robust-code steps) a failure path. At least one `wrong/*.py` that plausibly mimics a real learner mistake and must fail. A `gaps.py` for about a third of the step-1 and step-3 exercises.
3. `hint.md`: one or two sentences, a nudge, not the answer. `say.md`: how to explain the solution aloud in 3 to 5 sentences including complexity and one trade-off or edge case.
4. Starter files give the signature and a `pass` body, never the algorithm.
5. Time and randomness are injected (`clock`, `sleep`, seeds), never read from the system.
6. Lessons: plain markdown, 500 to 900 words: the problem it solves, the smallest example that runs, the three traps people hit, and a "say it like this" paragraph. Code fences only for code that works on Python 3.12.
7. Cards: 20 to 40 per step, one fact or snippet each, `front` is a task, `back` is the answer snippet.
8. Exercises that the interviewer would judge on communication (`explain`, `prompt`, `open`) carry a `rubric:` of 3 to 5 criteria written as statements, plus `say.md` as the model answer.

**Gate for every authoring commit** (all must pass):

```bash
uv run python -m gym.check_content   # prints: content ok
uv run pytest -q
graphify update .
```

Then `git add -A && git commit -m "content: <step> <what>"`.

**Kit: one worked example per exercise type.** Copy these shapes exactly.

*Python exercise* `content/01-hand-python/exercises/py1-reverse-words/`:

`exercise.yaml`
```yaml
title: Reverse the words
kind: python
time_limit_s: 480
required: true
```
`prompt.md`
```markdown
Write `reverse_words(s: str) -> str` that returns the words of `s` in reverse order, separated by single spaces. Extra spaces in the input are ignored. `"the  sky is blue"` becomes `"blue is sky the"`. An empty string returns an empty string.
```
`starter.py`
```python
def reverse_words(s: str) -> str:
    pass
```
`solution.py`
```python
def reverse_words(s: str) -> str:
    return " ".join(reversed(s.split()))
```
`gaps.py`
```python
def reverse_words(s: str) -> str:
    return " ".join(____(s.____()))
```
`tests/test_hidden.py`
```python
from solution import reverse_words


def test_basic():
    assert reverse_words("the sky is blue") == "blue is sky the"


def test_extra_spaces():
    assert reverse_words("  a   b ") == "b a"


def test_empty():
    assert reverse_words("") == ""
```
`wrong/reverses_letters.py`
```python
def reverse_words(s: str) -> str:
    return s[::-1]
```
`hint.md`: `str.split() with no argument splits on any run of whitespace.`
`say.md`: `I split on whitespace, which also drops the extra spaces, reverse the list and join it with one space. It is O(n) time and space. An empty string gives an empty list, so it returns "" without a special case.`

*SQL exercise* `content/03-hand-sql/exercises/sq-late-by-city/`:

`exercise.yaml`
```yaml
title: Late deliveries by city
kind: sql
time_limit_s: 600
required: true
ordered: true
seed_file: ../../../_shared/delivery.sql
```
`prompt.md`: `A delivered order is late when actual_minutes is above promised_minutes. For each restaurant city return city and late_orders (the count of late delivered orders), most late first, ties by city name.` `starter.sql`: `SELECT`. `solution.sql`:
```sql
SELECT r.city, COUNT(*) AS late_orders
FROM orders o JOIN restaurants r ON r.restaurant_id = o.restaurant_id
WHERE o.status = 'delivered' AND o.actual_minutes > o.promised_minutes
GROUP BY r.city
ORDER BY late_orders DESC, r.city;
```
plus `hint.md` and `say.md` as above. The result is compared with the reference by value, so column names do not matter but row order does when `ordered: true`.

*Test-writing exercise* `content/05-testing/exercises/tw-slugify/` (kind `tests`): `exercise.yaml` (`title: Test slugify`, `kind: tests`, `time_limit_s: 600`), `prompt.md` (spec: lowercases, splits on whitespace, joins with `-`), `starter.py` (`from solution import slugify\n\n\ndef test_basic():\n    pass\n`), `solution.py` (the reference test file: one test for lowercasing `slugify("Hello World") == "hello-world"`, one for repeated spaces `slugify("a  b") == "a-b"`, one for empty `slugify("") == ""`), `impl_good.py` (`def slugify(s):\n    return "-".join(s.lower().split())\n`), `impl_bad_1.py` (forgets `.lower()`), `impl_bad_2.py` (`s.lower().replace(" ", "-")`, breaks on repeated spaces), `impl_bad_3.py` (returns `s` unchanged for the empty string case by `return "-" if not s else ...`), `hint.md`, `say.md`. Every bad implementation must differ from the good one in exactly one way and the reference tests must catch each.

*Quiz* `content/07-ml-tools/exercises/tq-tracking/`: `exercise.yaml` (`title: Quiz: experiment tracking and orchestration`, `kind: quiz`, `pass_ratio: 0.8`), `prompt.md` (one-line intro), `quiz.yaml`:
```yaml
- q: What does an experiment tracker such as MLflow record for each run?
  options:
    - Only the final model file
    - Parameters, metrics and artifacts, so runs can be compared and reproduced
    - The GPU temperature
  answer: 1
  why: Tracking exists so that you can say which parameters and data produced which metric.
```
10 to 12 questions per quiz; every wrong option must be plausible; `why` is one sentence.

*Open question* (`kind: open`) `content/07-ml-tools/exercises/to-mlflow-why/`: `exercise.yaml` (`title: Explain: why track experiments?`, `kind: open`, `rubric:` list of 3 to 4 statements), `prompt.md` ("An interviewer asks: why would you use an experiment tracker instead of a spreadsheet? Answer in four to six sentences, as you would say it."), `say.md` (the model answer).

*Prompt exercise* (`kind: prompt`) `content/10-ai-assistant/exercises/pa-validate-feature-row/`: `prompt.md` describes the coding task the learner must get an AI assistant to solve; the learner types the prompt they would send; `rubric:` uses the four default prompt criteria plus task-specific ones; `model_prompt.md` is a strong example prompt; `say.md` explains what makes it strong.

*Explain exercise* (`kind: explain`) `content/11-explaining/exercises/ex-retry-backoff/`: `prompt.md` shows a complete code listing in a fenced block and asks "Explain this code as you would to the interviewer after finishing it: what it does, complexity, one risk."; `say.md` is the model explanation; `rubric:` optional (defaults apply).

*Pandas exercise with data files* (`kind: python`): `exercise.yaml` adds `files:` (`- ../../../_shared/orders.csv`, `- ../../../_shared/restaurants.csv`); the hidden test reads `pd.read_csv("orders.csv")` and compares the submission's result with a reference computed inside the test:
```python
import pandas as pd
from solution import gmv_by_city


def test_matches_reference():
    orders = pd.read_csv("orders.csv")
    restaurants = pd.read_csv("restaurants.csv")
    got = gmv_by_city(orders, restaurants)
    d = orders[orders["status"] == "delivered"].copy()
    d["gmv"] = d["subtotal"].fillna(0) + d["delivery_fee"]
    want = d.merge(restaurants, on="restaurant_id").groupby("city")["gmv"].sum().sort_values(ascending=False)
    assert list(got.index) == list(want.index)
    assert got.round(2).tolist() == want.round(2).tolist()
```

---

### Task 8: Step 1, Hand-coding Python from zero (Phase 2)

**Goal of the step:** the learner can type common Python from memory in a blank editor. Migrated: 10 `py-*` drills, lesson "Python core", Python cards. **New:** the items below. Time factor 2. Exercise ids use `py1-`.

Lessons (new, `lessons/NN-<slug>.md`, numbered after the migrated one): `types-and-strings` (str methods, slicing, f-strings, split and join), `lists-and-loops` (indexing, slicing, enumerate, zip, comprehensions), `dicts-and-sets` (get, setdefault, Counter and defaultdict, set operations), `functions` (defaults, the mutable default trap, `*args`, lambda, sorted with key), `classes-and-dataclasses`, `errors-files-json-dates` (try and except, `with open`, json, csv, datetime).

Exercises (python kind, 30):

| Group | ids and one-line spec |
|---|---|
| Strings (6) | `py1-reverse-words` (kit example), `py1-is-palindrome` (ignore case and non-letters), `py1-count-vowels`, `py1-title-case` (without `.title()`), `py1-caesar` (shift letters, keep others), `py1-compress-spaces` |
| Lists (6) | `py1-flatten` (one level), `py1-unique-keep-order`, `py1-rotate` (k steps, k larger than length), `py1-chunks` (size n, last chunk short), `py1-running-sum`, `py1-zip-pairs` (adjacent pairs) |
| Dicts and sets (6) | `py1-invert-dict` (values may repeat: list of keys), `py1-group-by-length`, `py1-word-count-top` (top n, ties alphabetical), `py1-common-keys`, `py1-merge-dicts-sum`, `py1-set-diff-report` (added, removed, kept) |
| Functions (4) | `py1-compose`, `py1-memo-fib` (cache with a dict), `py1-sort-multi-key` (by score desc then name), `py1-apply-n-times` |
| Classes (4) | `py1-counter-class`, `py1-stack-class` (raises on empty pop), `py1-dataclass-order` (dataclass with order, sort a list), `py1-bank-account` (overdraft raises `ValueError`) |
| Errors, files, json, dates (4) | `py1-safe-int` (default on failure), `py1-parse-csv-line` (quotes with `csv` module), `py1-json-roundtrip`, `py1-days-between` (ISO date strings) |

Also: 30 flashcards (`cards.yaml` ids prefixed `py1-`, appended to the migrated file), of which every exercise's core pattern is one card. Mark `mock: true` on 8 of the new exercises (a spread across groups) so mock rounds have Python variety.

- [ ] **Step 1:** dispatch authoring subagents in batches (lessons; strings and lists; dicts, functions, classes; errors; cards), each following the protocol and kit.
- [ ] **Step 2:** run the gate commands; fix every reported problem.
- [ ] **Step 3:** play three of the new exercises in the browser, one in each of retype, gaps and timed modes, to check the experience. Fix content that reads badly.
- [ ] **Step 4:** commit `content: step 1 hand-coding python`.

---

### Task 9: Step 2, The live-coding routine (Phase 2)

**Goal:** run the six-step routine (clarify, example, plan, code, test, improve) on classic problems under a clock, and talk while doing it. Migrated: 8 `cb-*` drills, lessons "The routine", "The Coderbyte format", "Algorithm patterns". **New**, ids prefixed `rt-`:

Lessons: `clarifying-questions` (the five questions to ask per problem type, with example answers), `testing-in-30-seconds` (tiny example plus one edge case, say it aloud), `when-you-are-stuck` (what to say and do).

Exercises (python, 12): `rt-two-sum` (indices, one pass with a dict), `rt-anagram-groups`, `rt-roman-to-int`, `rt-binary-search` (return index or -1, with duplicates return the first), `rt-merge-intervals`, `rt-lru-cache` (class with get and put, capacity), `rt-longest-unique-substring`, `rt-top-k-frequent`, `rt-parse-log-lines` (split "ts level message" lines, count by level), `rt-first-unique-char`, `rt-valid-ip` (IPv4 rules), `rt-rotate-matrix` (90 degrees clockwise). Mark all 12 `mock: true`. 20 flashcards prefixed `rt-` (the patterns: two pointers, sliding window, hash map count, stack, binary search, intervals).

- [ ] **Step 1:** dispatch authoring subagents (lessons and cards; exercises in two batches of 6).
- [ ] **Step 2:** run the gate commands; fix problems.
- [ ] **Step 3:** commit `content: step 2 live-coding routine`.

---

### Task 10: Step 3, Hand-coding SQL (Phase 2)

**Goal:** write SELECT statements from memory, through windows. Migrated: 10 `sql-*` drills, lesson "SQL", SQL cards. **New**, ids prefixed `sq-`, all on the shared dataset (`seed_file`), prompt always lists the tables used and states ties and ordering. Time factor 2.

Lessons: `joins-explained`, `group-by-and-having`, `subqueries-and-ctes`, `window-functions` (row_number, rank, dense_rank, lag, lead, running totals, frames, ntile, first_value), `nulls-dates-and-dedupe` (COALESCE, COUNT(col) vs COUNT(*), `strftime`, `julianday`, de-duplication with row_number), `dialect-notes` (what changes in Postgres, BigQuery, MySQL: date functions, `LIMIT`, `QUALIFY`, `FILTER`).

Exercises (sql, 36):

| Group | ids |
|---|---|
| Select and filter (5) | `sq-select-basic`, `sq-filter-and-or`, `sq-in-between-like`, `sq-order-limit`, `sq-distinct-count` |
| Joins (6) | `sq-inner-join`, `sq-left-join-missing` (customers with no orders), `sq-three-table-join`, `sq-self-join-pairs` (customers who ordered from the same restaurant twice), `sq-join-aggregate`, `sq-anti-join-not-exists` |
| Group and having (6) | `sq-count-by-status`, `sq-avg-by-cuisine`, `sq-having-threshold`, `sq-multi-group`, `sq-conditional-agg`, `sq-late-by-city` (kit example) |
| Subqueries and CTEs (5) | `sq-scalar-subquery`, `sq-in-subquery`, `sq-correlated`, `sq-cte-two-steps`, `sq-cte-chain` |
| Windows (8) | `sq-row-number-latest`, `sq-rank-vs-dense-rank`, `sq-running-total`, `sq-moving-average-7d`, `sq-lag-growth`, `sq-lead-next-order`, `sq-ntile-spend-bands`, `sq-first-value-per-customer` |
| Nulls, dates, dedupe (6) | `sq-coalesce-subtotal`, `sq-count-null-trap`, `sq-orders-per-week`, `sq-days-since-signup`, `sq-dedupe-keep-latest`, `sq-case-buckets` |

Mark 10 of them `mock: true`. 30 SQL flashcards prefixed `sq-`.

- [ ] **Step 1:** dispatch authoring subagents (lessons and cards; one batch per group, joining the two smallest).
- [ ] **Step 2:** run the gate commands. Each reference query must also run in under 1 second on the dataset.
- [ ] **Step 3:** commit `content: step 3 hand-coding sql`.

---

### Task 11: Step 4, Robust code (Phase 3)

**Goal:** write code that survives bad input, failure and re-runs, deterministically. Migrated: 6 drills (validate, batch, split, breaker, events, retry), lesson "Robust ML systems". **New**, ids `rb-`:

Lessons: `determinism` (seeds, stable sorts, dict and set ordering, `hash()` per-process randomisation, time and timezones), `failure-modes-checklist` (the ten questions to ask before coding), `injecting-clocks-and-sleep` (why and how, with a runnable example), `idempotency-and-retries`.

Exercises (python, 13): `rb-parse-config` (typed config with defaults and clear errors), `rb-deadline-timeout` (loop with a deadline and an injected clock), `rb-idempotency-key` (process each key once, return the stored result on repeat), `rb-stable-sort-ties`, `rb-seeded-sampling` (`random.Random(seed)`, same sample every call), `rb-structured-logging` (return log records as dicts), `rb-rate-limiter` (token bucket, injected clock), `rb-atomic-write` (write temp file then `os.replace`, in a temp dir the test provides), `rb-chunked-stream` (process an iterator in chunks, isolate failing records), `rb-safe-metrics` (division by zero, NaN and None in a metric), `rb-dataclass-contract` (validate with a dataclass `__post_init__`), `rb-retry-classify` (retry only transient errors), `rb-late-events` (out-of-order and duplicate events). Mark 6 `mock: true`. One quiz `rb-quiz` (12 questions on determinism, idempotency, retries). 25 cards prefixed `rb-`. Add a `rubric:` and `review: true` to `rb-parse-config` and `rb-chunked-stream` (the two flagship exercises that get an AI code review).

- [ ] **Steps 1 to 3:** author in batches, run the gate commands, commit `content: step 4 robust code`.

---

### Task 12: Step 8, Production ML systems (Phase 3)

Migrated: `prod-monitor`, `prod-debug`, `ai-psi`, `ai-eval`, `ai-prf`. **New**, ids `pm-`:

Lessons: `serving-patterns` (batch, online, streaming, when each), `monitoring-basics` (what to log, latency percentiles, data and prediction drift, alert thresholds), `deployment-strategies` (shadow, canary, blue-green, rollback), `data-contracts` (schema, ranges, versioning, what to do on violation).

Exercises (python, 14): `pm-input-contract`, `pm-model-registry-lookup` (latest version in a stage from a list of dicts), `pm-canary-split` (stable hash bucket with `hashlib`, 5 percent), `pm-shadow-compare` (compare two models' outputs, report disagreement), `pm-ttl-cache` (injected clock), `pm-health-check`, `pm-feature-skew-check` (online versus offline feature values), `pm-ab-assignment` (deterministic, sticky), `pm-backpressure-queue` (bounded queue, drop policy), `pm-timeout-fallback` (fallback value when the model call is slow or raises), `pm-latency-percentiles` (nearest-rank p50, p95, p99), `pm-drift-alert` (thresholds, hysteresis to avoid flapping), `pm-batch-checkpoint` (resume after a crash), `pm-schema-evolution` (old and new payload versions both accepted). Mark 6 `mock: true`. Quiz `pm-quiz` (12 questions). 25 cards prefixed `pm-`.

- [ ] **Steps 1 to 3:** author, gate, commit `content: step 8 production ml`.

---

### Task 13: Step 9, Common model failures (Phase 3)

**Goal:** recognise the usual ways a model in production goes wrong and write the defensive code. No migrated drills. ids `mf-`.

Lessons: `catalog-of-failures` (each failure with symptom, cause, detection, defence), `defensive-patterns` (validate, clip, fall back, alarm, fail closed or open and why), `debugging-routine` (reproduce, shrink, hypothesise, check one thing at a time; what to say aloud).

Exercises (python, 14): `mf-nan-score-guard`, `mf-out-of-range-score`, `mf-missing-feature-fallback`, `mf-stale-model-detector` (model age and data age), `mf-label-leakage-scan` (find a feature that almost equals the label), `mf-imbalance-metrics` (accuracy hides a bad model: return precision and recall), `mf-calibration-bins`, `mf-silent-drift-alarm`, `mf-heuristic-fallback-chain` (model, then rule, then constant), `mf-partial-batch-failure` (one bad row must not sink the batch), `mf-duplicate-events`, and three debugging drills (buggy code supplied, tests fail, fix with the smallest safe change): `mf-timezone-bug`, `mf-off-by-one-window`, `mf-train-serve-skew`. Mark 5 `mock: true`. Quiz `mf-quiz`. 20 cards prefixed `mf-`.

- [ ] **Steps 1 to 3:** author, gate, commit `content: step 9 model failures`.

---

### Task 14: Step 10, Using an AI assistant while observed (Phase 3)

Migrated: `ai-topk`, `ai-chunk`, `ai-json`, `ai-trim` (their old `prompt` field becomes `model_prompt.md`), lesson "Prompting while they watch". **New**:

Lessons: `prompt-anatomy` (task, inputs and outputs, constraints, examples, asks for tests), `verifying-ai-code` (read every line, run the tests, try three edge inputs, spot the usual AI mistakes), `what-the-interviewer-sees` (what they judge: your prompt, your edits, whether you understand the result; scripts to say aloud).

Exercises: 10 `prompt` kind, ids `pa-validate-feature-row`, `pa-retry-wrapper`, `pa-sql-cohort`, `pa-parse-logs`, `pa-batch-scoring`, `pa-drift-check`, `pa-dedupe-events`, `pa-rate-limiter`, `pa-split-data`, `pa-metrics-fn`: each states a task as an interviewer would, the learner writes the prompt, Gemini grades it with the four default prompt criteria; `model_prompt.md` holds a strong prompt. 6 `python` "verify" exercises, ids `va-off-by-one-chunk`, `va-mutable-default`, `va-nan-comparison`, `va-timezone-naive`, `va-swallowed-exception`, `va-leaky-scaler` (scikit-learn): the starter is plausible AI-generated code with one hidden bug, hidden tests fail on it, the learner finds and fixes it; `say.md` names the bug and how to spot it. 15 cards prefixed `pa-`.

- [ ] **Steps 1 to 3:** author, gate, commit `content: step 10 ai assistant`.

---

### Task 15: Step 11, Explaining your code (Phase 3)

Migrated: lessons "Senior talking points", "Thinking-aloud phrases". **New**:

Lessons: `explanation-structure` (what it does, how, complexity, trade-offs, risks, next step; with one full worked example), `complexity-cheatsheet`, `portuguese-phrase-bank` (optional: the same structure in Portuguese, with the key technical terms kept in English).

Exercises: 12 `explain` kind, ids `ex-validate-row`, `ex-retry-backoff`, `ex-circuit-breaker`, `ex-lru-cache`, `ex-sql-window`, `ex-pipeline-leak`, `ex-batch-chunking`, `ex-idempotent-consumer`, `ex-psi`, `ex-time-split`, `ex-token-bucket`, `ex-ab-bucketing`: each shows a complete listing (30 to 60 lines, correct but not trivial, one contains a subtle risk), the learner explains it, Gemini grades with the explain rubric; `say.md` is the model explanation. 4 `open` kind, ids `ab-tell-me-about-a-project`, `ab-hardest-bug`, `ab-ai-usage-philosophy`, `ab-weaknesses`: behavioural questions about the learner's own background; the model answer in `say.md` is written as a template with `[your example]` markers, because it depends on the learner (state this in the prompt). 10 cards prefixed `ex-`.

- [ ] **Steps 1 to 3:** author, gate, commit `content: step 11 explaining`.

---

### Task 16: Step 5, Testing your own code (Phase 4)

**Goal:** write tests that catch real bugs. Exercises use the `tests` kind (learner writes the test file; the app runs it against one correct and several buggy implementations). ids `tw-`.

Lessons: `pytest-basics`, `fixtures-and-parametrize`, `testing-failures-and-time` (`pytest.raises`, fake clock, monkeypatch), `what-to-test` (the behaviours, the edges, the failure paths; how many tests is enough).

Exercises (tests, 12): `tw-slugify` (kit example), `tw-clamp`, `tw-parse-duration` ("1h30m" to seconds), `tw-dedupe`, `tw-moving-average`, `tw-validate-email`, `tw-bank-withdraw` (exceptions), `tw-retry` (fake sleep), `tw-top-k`, `tw-batch-split`, `tw-normalize-scores` (min-max with constant input), `tw-merge-sorted`. Each has 3 to 4 `impl_bad_N`, each differing from the good one in exactly one way, and a reference `solution.py` that catches them all. One quiz `tq-testing` (10 questions). 15 cards prefixed `tw-`. Mark none `mock`.

- [ ] **Steps 1 to 3:** author, gate (the checker verifies every reference test file catches every bug), commit `content: step 5 testing`.

---

### Task 17: Step 6, Real data behaviour and statistics (Phase 4)

Migrated: 8 drills (5 `st-*`, 3 `dbg-*`), lessons "pandas", "Data traps", "Stats by hand", pandas and Stats cards. **Convert by hand** the four `pd-*` drills (`pd-gmv`, `pd-agg`, `pd-gap`, `pd-coupon`) from self-check to real Python exercises using the data-file pattern in the kit (read their text and `solution` from `tools/old_gym.json`; each becomes a function taking the dataframes and returning the described result; hidden tests compare with a reference computed in the test). **New**:

Lessons: `missing-values`, `merges-and-duplicates` (row counts before and after a merge, many-to-many surprises), `time-based-splits-and-leakage`.

Exercises: 11 pandas `python` exercises with data files, ids `pdx-fillna-strategy`, `pdx-dtype-fix`, `pdx-dedupe-latest`, `pdx-merge-count-check`, `pdx-groupby-multi`, `pdx-datetime-features`, `pdx-time-split`, `pdx-outliers-iqr`, `pdx-pivot`, `pdx-rolling`, `pdx-leakage-detect`. 6 `sql` data-quality exercises on the shared dataset, ids `dq-null-rates`, `dq-duplicates`, `dq-orphan-keys`, `dq-out-of-range`, `dq-freshness`, `dq-reconcile-counts`. Quiz `dq-quiz` (statistics and data traps, 12 questions). 15 cards prefixed `pdx-`. Mark 4 `mock: true`.

- [ ] **Steps 1 to 3:** convert the `pd-*` drills first, then author the rest; gate; commit `content: step 6 real data`.

---

### Task 18: Step 7, AI/ML engineering tools tour (Phase 4)

**Goal:** the learner can talk about the common tooling credibly. Theory and examples; no external services are called. Every lesson has the same shape: what problem the tool solves, where it sits in a pipeline, a minimal real example (code that runs where possible, otherwise config), what to say and what not to claim, and the three questions an interviewer is likely to ask.

Lessons (11): `sklearn-pipelines`, `experiment-tracking-mlflow`, `orchestration-airflow-and-friends`, `containers-docker`, `model-serving-fastapi`, `feature-stores`, `data-and-model-versioning-dvc`, `monitoring-evidently-prometheus`, `ci-cd-for-ml`, `cloud-ml-platforms` (SageMaker, Vertex AI, Databricks), `llm-stack` (embeddings, vector databases, RAG, LangChain-style frameworks, evaluation). Cards (40) prefixed `tl-`.

Exercises: 6 quizzes, ids `tq-sklearn`, `tq-tracking`, `tq-orchestration-containers`, `tq-serving-features`, `tq-monitoring-cicd`, `tq-llm-stack` (10 to 12 questions each). 8 `open` questions, ids `to-pipeline-vs-script`, `to-mlflow-why`, `to-airflow-vs-cron`, `to-docker-why`, `to-batch-vs-online`, `to-feature-store`, `to-drift-monitoring`, `to-rag-basics`. 4 coded drills with scikit-learn (all deterministic with `random_state`), ids `tc-pipeline-impute-scale`, `tc-column-transformer`, `tc-cross-val-score`, `tc-save-load-model` (joblib into a temp directory). Gate rule for the step: all quizzes passed and all open answers at 4 or better.

- [ ] **Steps 1 to 3:** author lessons in batches of 3 to 4 (verify every code example runs on Python 3.12 with the project's dependencies, or is clearly marked as config), then exercises; gate; commit `content: step 7 ml tools`.

---

### Task 19: Step 12, Mock rounds and readiness (Phase 4)

**Goal:** the final simulation. The app's mock round picks one Python and one SQL exercise flagged `mock: true`, so this task also audits the pool.

Lessons: `strategy-for-the-hour` (time split: 5 clarify, 25 code, 10 prompt and AI use, 20 explain; what to do when stuck; how to use the assistant visibly), `after-the-round` (a one-page debrief template).

- [ ] **Step 1:** write the two lessons.
- [ ] **Step 2: Audit the mock pool.** Run:

```bash
uv run python - <<'EOF'
from gym.content import load_content
steps, _ = load_content("content")
pool = [ex for s in steps for ex in s.exercises if ex.mock]
for kind in ("python", "sql"):
    print(kind, sum(ex.kind == kind for ex in pool))
EOF
```

Expected: at least 20 Python and 10 SQL. If not, flag more suitable exercises `mock: true` (prefer ones from steps 2, 4, 8, 9).

- [ ] **Step 3:** run a full mock round in the browser end to end (as in the app plan's page check). Commit `content: step 12 mock rounds`.

---

### Task 20: Final audit

- [ ] **Step 1:** `uv run python -m gym.check_content` prints `content ok`; `uv run pytest -q` passes.
- [ ] **Step 2: Coverage report.** Print, per step, the number of lessons, exercises by kind, cards and required exercises:

```bash
uv run python - <<'EOF'
from collections import Counter
from gym.content import load_content
steps, errors = load_content("content")
print("errors:", errors)
for s in steps:
    kinds = Counter(ex.kind for ex in s.exercises)
    print(f"{s.id:20} lessons={len(s.lessons):2} cards={len(s.cards):3} exercises={dict(kinds)}")
EOF
```

Every step except 12 must have at least 3 lessons and 10 exercises (step 7 counts quizzes and open questions). Fix any gap.

- [ ] **Step 3:** reset the learner's progress (`rm -f data/progress.db`), start the server, click through step 1's first exercise and one quiz, then stop the server.
- [ ] **Step 4:** `graphify update .`, commit `content: final audit`, and report the coverage numbers to the user.

---

## Self-review notes

- **Spec coverage:** every one of the 12 journey steps has a task (1 to 3 in Tasks 8 to 10, 4 in Task 11, 5 in Task 16, 6 in Task 17, 7 in Task 18, 8 to 11 in Tasks 12 to 15, 12 in Task 19). Spec section 4's four exercise modes, flashcards, gates and mocks are covered by the finished app; spec section 5's content format is extended in Part 1 (quiz, tests, hint, say, shared data) and the spec's migration of the 55 drills, lessons and mocks is Task 7 plus the `pd-*` conversion in Task 17. The old mocks' preset sets are replaced by the random Python plus SQL pick; their drill lists only decide which exercises are flagged `mock: true`.
- **Known limits:** the AI reviewer grades communication, not truth: for `open` and `explain` answers its marks are an interviewer-style opinion, not ground truth. The SQL dialect is SQLite. Step 12 has no required exercises, so its "passed" mark never lights up; the readiness number on the journey page is its gate.
