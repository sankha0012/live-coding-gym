# Live Coding Gym App Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the local training app (server, code runner, Gemini reviewer, gates, flashcards, mock rounds, web page) that the 12-step learning journey runs on.

**Architecture:** A FastAPI server on the user's Mac loads content from plain files, runs submissions in real CPython (pytest in a subprocess) or SQLite, asks Gemini for rubric-based reviews over REST, and stores progress in one SQLite file. A no-build web page (plain JavaScript, CodeMirror from a CDN) talks to the server over a JSON API.

**Tech Stack:** Python 3.12 managed by `uv`, FastAPI, uvicorn, PyYAML, pytest, standard-library `sqlite3` and `urllib`, CodeMirror 5 and marked from cdnjs.

**Spec:** `docs/superpowers/specs/2026-11-14-live-coding-gym-design.md`

**Scope of this plan:** the app only (spec build phases 1, 2, 3 and 5). It ships with three sample exercises so every feature can be used. The journey content (spec phase 4: all 12 steps, and migration of the 55 drills from `live-coding-gym.html`) is a second plan, written after this app works, because content is authored against the finished content format.

## Global Constraints

- One user, one Mac. No accounts, no hosting. Rough visual finish is acceptable.
- Python `>=3.12`, run through `uv`. The system Python is 3.9 and must not be used.
- The Gemini key is read from `.env` as `GEMINI_API_KEY`. The model name is read from `GEMINI_MODEL`. Never print, log or commit the key. `.env` is already in `.gitignore`.
- The reviewer calls Gemini with the standard library only. No Gemini SDK.
- A reviewer failure never loses a submission: tests still work, the review is stored with status `pending`.
- The editor has autocomplete off on purpose.
- Content lives in `content/` as plain files. App code never contains lesson or exercise text.
- The only code the runner executes is the user's own. No sandbox.
- Run all commands from `/Users/surface/Documents/Monica/live-coding-gym`.
- End every commit message with: `Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>`

## File Structure

| File | Responsibility |
|------|----------------|
| `pyproject.toml` | Dependencies and pytest settings. |
| `gym/config.py` | Paths and `.env` loading. |
| `gym/content.py` | Load steps, lessons, exercises and cards from `content/`. |
| `gym/runner.py` | Run Python submissions under pytest; run and compare SQL. |
| `gym/db.py` | Progress storage (attempts, reviews, cards, mocks, unlocks). |
| `gym/reviewer.py` | Build review prompts, call Gemini, parse and validate the reply. |
| `gym/gates.py` | Decide whether an exercise and a step are passed, and which steps are unlocked. |
| `gym/cards.py` | Flashcard schedule (Leitner boxes). |
| `gym/mock.py` | Pick mock tasks, score a round, compute readiness. |
| `gym/app.py` | FastAPI routes wiring the modules together. |
| `gym/check_content.py` | Run every reference solution against its own tests. |
| `web/index.html`, `web/app.js`, `web/style.css` | The page. |
| `tests/fixtures/content/` | Sample content used by tests and copied to `content/` as starter content. |
| `tests/test_*.py` | One test file per module. |

---

### Task 1: Project skeleton, config and content loader

**Files:**
- Create: `pyproject.toml`, `gym/__init__.py`, `gym/config.py`, `gym/content.py`
- Create: `tests/conftest.py`, `tests/test_content.py`
- Create: sample content under `tests/fixtures/content/` (listed in Step 1)
- Modify: `.gitignore`

**Interfaces:**
- Produces: `gym.config.ROOT`, `CONTENT_DIR`, `DB_PATH`, `WEB_DIR` (all `pathlib.Path`), `gym.config.load_env(path=ROOT / ".env") -> None`.
- Produces: `gym.content.Exercise` with fields `id, step_id, title, kind, prompt, dir, starter, solution, gaps, seed, time_limit_s, required, review, mock, ordered, rubric`; `gym.content.Step` with fields `id, title, order, min_score, timed_required, lessons, exercises, cards`; `gym.content.load_content(content_dir) -> tuple[list[Step], list[str]]` (steps sorted by `order`, plus a list of error strings for broken exercises).
- Produces: test fixtures `FIXTURES` (path) and `steps`.

- [ ] **Step 1: Create the sample content**

`tests/fixtures/content/01-hand-python/step.yaml`:

```yaml
title: Hand-coding Python from zero
order: 1
gate:
  min_score: 4
  timed_required: true
```

`tests/fixtures/content/01-hand-python/lessons/01-counting.md`:

```markdown
# Counting with a dict

The most common hand-coded pattern: walk a sequence and count.

    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1

`dict.get(key, 0)` returns 0 when the key is missing, so no `if` is needed.
```

`tests/fixtures/content/01-hand-python/cards.yaml`:

```yaml
- id: dict-count
  front: Count how often each item appears in `items`, using a plain dict.
  back: |
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
```

`tests/fixtures/content/01-hand-python/exercises/count-words/exercise.yaml`:

```yaml
title: Count words
kind: python
time_limit_s: 300
required: true
review: true
mock: true
rubric:
  - Correct for empty input and mixed case
  - Readable names and structure
  - No unnecessary code
```

`tests/fixtures/content/01-hand-python/exercises/count-words/prompt.md`:

```markdown
Write `count_words(text: str) -> dict[str, int]`.

Split `text` on whitespace, lowercase every word, and return how many times each word appears. An empty string returns an empty dict.
```

`tests/fixtures/content/01-hand-python/exercises/count-words/starter.py`:

```python
def count_words(text: str) -> dict[str, int]:
    pass
```

`tests/fixtures/content/01-hand-python/exercises/count-words/solution.py`:

```python
def count_words(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts
```

`tests/fixtures/content/01-hand-python/exercises/count-words/gaps.py`:

```python
def count_words(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in ____:
        counts[word] = ____
    return counts
```

`tests/fixtures/content/01-hand-python/exercises/count-words/tests/test_hidden.py`:

```python
from solution import count_words


def test_basic():
    assert count_words("a b a") == {"a": 2, "b": 1}


def test_mixed_case():
    assert count_words("A a") == {"a": 2}


def test_empty():
    assert count_words("") == {}
```

`tests/fixtures/content/01-hand-python/exercises/explain-count-words/exercise.yaml`:

```yaml
title: Explain count_words
kind: explain
required: true
```

`tests/fixtures/content/01-hand-python/exercises/explain-count-words/prompt.md`:

```markdown
Explain your `count_words` solution as you would to an interviewer: what it does step by step, its time complexity, and one input that could surprise a caller.
```

`tests/fixtures/content/03-hand-sql/step.yaml`:

```yaml
title: Hand-coding SQL
order: 3
```

`tests/fixtures/content/03-hand-sql/exercises/top-customers/exercise.yaml`:

```yaml
title: Top customers
kind: sql
time_limit_s: 300
required: true
mock: true
ordered: true
```

`tests/fixtures/content/03-hand-sql/exercises/top-customers/prompt.md`:

```markdown
Return each customer's `name` and their `total` order amount, only for customers whose total is above 100, highest total first.
```

`tests/fixtures/content/03-hand-sql/exercises/top-customers/seed.sql`:

```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL);
INSERT INTO customers VALUES (1, 'Ana'), (2, 'Bruno'), (3, 'Carla');
INSERT INTO orders VALUES (1, 1, 80), (2, 1, 70), (3, 2, 40), (4, 3, 200), (5, 3, 10);
```

`tests/fixtures/content/03-hand-sql/exercises/top-customers/starter.sql`:

```sql
SELECT
```

`tests/fixtures/content/03-hand-sql/exercises/top-customers/solution.sql`:

```sql
SELECT c.name, SUM(o.amount) AS total
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.name
HAVING SUM(o.amount) > 100
ORDER BY total DESC;
```

- [ ] **Step 2: Write `pyproject.toml` and extend `.gitignore`**

`pyproject.toml`:

```toml
[project]
name = "live-coding-gym"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi",
    "uvicorn",
    "pyyaml",
    "pytest",
    "pandas",
    "numpy",
    "scikit-learn",
]

[dependency-groups]
dev = ["httpx"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
norecursedirs = ["fixtures"]
```

`pytest` is a runtime dependency because the runner uses it to grade submissions. `pandas`, `numpy` and `scikit-learn` are there for exercises. `norecursedirs` stops pytest collecting the hidden tests inside the fixtures.

Append to `.gitignore`:

```
.venv/
__pycache__/
data/
```

Run: `uv sync`
Expected: a `.venv` is created with Python 3.12 and the packages install without error.

- [ ] **Step 3: Write the failing test**

`tests/conftest.py`:

```python
from pathlib import Path

import pytest

from gym.content import load_content

FIXTURES = Path(__file__).parent / "fixtures" / "content"


@pytest.fixture
def steps():
    return load_content(FIXTURES)[0]
```

`tests/test_content.py`:

```python
from gym.content import load_content
from tests.conftest import FIXTURES


def test_steps_load_in_order(steps):
    assert [s.id for s in steps] == ["01-hand-python", "03-hand-sql"]
    assert steps[0].min_score == 4
    assert steps[0].timed_required is True
    assert steps[1].timed_required is False


def test_python_exercise_fields(steps):
    ex = steps[0].exercises[0]
    assert ex.id == "count-words"
    assert ex.kind == "python"
    assert "def count_words" in ex.solution
    assert "____" in ex.gaps
    assert ex.review and ex.mock
    assert len(ex.rubric) == 3


def test_sql_exercise_has_seed(steps):
    ex = steps[1].exercises[0]
    assert ex.kind == "sql"
    assert "CREATE TABLE" in ex.seed
    assert ex.ordered is True


def test_lessons_and_cards(steps):
    assert steps[0].lessons[0]["title"] == "Counting with a dict"
    assert steps[0].cards[0]["id"] == "dict-count"


def test_broken_exercise_is_reported_and_skipped(tmp_path):
    step = tmp_path / "01-x"
    (step / "exercises" / "bad").mkdir(parents=True)
    (step / "step.yaml").write_text("title: X\norder: 1\n")
    (step / "exercises" / "bad" / "exercise.yaml").write_text("title: Bad\nkind: nope\n")
    (step / "exercises" / "bad" / "prompt.md").write_text("x")
    steps, errors = load_content(tmp_path)
    assert steps[0].exercises == []
    assert len(errors) == 1 and "nope" in errors[0]
```

Create an empty `tests/__init__.py` so `tests.conftest` is importable, and an empty `gym/__init__.py`.

- [ ] **Step 4: Run test to verify it fails**

Run: `uv run pytest tests/test_content.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'gym.content'`

- [ ] **Step 5: Write the implementation**

`gym/config.py`:

```python
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"
DB_PATH = ROOT / "data" / "progress.db"
WEB_DIR = ROOT / "web"


def load_env(path=ROOT / ".env"):
    """Read KEY=VALUE lines into os.environ without overriding existing values."""
    if not Path(path).exists():
        return
    for line in Path(path).read_text().splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())
```

`gym/content.py`:

```python
from dataclasses import dataclass, field
from pathlib import Path

import yaml

KINDS = {"python", "sql", "open", "prompt", "explain"}
EXT = {"python": "py", "sql": "sql"}


@dataclass
class Exercise:
    id: str
    step_id: str
    title: str
    kind: str
    prompt: str
    dir: Path
    starter: str = ""
    solution: str = ""
    gaps: str = ""
    seed: str = ""
    time_limit_s: int = 600
    required: bool = True
    review: bool = False
    mock: bool = False
    ordered: bool = False
    rubric: list = field(default_factory=list)


@dataclass
class Step:
    id: str
    title: str
    order: int
    min_score: int = 4
    timed_required: bool = False
    lessons: list = field(default_factory=list)
    exercises: list = field(default_factory=list)
    cards: list = field(default_factory=list)


def _read(path):
    return path.read_text() if path.exists() else ""


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
    )
    ext = EXT.get(kind)
    if ext:
        ex.starter = _read(d / f"starter.{ext}")
        ex.solution = (d / f"solution.{ext}").read_text()
        ex.gaps = _read(d / f"gaps.{ext}")
    if kind == "python" and not (d / "tests" / "test_hidden.py").exists():
        raise ValueError("missing tests/test_hidden.py")
    if kind == "sql":
        ex.seed = (d / "seed.sql").read_text()
    return ex


def load_content(content_dir):
    steps, errors = [], []
    content_dir = Path(content_dir)
    if not content_dir.exists():
        return steps, [f"content directory not found: {content_dir}"]
    for sd in sorted(p for p in content_dir.iterdir() if (p / "step.yaml").exists()):
        meta = yaml.safe_load((sd / "step.yaml").read_text())
        gate = meta.get("gate") or {}
        step = Step(
            id=sd.name,
            title=meta["title"],
            order=meta["order"],
            min_score=gate.get("min_score", 4),
            timed_required=gate.get("timed_required", False),
            cards=yaml.safe_load(_read(sd / "cards.yaml")) or [],
        )
        for lp in sorted((sd / "lessons").glob("*.md")):
            body = lp.read_text()
            title = body.splitlines()[0].lstrip("# ").strip() if body.strip() else lp.stem
            step.lessons.append({"id": lp.stem, "title": title, "body": body})
        ex_root = sd / "exercises"
        for ed in sorted(p for p in ex_root.iterdir() if p.is_dir()) if ex_root.exists() else []:
            try:
                step.exercises.append(load_exercise(ed, sd.name))
            except Exception as e:  # one broken exercise must not stop the app
                errors.append(f"{ed}: {e}")
        steps.append(step)
    steps.sort(key=lambda s: s.order)
    return steps, errors
```

- [ ] **Step 6: Run test to verify it passes**

Run: `uv run pytest tests/test_content.py -v`
Expected: 5 passed

- [ ] **Step 7: Commit**

```bash
git add pyproject.toml uv.lock .gitignore gym tests
git commit -m "feat: project skeleton, config and content loader"
```

---

### Task 2: Python runner

**Files:**
- Create: `gym/runner.py`
- Test: `tests/test_runner_python.py`

**Interfaces:**
- Consumes: sample exercise directory `FIXTURES / "01-hand-python" / "exercises" / "count-words"`.
- Produces: `gym.runner.RunResult(passed: bool, tests: list[dict], output: str, timed_out: bool)` where each test dict is `{"name": str, "passed": bool}`; `run_python_tests(code: str, tests_dir: Path, timeout: int = 10) -> RunResult`; `run_python_free(code: str, timeout: int = 10) -> RunResult`.

- [ ] **Step 1: Write the failing test**

`tests/test_runner_python.py`:

```python
from gym.runner import run_python_free, run_python_tests
from tests.conftest import FIXTURES

EX = FIXTURES / "01-hand-python" / "exercises" / "count-words"


def test_reference_solution_passes():
    r = run_python_tests((EX / "solution.py").read_text(), EX / "tests")
    assert r.passed
    assert {t["name"] for t in r.tests} == {"test_basic", "test_mixed_case", "test_empty"}
    assert all(t["passed"] for t in r.tests)


def test_wrong_solution_reports_each_test():
    code = "def count_words(text):\n    return {}\n"
    r = run_python_tests(code, EX / "tests")
    assert not r.passed
    by_name = {t["name"]: t["passed"] for t in r.tests}
    assert by_name == {"test_basic": False, "test_mixed_case": False, "test_empty": True}


def test_syntax_error_is_a_failed_run_not_a_crash():
    r = run_python_tests("def count_words(:\n", EX / "tests")
    assert not r.passed
    assert "SyntaxError" in r.output


def test_infinite_loop_times_out():
    code = "def count_words(text):\n    while True:\n        pass\n"
    r = run_python_tests(code, EX / "tests", timeout=2)
    assert not r.passed and r.timed_out


def test_free_run_captures_output():
    r = run_python_free("print(1 + 1)")
    assert r.passed and r.output.strip() == "2"


def test_free_run_reports_exception():
    r = run_python_free("raise ValueError('boom')")
    assert not r.passed and "boom" in r.output
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_runner_python.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'gym.runner'`

- [ ] **Step 3: Write the implementation**

`gym/runner.py`:

```python
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RunResult:
    passed: bool
    tests: list = field(default_factory=list)
    output: str = ""
    timed_out: bool = False


def run_python_tests(code, tests_dir, timeout=10):
    """Run hidden pytest tests against a submission saved as solution.py."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "solution.py").write_text(code)
        shutil.copytree(tests_dir, tmp / "tests")
        cmd = [sys.executable, "-m", "pytest", "tests", "-q", "--tb=short",
               "-p", "no:cacheprovider", "--junitxml=report.xml"]
        try:
            # `python -m pytest` puts the working directory on sys.path,
            # which is what lets the tests `from solution import ...`.
            proc = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return RunResult(False, [], f"Timed out after {timeout}s", True)
        tests = []
        report = tmp / "report.xml"
        if report.exists():
            for case in ET.parse(report).iter("testcase"):
                failed = case.find("failure") is not None or case.find("error") is not None
                tests.append({"name": case.get("name"), "passed": not failed})
        return RunResult(proc.returncode == 0, tests, proc.stdout + proc.stderr)


def run_python_free(code, timeout=10):
    """Run code as a script with no tests, like the Run button on Coderbyte."""
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "main.py").write_text(code)
        try:
            proc = subprocess.run([sys.executable, "main.py"], cwd=tmp,
                                  capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return RunResult(False, [], f"Timed out after {timeout}s", True)
        return RunResult(proc.returncode == 0, [], proc.stdout + proc.stderr)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_runner_python.py -v`
Expected: 6 passed

- [ ] **Step 5: Commit**

```bash
git add gym/runner.py tests/test_runner_python.py
git commit -m "feat: run Python submissions under pytest"
```

---

### Task 3: SQL runner

**Files:**
- Modify: `gym/runner.py` (append)
- Test: `tests/test_runner_sql.py`

**Interfaces:**
- Consumes: `RunResult` from Task 2.
- Produces: `run_sql_free(seed: str, sql: str, timeout: float = 5) -> RunResult` (output is a text table or the SQLite error); `check_sql(seed: str, sql: str, solution: str, ordered: bool = False, timeout: float = 5) -> RunResult` (one test named `result matches reference`). Comparison is on row values only; column names are ignored.

- [ ] **Step 1: Write the failing test**

`tests/test_runner_sql.py`:

```python
from gym.runner import check_sql, run_sql_free
from tests.conftest import FIXTURES

EX = FIXTURES / "03-hand-sql" / "exercises" / "top-customers"
SEED = (EX / "seed.sql").read_text()
SOLUTION = (EX / "solution.sql").read_text()


def test_reference_matches_itself():
    assert check_sql(SEED, SOLUTION, SOLUTION, ordered=True).passed


def test_free_run_shows_rows():
    r = run_sql_free(SEED, "SELECT name FROM customers ORDER BY id")
    assert r.passed
    assert r.output.splitlines() == ["name", "Ana", "Bruno", "Carla"]


def test_wrong_order_fails_only_when_ordered():
    asc = SOLUTION.replace("DESC", "ASC")
    assert not check_sql(SEED, asc, SOLUTION, ordered=True).passed
    assert check_sql(SEED, asc, SOLUTION, ordered=False).passed


def test_duplicates_are_not_collapsed():
    seed = "CREATE TABLE t (x INTEGER); INSERT INTO t VALUES (1), (1), (2);"
    assert not check_sql(seed, "SELECT DISTINCT x FROM t", "SELECT x FROM t").passed


def test_nulls_compare_equal():
    seed = "CREATE TABLE t (x INTEGER); INSERT INTO t VALUES (NULL), (1);"
    assert check_sql(seed, "SELECT x FROM t ORDER BY x DESC", "SELECT x FROM t").passed


def test_sql_error_is_reported():
    r = check_sql(SEED, "SELEC nope", SOLUTION)
    assert not r.passed and "syntax error" in r.output


def test_runaway_query_is_stopped():
    q = "WITH RECURSIVE n(i) AS (SELECT 1 UNION ALL SELECT i + 1 FROM n) SELECT COUNT(*) FROM n"
    r = run_sql_free(SEED, q, timeout=0.5)
    assert not r.passed and "interrupted" in r.output
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_runner_sql.py -v`
Expected: FAIL with `ImportError: cannot import name 'check_sql'`

- [ ] **Step 3: Write the implementation**

Add to the imports at the top of `gym/runner.py`:

```python
import sqlite3
import time
```

Append to `gym/runner.py`:

```python
def _query(seed, sql, timeout):
    conn = sqlite3.connect(":memory:")
    try:
        conn.executescript(seed)
        deadline = time.monotonic() + timeout
        # A truthy return from the progress handler aborts the running query.
        conn.set_progress_handler(lambda: time.monotonic() > deadline, 10000)
        cur = conn.execute(sql)
        cols = [d[0] for d in cur.description or []]
        return cols, cur.fetchall()
    finally:
        conn.close()


def _table(cols, rows, limit=50):
    lines = [" | ".join(cols)] + [" | ".join(str(v) for v in r) for r in rows[:limit]]
    if len(rows) > limit:
        lines.append(f"... {len(rows) - limit} more rows")
    return "\n".join(lines)


def run_sql_free(seed, sql, timeout=5):
    try:
        cols, rows = _query(seed, sql, timeout)
    except (sqlite3.Error, sqlite3.Warning) as e:
        return RunResult(False, [], str(e))
    return RunResult(True, [], _table(cols, rows))


def check_sql(seed, sql, solution, ordered=False, timeout=5):
    try:
        cols, got = _query(seed, sql, timeout)
    except (sqlite3.Error, sqlite3.Warning) as e:
        return RunResult(False, [{"name": "result matches reference", "passed": False}], str(e))
    _, want = _query(seed, solution, timeout)

    def norm(rows):
        return rows if ordered else sorted(rows, key=repr)

    passed = norm(got) == norm(want)
    output = _table(cols, got)
    if not passed:
        output += f"\n\nExpected {len(want)} rows, got {len(got)}."
        if ordered and sorted(got, key=repr) == sorted(want, key=repr):
            output += " The rows are right but the order is wrong."
    return RunResult(passed, [{"name": "result matches reference", "passed": passed}], output)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_runner_sql.py -v`
Expected: 7 passed

- [ ] **Step 5: Commit**

```bash
git add gym/runner.py tests/test_runner_sql.py
git commit -m "feat: run and compare SQL submissions"
```

---

### Task 4: Progress storage

**Files:**
- Create: `gym/db.py`
- Modify: `tests/conftest.py` (add `conn` fixture)
- Test: `tests/test_db.py`

**Interfaces:**
- Produces (all take an open `sqlite3.Connection` whose rows are `sqlite3.Row`):
  - `connect(path) -> sqlite3.Connection` (creates parent folder and tables)
  - `record_attempt(conn, exercise_id, mode, code, passed, duration_s, output) -> int`
  - `get_attempt(conn, attempt_id) -> Row | None`
  - `passed_attempts(conn, exercise_id) -> list[Row]` (columns include `mode`, `duration_s`)
  - `save_review(conn, exercise_id, kind, material: dict, result: dict, attempt_id=None) -> int`
  - `update_review(conn, review_id, result: dict) -> None`
  - `get_review(conn, review_id) -> Row | None`
  - `latest_review(conn, exercise_id, kind) -> Row | None` (columns include `status`, `scores_json`, `material_json`)
  - `unlock(conn, step_id) -> None`, `unlocked(conn) -> set[str]`
  - `create_mock(conn, state: dict) -> int`, `get_mock(conn, mock_id) -> Row | None`, `update_mock(conn, mock_id, state: dict, score: dict | None = None) -> None`, `finished_mocks(conn) -> list[Row]` (newest first, columns `id, started_at, score_json`)
- A review `result` dict always has keys `status` (`"done"` or `"pending"`), `scores` (dict), `verdict` (str), `feedback` (str).

- [ ] **Step 1: Write the failing test**

Append to `tests/conftest.py`:

```python
from gym import db


@pytest.fixture
def conn(tmp_path):
    return db.connect(tmp_path / "data" / "progress.db")
```

`tests/test_db.py`:

```python
import json

from gym import db

DONE = {"status": "done", "scores": {"a": 4}, "verdict": "ok", "feedback": "fine"}
PENDING = {"status": "pending", "scores": {}, "verdict": "", "feedback": "down"}


def test_attempts_round_trip(conn):
    a = db.record_attempt(conn, "ex", "blank", "code", True, 12.5, "out")
    db.record_attempt(conn, "ex", "blank", "bad", False, 3, "out")
    assert db.get_attempt(conn, a)["code"] == "code"
    rows = db.passed_attempts(conn, "ex")
    assert [(r["mode"], r["duration_s"]) for r in rows] == [("blank", 12.5)]


def test_latest_review_is_per_kind(conn):
    db.save_review(conn, "ex", "code", {"code": "x"}, DONE)
    rid = db.save_review(conn, "ex", "code", {"code": "y"}, PENDING)
    db.save_review(conn, "ex", "explain", {"answer": "z"}, DONE)
    latest = db.latest_review(conn, "ex", "code")
    assert latest["id"] == rid and latest["status"] == "pending"
    assert json.loads(latest["material_json"]) == {"code": "y"}


def test_update_review(conn):
    rid = db.save_review(conn, "ex", "code", {}, PENDING)
    db.update_review(conn, rid, DONE)
    row = db.get_review(conn, rid)
    assert row["status"] == "done" and json.loads(row["scores_json"]) == {"a": 4}


def test_unlocks(conn):
    db.unlock(conn, "03-hand-sql")
    db.unlock(conn, "03-hand-sql")
    assert db.unlocked(conn) == {"03-hand-sql"}


def test_mocks(conn):
    m = db.create_mock(conn, {"python_id": "a"})
    assert db.finished_mocks(conn) == []
    db.update_mock(conn, m, {"python_id": "a", "done": True}, {"total": 70})
    rows = db.finished_mocks(conn)
    assert json.loads(rows[0]["score_json"]) == {"total": 70}
    assert json.loads(db.get_mock(conn, m)["state_json"])["done"] is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_db.py -v`
Expected: FAIL with `ImportError: cannot import name 'db' from 'gym'`

- [ ] **Step 3: Write the implementation**

`gym/db.py`:

```python
import json
import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY, exercise_id TEXT, mode TEXT, code TEXT,
    passed INTEGER, duration_s REAL, output TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY, exercise_id TEXT, attempt_id INTEGER, kind TEXT,
    material_json TEXT, status TEXT, scores_json TEXT, verdict TEXT, feedback TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS cards (card_id TEXT PRIMARY KEY, box INTEGER, due TEXT);
CREATE TABLE IF NOT EXISTS unlocks (step_id TEXT PRIMARY KEY);
CREATE TABLE IF NOT EXISTS mocks (
    id INTEGER PRIMARY KEY, started_at TEXT DEFAULT CURRENT_TIMESTAMP,
    state_json TEXT, score_json TEXT);
"""


def connect(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    # ponytail: one shared connection across FastAPI's worker threads. Fine for
    # a single local user; use a connection per request if writes ever overlap.
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def _insert(conn, sql, params):
    cur = conn.execute(sql, params)
    conn.commit()
    return cur.lastrowid


def record_attempt(conn, exercise_id, mode, code, passed, duration_s, output):
    return _insert(
        conn,
        "INSERT INTO attempts (exercise_id, mode, code, passed, duration_s, output) VALUES (?,?,?,?,?,?)",
        (exercise_id, mode, code, int(passed), duration_s, output),
    )


def get_attempt(conn, attempt_id):
    return conn.execute("SELECT * FROM attempts WHERE id = ?", (attempt_id,)).fetchone()


def passed_attempts(conn, exercise_id):
    return conn.execute(
        "SELECT * FROM attempts WHERE exercise_id = ? AND passed = 1", (exercise_id,)
    ).fetchall()


def save_review(conn, exercise_id, kind, material, result, attempt_id=None):
    return _insert(
        conn,
        "INSERT INTO reviews (exercise_id, attempt_id, kind, material_json, status, scores_json, verdict, feedback)"
        " VALUES (?,?,?,?,?,?,?,?)",
        (exercise_id, attempt_id, kind, json.dumps(material), result["status"],
         json.dumps(result["scores"]), result["verdict"], result["feedback"]),
    )


def update_review(conn, review_id, result):
    conn.execute(
        "UPDATE reviews SET status = ?, scores_json = ?, verdict = ?, feedback = ? WHERE id = ?",
        (result["status"], json.dumps(result["scores"]), result["verdict"], result["feedback"], review_id),
    )
    conn.commit()


def get_review(conn, review_id):
    return conn.execute("SELECT * FROM reviews WHERE id = ?", (review_id,)).fetchone()


def latest_review(conn, exercise_id, kind):
    return conn.execute(
        "SELECT * FROM reviews WHERE exercise_id = ? AND kind = ? ORDER BY id DESC LIMIT 1",
        (exercise_id, kind),
    ).fetchone()


def unlock(conn, step_id):
    conn.execute("INSERT OR IGNORE INTO unlocks (step_id) VALUES (?)", (step_id,))
    conn.commit()


def unlocked(conn):
    return {r["step_id"] for r in conn.execute("SELECT step_id FROM unlocks")}


def create_mock(conn, state):
    return _insert(conn, "INSERT INTO mocks (state_json) VALUES (?)", (json.dumps(state),))


def get_mock(conn, mock_id):
    return conn.execute("SELECT * FROM mocks WHERE id = ?", (mock_id,)).fetchone()


def update_mock(conn, mock_id, state, score=None):
    conn.execute(
        "UPDATE mocks SET state_json = ?, score_json = ? WHERE id = ?",
        (json.dumps(state), json.dumps(score) if score is not None else None, mock_id),
    )
    conn.commit()


def finished_mocks(conn):
    return conn.execute(
        "SELECT id, started_at, score_json FROM mocks WHERE score_json IS NOT NULL ORDER BY id DESC"
    ).fetchall()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_db.py -v`
Expected: 5 passed

- [ ] **Step 5: Commit**

```bash
git add gym/db.py tests/conftest.py tests/test_db.py
git commit -m "feat: progress storage"
```

---

### Task 5: Gemini reviewer

**Files:**
- Create: `gym/reviewer.py`
- Modify: `.env` (add `GEMINI_MODEL`; do not print the file)
- Test: `tests/test_reviewer.py`

**Interfaces:**
- Produces:
  - `REVIEW_KIND: dict[str, str]` mapping exercise kind to review kind: `python -> code`, `sql -> code`, `explain -> explain`, `prompt -> prompt`, `open -> open`.
  - `DEFAULT_RUBRICS: dict[str, list[str]]` for review kinds `code, explain, prompt, open, mock`.
  - `call_gemini(prompt: str, timeout: int = 60) -> str` (the model's text reply).
  - `review(kind: str, rubric: list[str] | None, material: dict, call=call_gemini) -> dict` returning `{"status": "done" | "pending", "scores": {criterion: int 1..5}, "verdict": str, "feedback": str}`. One retry, then `pending`. Never raises.
  - `followups(task: str, code: str, call=call_gemini) -> list[str]` returning exactly 3 questions (a fixed fallback list if Gemini fails). Never raises.
- The review prompt always contains the sentence `Return exactly N scores` where N is the rubric length. Test stubs rely on this.

- [ ] **Step 1: Check the key against the live API before building on it**

Run (prints only the HTTP status and model names, never the key):

```bash
uv run python - <<'EOF'
import json, os, urllib.request, urllib.error
from gym.config import load_env
load_env()
req = urllib.request.Request(
    "https://generativelanguage.googleapis.com/v1beta/models",
    headers={"x-goog-api-key": os.environ["GEMINI_API_KEY"]})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        names = [m["name"] for m in json.load(r)["models"]
                 if "generateContent" in m.get("supportedGenerationMethods", [])]
    print("OK", *names, sep="\n")
except urllib.error.HTTPError as e:
    print("HTTP", e.code, e.read().decode()[:300])
EOF
```

Expected: `OK` followed by model names such as `models/gemini-2.5-flash`.

Pick the newest listed "flash" model (fast and cheap is right for reviews) and append it to `.env` without the `models/` prefix, for example:

```bash
echo 'GEMINI_MODEL=gemini-2.5-flash' >> .env
```

If the call returns an HTTP error (401, 403 or 404), STOP. Do not continue this task. Report the status code and the error message to the user: the key may belong to a different Google service (for example Vertex AI) and need a different endpoint, which is a decision for the user.

- [ ] **Step 2: Write the failing test**

`tests/test_reviewer.py`:

```python
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
```

- [ ] **Step 3: Run test to verify it fails**

Run: `uv run pytest tests/test_reviewer.py -v`
Expected: FAIL with `ImportError: cannot import name 'reviewer' from 'gym'`

- [ ] **Step 4: Write the implementation**

`gym/reviewer.py`:

```python
import json
import os
import urllib.request

API = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

REVIEW_KIND = {"python": "code", "sql": "code", "explain": "explain", "prompt": "prompt", "open": "open"}

DEFAULT_RUBRICS = {
    "code": [
        "Correct, including edge cases the tests may not cover",
        "Readable: clear names and structure",
        "Robust: handles bad or unexpected input sensibly",
        "No unnecessary complexity",
    ],
    "explain": [
        "Accurately describes what the code does, step by step",
        "States trade-offs and complexity",
        "Names failure modes and limits honestly",
        "Clear and concise, as spoken to an interviewer",
    ],
    "prompt": [
        "States the task, inputs, outputs and constraints precisely",
        "Asks for robustness: validation, edge cases, determinism",
        "Keeps the candidate in control: small scope, asks for tests or explanation",
        "Would convince an observer the candidate understands the problem",
    ],
    "open": [
        "Technically accurate",
        "Shows understanding of what problem the tool or idea solves",
        "Gives a concrete example",
        "Honest about limits of own experience",
    ],
    "mock": [
        "Answers the follow-up questions directly and correctly",
        "Explains reasoning and trade-offs behind the code",
        "Identifies what could fail in production",
        "Communicates clearly under pressure",
    ],
}

ROLES = {
    "code": "You are a senior engineer interviewing a candidate for a production ML systems role. Review the candidate's code.",
    "explain": "You are an interviewer. The candidate is explaining their own code after a live-coding exercise. Judge the explanation.",
    "prompt": "You are an interviewer watching a candidate use an AI coding assistant. Judge the prompt the candidate wrote for the assistant.",
    "open": "You are an interviewer for an AI/ML engineering role. Grade the candidate's answer to a theory question.",
    "mock": "You are an interviewer. Grade the candidate's answers to your follow-up questions about their code.",
}

FALLBACK_QUESTIONS = [
    "Walk me through your code line by line. Why did you structure it this way?",
    "What inputs would break this code, and how would you defend against them?",
    "How would this behave in production with 100 times more data, and what would you monitor?",
]


def call_gemini(prompt, timeout=60):
    model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"},
    }).encode()
    req = urllib.request.Request(
        API.format(model=model),
        data=body,
        headers={"Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]},
    )
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = json.load(r)
    return data["candidates"][0]["content"]["parts"][0]["text"]


def _material(material):
    return "\n\n".join(f"## {k.upper()}\n{v}" for k, v in material.items() if v)


def build_prompt(kind, rubric, material):
    criteria = "\n".join(f"- {c}" for c in rubric)
    return (
        f"{ROLES[kind]}\n\n"
        "Score each criterion from 1 (poor) to 5 (excellent). Be strict: 4 means an "
        "interviewer would be satisfied, 5 means impressed.\n\n"
        f"Criteria, in order:\n{criteria}\n\n"
        f"{_material(material)}\n\n"
        f"Return exactly {len(rubric)} scores, in the same order as the criteria, as JSON:\n"
        '{"scores": [int, ...], "verdict": "one sentence", '
        '"feedback": "specific, actionable feedback that quotes the candidate\'s work"}'
    )


def parse_review(text, rubric):
    data = json.loads(text)
    scores = [int(s) for s in data["scores"]]
    if len(scores) != len(rubric) or not all(1 <= s <= 5 for s in scores):
        raise ValueError(f"bad scores: {scores}")
    return {"scores": dict(zip(rubric, scores)), "verdict": str(data["verdict"]),
            "feedback": str(data["feedback"])}


def review(kind, rubric, material, call=call_gemini):
    rubric = rubric or DEFAULT_RUBRICS[kind]
    prompt = build_prompt(kind, rubric, material)
    error = None
    for _ in range(2):
        try:
            return {"status": "done", **parse_review(call(prompt), rubric)}
        except Exception as e:  # network, quota, bad JSON: all end as pending
            error = e
    return {"status": "pending", "scores": {}, "verdict": "",
            "feedback": f"Review unavailable: {error}. Your submission is saved; retry later."}


def followups(task, code, call=call_gemini):
    prompt = (
        "You are an interviewer for a production ML systems role. The candidate just "
        "finished this live-coding task. Ask exactly 3 follow-up questions that probe "
        "whether they understand their own code: design choices, edge cases, and "
        "production behaviour. Refer to specific lines.\n\n"
        f"## TASK\n{task}\n\n## CODE\n{code}\n\n"
        'Return JSON: {"questions": ["...", "...", "..."]}'
    )
    try:
        questions = [str(q) for q in json.loads(call(prompt))["questions"]][:3]
        if len(questions) == 3:
            return questions
    except Exception:
        pass
    return FALLBACK_QUESTIONS
```

- [ ] **Step 5: Run test to verify it passes**

Run: `uv run pytest tests/test_reviewer.py -v`
Expected: 8 passed

- [ ] **Step 6: Run one real review against Gemini**

```bash
uv run python - <<'EOF'
from gym.config import load_env
from gym import reviewer
load_env()
r = reviewer.review("code", None, {"task": "Sum a list of numbers.",
                                   "code": "def total(xs):\n    return sum(xs)"})
print(r["status"], r["scores"], r["verdict"], sep="\n")
EOF
```

Expected: `done`, a dict with four criteria scored 1 to 5, and a one-sentence verdict. If it prints `pending`, read the feedback text, fix the cause (usually the model name in `.env`), and rerun.

- [ ] **Step 7: Commit**

```bash
git add gym/reviewer.py tests/test_reviewer.py
git commit -m "feat: Gemini reviewer with rubric scoring and pending fallback"
```

---

### Task 6: Gates

**Files:**
- Create: `gym/gates.py`
- Test: `tests/test_gates.py`

**Interfaces:**
- Consumes: `Step`, `Exercise` (Task 1); `db.passed_attempts`, `db.latest_review`, `db.unlocked` (Task 4); `reviewer.REVIEW_KIND` (Task 5).
- Produces:
  - `exercise_status(conn, ex, step) -> dict` with keys `tests`, `timed`, `review` (each `True`, `False`, or `None` when that requirement does not apply) and `done` (bool).
  - `step_status(conn, step) -> dict` with keys `passed` (bool), `done` (int), `total` (int, required exercises), `exercises` (dict of exercise id to `exercise_status`).
  - `journey(conn, steps) -> list[dict]`, one dict per step with keys `id, title, order, passed, done, total, unlocked`.
- Rules: a coded exercise (python or sql) needs a passed attempt in mode `blank` or `timed`. If the step has `timed_required`, it also needs a passed `timed` attempt with `duration_s <= time_limit_s`. A review is needed when the exercise has `review: true` or is not coded; the latest review of its kind must be `done` with every score `>= step.min_score`. A step passes when it has at least one required exercise and all required exercises are done. A step is unlocked when it is first, the previous step passed, or it was unlocked by hand.

- [ ] **Step 1: Write the failing test**

`tests/test_gates.py`:

```python
from gym import db, gates


def good(score=4):
    return {"status": "done", "scores": {"a": score, "b": 5}, "verdict": "v", "feedback": "f"}


def test_fresh_journey_only_first_step_unlocked(conn, steps):
    j = gates.journey(conn, steps)
    assert [(s["id"], s["unlocked"], s["passed"]) for s in j] == [
        ("01-hand-python", True, False), ("03-hand-sql", False, False)]
    assert j[0]["total"] == 2 and j[0]["done"] == 0


def test_retype_and_gaps_passes_do_not_count(conn, steps):
    step, ex = steps[0], steps[0].exercises[0]
    db.record_attempt(conn, ex.id, "retype", "c", True, 10, "")
    db.record_attempt(conn, ex.id, "gaps", "c", True, 10, "")
    assert gates.exercise_status(conn, ex, step)["tests"] is False


def test_timed_requirement(conn, steps):
    step, ex = steps[0], steps[0].exercises[0]
    db.record_attempt(conn, ex.id, "blank", "c", True, 999, "")
    st = gates.exercise_status(conn, ex, step)
    assert st["tests"] is True and st["timed"] is False
    db.record_attempt(conn, ex.id, "timed", "c", True, ex.time_limit_s + 1, "")
    assert gates.exercise_status(conn, ex, step)["timed"] is False
    db.record_attempt(conn, ex.id, "timed", "c", True, ex.time_limit_s, "")
    assert gates.exercise_status(conn, ex, step)["timed"] is True


def test_review_must_be_done_and_meet_min_score(conn, steps):
    step, ex = steps[0], steps[0].exercises[0]
    assert gates.exercise_status(conn, ex, step)["review"] is False
    db.save_review(conn, ex.id, "code", {}, good(score=3))
    assert gates.exercise_status(conn, ex, step)["review"] is False
    db.save_review(conn, ex.id, "code", {}, good(score=4))
    assert gates.exercise_status(conn, ex, step)["review"] is True
    db.save_review(conn, ex.id, "code", {}, {"status": "pending", "scores": {}, "verdict": "", "feedback": ""})
    assert gates.exercise_status(conn, ex, step)["review"] is False


def test_uncoded_exercise_needs_only_review(conn, steps):
    step, ex = steps[0], steps[0].exercises[1]
    st = gates.exercise_status(conn, ex, step)
    assert st["tests"] is None and st["timed"] is None and st["review"] is False
    db.save_review(conn, ex.id, "explain", {}, good())
    assert gates.exercise_status(conn, ex, step)["done"] is True


def test_step_passes_and_unlocks_next(conn, steps):
    code_ex, explain_ex = steps[0].exercises
    db.record_attempt(conn, code_ex.id, "timed", "c", True, 100, "")
    db.save_review(conn, code_ex.id, "code", {}, good())
    db.save_review(conn, explain_ex.id, "explain", {}, good())
    j = gates.journey(conn, steps)
    assert j[0]["passed"] is True and j[0]["done"] == 2
    assert j[1]["unlocked"] is True


def test_sql_step_without_timed_or_review(conn, steps):
    step, ex = steps[1], steps[1].exercises[0]
    db.record_attempt(conn, ex.id, "blank", "q", True, 5000, "")
    st = gates.exercise_status(conn, ex, step)
    assert st == {"tests": True, "timed": None, "review": None, "done": True}
    assert gates.step_status(conn, step)["passed"] is True


def test_manual_unlock(conn, steps):
    db.unlock(conn, "03-hand-sql")
    assert gates.journey(conn, steps)[1]["unlocked"] is True


def test_step_with_no_required_exercises_never_passes(conn, steps):
    step = steps[1]
    step.exercises[0].required = False
    assert gates.step_status(conn, step)["passed"] is False
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_gates.py -v`
Expected: FAIL with `ImportError: cannot import name 'gates' from 'gym'`

- [ ] **Step 3: Write the implementation**

`gym/gates.py`:

```python
import json

from . import db
from .reviewer import REVIEW_KIND


def _review_ok(conn, ex, min_score):
    row = db.latest_review(conn, ex.id, REVIEW_KIND[ex.kind])
    if row is None or row["status"] != "done":
        return False
    scores = json.loads(row["scores_json"])
    return bool(scores) and min(scores.values()) >= min_score


def exercise_status(conn, ex, step):
    coded = ex.kind in ("python", "sql")
    rows = db.passed_attempts(conn, ex.id) if coded else []
    status = {"tests": None, "timed": None, "review": None}
    if coded:
        status["tests"] = any(r["mode"] in ("blank", "timed") for r in rows)
        if step.timed_required:
            status["timed"] = any(
                r["mode"] == "timed" and r["duration_s"] <= ex.time_limit_s for r in rows)
    if ex.review or not coded:
        status["review"] = _review_ok(conn, ex, step.min_score)
    status["done"] = all(v for v in status.values() if v is not None)
    return status


def step_status(conn, step):
    exercises = {ex.id: exercise_status(conn, ex, step) for ex in step.exercises}
    required = [ex.id for ex in step.exercises if ex.required]
    done = sum(exercises[i]["done"] for i in required)
    return {"passed": bool(required) and done == len(required),
            "done": done, "total": len(required), "exercises": exercises}


def journey(conn, steps):
    manual = db.unlocked(conn)
    out, previous_passed = [], True
    for step in steps:
        st = step_status(conn, step)
        out.append({"id": step.id, "title": step.title, "order": step.order,
                    "passed": st["passed"], "done": st["done"], "total": st["total"],
                    "unlocked": previous_passed or step.id in manual})
        previous_passed = st["passed"]
    return out
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_gates.py -v`
Expected: 9 passed

- [ ] **Step 5: Commit**

```bash
git add gym/gates.py tests/test_gates.py
git commit -m "feat: exercise and step gates"
```

---

### Task 7: Flashcard schedule

**Files:**
- Create: `gym/cards.py`
- Test: `tests/test_cards.py`

**Interfaces:**
- Consumes: the `cards` table from Task 4 (`card_id`, `box`, `due` as ISO date text); card dicts `{"id", "front", "back"}` from `Step.cards`.
- Produces: `INTERVALS = [1, 2, 4, 8, 16]` (days per box 1 to 5); `due(conn, cards: list[dict], today: date) -> list[dict]` (cards never seen, or whose due date is today or earlier); `record(conn, card_id: str, correct: bool, today: date) -> dict` returning `{"box": int, "due": "YYYY-MM-DD"}`.
- Rules: a correct answer moves the card up one box (maximum 5) and schedules it `INTERVALS[box - 1]` days ahead. A wrong answer sends it to box 1 and leaves it due today, so it returns in the same session.

- [ ] **Step 1: Write the failing test**

`tests/test_cards.py`:

```python
from datetime import date, timedelta

from gym import cards

DAY = date(2026, 11, 14)
DECK = [{"id": "a", "front": "f", "back": "b"}, {"id": "b", "front": "f", "back": "b"}]


def test_unseen_cards_are_due(conn):
    assert cards.due(conn, DECK, DAY) == DECK


def test_correct_answers_climb_boxes(conn):
    assert cards.record(conn, "a", True, DAY) == {"box": 1, "due": "2026-11-15"}
    assert cards.record(conn, "a", True, DAY) == {"box": 2, "due": "2026-11-16"}
    assert cards.record(conn, "a", True, DAY) == {"box": 3, "due": "2026-11-18"}


def test_box_is_capped_at_five(conn):
    for _ in range(8):
        r = cards.record(conn, "a", True, DAY)
    assert r == {"box": 5, "due": "2026-11-30"}


def test_wrong_answer_resets_and_stays_due(conn):
    cards.record(conn, "a", True, DAY)
    cards.record(conn, "a", True, DAY)
    assert cards.record(conn, "a", False, DAY) == {"box": 1, "due": "2026-11-14"}
    assert [c["id"] for c in cards.due(conn, DECK, DAY)] == ["a", "b"]


def test_card_returns_on_its_due_date(conn):
    cards.record(conn, "a", True, DAY)
    assert [c["id"] for c in cards.due(conn, DECK, DAY)] == ["b"]
    assert [c["id"] for c in cards.due(conn, DECK, DAY + timedelta(days=1))] == ["a", "b"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_cards.py -v`
Expected: FAIL with `ImportError: cannot import name 'cards' from 'gym'`

- [ ] **Step 3: Write the implementation**

`gym/cards.py`:

```python
from datetime import timedelta

INTERVALS = [1, 2, 4, 8, 16]  # days until a card in box 1..5 returns


def due(conn, cards, today):
    scheduled = {r["card_id"]: r["due"] for r in conn.execute("SELECT card_id, due FROM cards")}
    return [c for c in cards if scheduled.get(c["id"], "") <= today.isoformat()]


def record(conn, card_id, correct, today):
    row = conn.execute("SELECT box FROM cards WHERE card_id = ?", (card_id,)).fetchone()
    if correct:
        box = min((row["box"] if row else 0) + 1, len(INTERVALS))
        due_date = today + timedelta(days=INTERVALS[box - 1])
    else:
        box, due_date = 1, today
    conn.execute(
        "INSERT INTO cards (card_id, box, due) VALUES (?, ?, ?) "
        "ON CONFLICT(card_id) DO UPDATE SET box = excluded.box, due = excluded.due",
        (card_id, box, due_date.isoformat()),
    )
    conn.commit()
    return {"box": box, "due": due_date.isoformat()}
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_cards.py -v`
Expected: 5 passed

- [ ] **Step 5: Commit**

```bash
git add gym/cards.py tests/test_cards.py
git commit -m "feat: flashcard schedule"
```

---

### Task 8: Mock scoring and readiness

**Files:**
- Create: `gym/mock.py`
- Test: `tests/test_mock.py`

**Interfaces:**
- Consumes: `Step`/`Exercise` (Task 1), `db.finished_mocks` (Task 4). Test results are plain dicts with keys `passed` and `tests` (the `asdict` form of `RunResult`).
- Produces: `MOCK_TIME_S = 2700`; `pick(steps, rng=random) -> tuple[Exercise, Exercise]` (one python and one sql exercise with `mock: true`; raises `ValueError` if either pool is empty); `score(python_result: dict, sql_result: dict, review_scores: list[dict], duration_s: float) -> dict` with keys `pass_rate` (0 to 1), `review_avg` (0 to 5), `in_time` (bool), `total` (0 to 100 int); `readiness(conn) -> int | None` (mean `total` of the last three finished mocks, `None` with fewer than three).
- Formula: `total = round(100 * (0.5 * pass_rate + 0.4 * review_avg / 5 + 0.1 * in_time))`. `pass_rate` is passed tests over all tests in both tasks. `review_avg` is the mean of every score in every review; reviews that are pending contribute no scores, and with no scores at all `review_avg` is 0.

- [ ] **Step 1: Write the failing test**

`tests/test_mock.py`:

```python
import random

import pytest

from gym import db, mock

PY_OK = {"passed": True, "tests": [{"name": "a", "passed": True}, {"name": "b", "passed": True}]}
SQL_BAD = {"passed": False, "tests": [{"name": "result matches reference", "passed": False}]}


def test_pick_returns_one_python_and_one_sql(steps):
    py, sql = mock.pick(steps, random.Random(0))
    assert (py.id, sql.id) == ("count-words", "top-customers")


def test_pick_fails_without_mock_exercises(steps):
    steps[1].exercises[0].mock = False
    with pytest.raises(ValueError):
        mock.pick(steps)


def test_score_formula():
    s = mock.score(PY_OK, SQL_BAD, [{"a": 5, "b": 3}, {"c": 4}], duration_s=100)
    assert s["pass_rate"] == pytest.approx(2 / 3)
    assert s["review_avg"] == pytest.approx(4.0)
    assert s["in_time"] is True
    assert s["total"] == round(100 * (0.5 * 2 / 3 + 0.4 * 4 / 5 + 0.1))


def test_score_over_time_and_no_reviews():
    s = mock.score(PY_OK, PY_OK, [{}, {}], duration_s=mock.MOCK_TIME_S + 1)
    assert s == {"pass_rate": 1.0, "review_avg": 0, "in_time": False, "total": 50}


def test_readiness_needs_three_mocks_and_uses_last_three(conn):
    for total in (10, 60, 70):
        m = db.create_mock(conn, {})
        db.update_mock(conn, m, {}, {"total": total})
        expected = None if total != 70 else round((10 + 60 + 70) / 3)
        assert mock.readiness(conn) == expected
    m = db.create_mock(conn, {})
    db.update_mock(conn, m, {}, {"total": 80})
    assert mock.readiness(conn) == 70
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_mock.py -v`
Expected: FAIL with `ImportError: cannot import name 'mock' from 'gym'`

- [ ] **Step 3: Write the implementation**

`gym/mock.py`:

```python
import json
import random

from . import db

MOCK_TIME_S = 45 * 60


def pick(steps, rng=random):
    pool = [ex for step in steps for ex in step.exercises if ex.mock]
    python = [ex for ex in pool if ex.kind == "python"]
    sql = [ex for ex in pool if ex.kind == "sql"]
    if not python or not sql:
        raise ValueError("a mock round needs at least one python and one sql exercise with mock: true")
    return rng.choice(python), rng.choice(sql)


def score(python_result, sql_result, review_scores, duration_s):
    tests = python_result["tests"] + sql_result["tests"]
    pass_rate = sum(t["passed"] for t in tests) / len(tests) if tests else 0
    values = [v for scores in review_scores for v in scores.values()]
    review_avg = sum(values) / len(values) if values else 0
    in_time = duration_s <= MOCK_TIME_S
    total = round(100 * (0.5 * pass_rate + 0.4 * review_avg / 5 + 0.1 * in_time))
    return {"pass_rate": pass_rate, "review_avg": review_avg, "in_time": in_time, "total": total}


def readiness(conn):
    rows = db.finished_mocks(conn)[:3]
    if len(rows) < 3:
        return None
    return round(sum(json.loads(r["score_json"])["total"] for r in rows) / 3)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_mock.py -v`
Expected: 5 passed

- [ ] **Step 5: Commit**

```bash
git add gym/mock.py tests/test_mock.py
git commit -m "feat: mock scoring and readiness"
```

---

### Task 9: HTTP API

**Files:**
- Create: `gym/app.py`, `web/index.html` (a one-line placeholder so static mounting works; Task 10 replaces it)
- Test: `tests/test_app.py`

**Interfaces:**
- Consumes: everything from Tasks 1 to 8, with the exact names listed there.
- Produces: `create_app(content_dir=config.CONTENT_DIR, db_path=config.DB_PATH, call=reviewer.call_gemini) -> FastAPI`, and a module-level `main()` that loads `.env` and serves on `127.0.0.1:8000`.
- Routes (all JSON):

| Method and path | Request | Response |
|---|---|---|
| `GET /api/journey` | | `{steps: [{id,title,order,passed,done,total,unlocked}], readiness, mocks: [{id,started_at,total}], due_cards: int, errors: [str]}` |
| `GET /api/step/{step_id}` | | `{id, title, lessons: [{id,title,body}], exercises: [{id,title,kind,required,status}]}` |
| `GET /api/exercise/{id}?mode=blank` | | `{id,title,kind,prompt,time_limit_s,modes,mode,code,solution,schema,status,review}` (`solution` only in retype mode, else `""`; `review` is the latest review or `null`) |
| `POST /api/run` | `{exercise_id, code}` | `{passed,tests,output,timed_out}` |
| `POST /api/submit` | `{exercise_id, code, mode, duration_s}` | run result plus `attempt_id` and `status` |
| `POST /api/review` | `{exercise_id, attempt_id?, text}` | `{review_id,status,scores,verdict,feedback}` |
| `POST /api/reviews/{id}/retry` | | same as review |
| `GET /api/cards/due` | | `[{id,front,back}]` |
| `POST /api/cards/grade` | `{card_id, correct}` | `{box, due}` |
| `POST /api/unlock` | `{step_id}` | `{ok: true}` |
| `POST /api/mock/start` | | `{mock_id, time_limit_s, python: exercise payload, sql: exercise payload}` |
| `POST /api/mock/{id}/submit` | `{python_code, sql_code, prompt_text, duration_s}` | `{python: run result, sql: run result, questions: [str]}` |
| `POST /api/mock/{id}/answers` | `{answers: [str]}` | `{score, reviews: [review], readiness}` |

- Unknown exercise, step, attempt, review or mock ids return HTTP 404. Submitting a non-coded exercise returns HTTP 400.

- [ ] **Step 1: Write the failing test**

`tests/test_app.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_app.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'gym.app'`

- [ ] **Step 3: Write the implementation**

`web/index.html` (placeholder, replaced in Task 10):

```html
<!doctype html><title>Live Coding Gym</title>
```

`gym/app.py`:

```python
import json
from dataclasses import asdict
from datetime import date

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import cards, config, db, gates, mock, reviewer, runner
from .content import load_content

CODED = ("python", "sql")


class RunBody(BaseModel):
    exercise_id: str
    code: str


class SubmitBody(RunBody):
    mode: str = "blank"
    duration_s: float = 0


class ReviewBody(BaseModel):
    exercise_id: str
    attempt_id: int | None = None
    text: str = ""


class CardBody(BaseModel):
    card_id: str
    correct: bool


class UnlockBody(BaseModel):
    step_id: str


class MockSubmit(BaseModel):
    python_code: str
    sql_code: str
    prompt_text: str
    duration_s: float


class MockAnswers(BaseModel):
    answers: list[str]


def create_app(content_dir=config.CONTENT_DIR, db_path=config.DB_PATH, call=reviewer.call_gemini):
    steps, errors = load_content(content_dir)
    conn = db.connect(db_path)
    step_by_id = {s.id: s for s in steps}
    exercises = {ex.id: ex for s in steps for ex in s.exercises}
    all_cards = [c for s in steps for c in s.cards]
    app = FastAPI()

    def need(found, what):
        if found is None:
            raise HTTPException(404, f"{what} not found")
        return found

    def get_ex(exercise_id):
        return need(exercises.get(exercise_id), "exercise")

    def status_of(ex):
        return gates.exercise_status(conn, ex, step_by_id[ex.step_id])

    def review_dict(row):
        if row is None:
            return None
        return {"review_id": row["id"], "status": row["status"], "scores": json.loads(row["scores_json"]),
                "verdict": row["verdict"], "feedback": row["feedback"]}

    def payload(ex, mode="blank"):
        coded = ex.kind in CODED
        modes = (["retype"] + (["gaps"] if ex.gaps else []) + ["blank", "timed"]) if coded else []
        code = {"retype": "", "gaps": ex.gaps}.get(mode, ex.starter)
        return {"id": ex.id, "title": ex.title, "kind": ex.kind, "prompt": ex.prompt,
                "time_limit_s": ex.time_limit_s, "modes": modes, "mode": mode, "code": code,
                "solution": ex.solution if mode == "retype" else "", "schema": ex.seed,
                "status": status_of(ex),
                "review": review_dict(db.latest_review(conn, ex.id, reviewer.REVIEW_KIND[ex.kind]))}

    def grade(ex, code):
        if ex.kind == "python":
            return runner.run_python_tests(code, ex.dir / "tests")
        return runner.check_sql(ex.seed, code, ex.solution, ex.ordered)

    def do_review(exercise_id, kind, rubric, material, attempt_id=None):
        result = reviewer.review(kind, rubric, material, call)
        review_id = db.save_review(conn, exercise_id, kind, material, result, attempt_id)
        return {"review_id": review_id, **result}

    @app.get("/api/journey")
    def journey():
        mocks = [{"id": r["id"], "started_at": r["started_at"],
                  "total": json.loads(r["score_json"])["total"]} for r in db.finished_mocks(conn)]
        return {"steps": gates.journey(conn, steps), "readiness": mock.readiness(conn), "mocks": mocks,
                "due_cards": len(cards.due(conn, all_cards, date.today())), "errors": errors}

    @app.get("/api/step/{step_id}")
    def step(step_id: str):
        s = need(step_by_id.get(step_id), "step")
        st = gates.step_status(conn, s)
        return {"id": s.id, "title": s.title, "lessons": s.lessons,
                "exercises": [{"id": ex.id, "title": ex.title, "kind": ex.kind, "required": ex.required,
                               "status": st["exercises"][ex.id]} for ex in s.exercises]}

    @app.get("/api/exercise/{exercise_id}")
    def exercise(exercise_id: str, mode: str = "blank"):
        return payload(get_ex(exercise_id), mode)

    @app.post("/api/run")
    def run(body: RunBody):
        ex = get_ex(body.exercise_id)
        if ex.kind == "sql":
            return asdict(runner.run_sql_free(ex.seed, body.code))
        return asdict(runner.run_python_free(body.code))

    @app.post("/api/submit")
    def submit(body: SubmitBody):
        ex = get_ex(body.exercise_id)
        if ex.kind not in CODED:
            raise HTTPException(400, "this exercise has no code to submit; use review")
        result = grade(ex, body.code)
        attempt_id = db.record_attempt(conn, ex.id, body.mode, body.code, result.passed,
                                       body.duration_s, result.output)
        return {**asdict(result), "attempt_id": attempt_id, "status": status_of(ex)}

    @app.post("/api/review")
    def review(body: ReviewBody):
        ex = get_ex(body.exercise_id)
        if ex.kind in CODED:
            attempt = need(db.get_attempt(conn, body.attempt_id), "attempt")
            material = {"task": ex.prompt, "code": attempt["code"],
                        "candidate explanation": body.text, "reference solution": ex.solution}
        else:
            material = {"task": ex.prompt, "answer": body.text}
        return do_review(ex.id, reviewer.REVIEW_KIND[ex.kind], ex.rubric, material, body.attempt_id)

    @app.post("/api/reviews/{review_id}/retry")
    def retry(review_id: int):
        row = need(db.get_review(conn, review_id), "review")
        ex = exercises.get(row["exercise_id"])
        rubric = ex.rubric if ex and reviewer.REVIEW_KIND[ex.kind] == row["kind"] else None
        result = reviewer.review(row["kind"], rubric, json.loads(row["material_json"]), call)
        db.update_review(conn, review_id, result)
        return {"review_id": review_id, **result}

    @app.get("/api/cards/due")
    def cards_due():
        return cards.due(conn, all_cards, date.today())

    @app.post("/api/cards/grade")
    def cards_grade(body: CardBody):
        return cards.record(conn, body.card_id, body.correct, date.today())

    @app.post("/api/unlock")
    def unlock(body: UnlockBody):
        need(step_by_id.get(body.step_id), "step")
        db.unlock(conn, body.step_id)
        return {"ok": True}

    def mock_state(mock_id):
        return json.loads(need(db.get_mock(conn, mock_id), "mock")["state_json"])

    @app.post("/api/mock/start")
    def mock_start():
        try:
            py, sql = mock.pick(steps)
        except ValueError as e:
            raise HTTPException(400, str(e))
        mock_id = db.create_mock(conn, {"python_id": py.id, "sql_id": sql.id})
        return {"mock_id": mock_id, "time_limit_s": mock.MOCK_TIME_S,
                "python": payload(py), "sql": payload(sql)}

    @app.post("/api/mock/{mock_id}/submit")
    def mock_submit(mock_id: int, body: MockSubmit):
        state = mock_state(mock_id)
        py, sql = exercises[state["python_id"]], exercises[state["sql_id"]]
        state.update(
            python_code=body.python_code, prompt_text=body.prompt_text, duration_s=body.duration_s,
            python=asdict(grade(py, body.python_code)), sql=asdict(grade(sql, body.sql_code)),
            questions=reviewer.followups(py.prompt, body.python_code, call))
        db.update_mock(conn, mock_id, state)
        return {"python": state["python"], "sql": state["sql"], "questions": state["questions"]}

    @app.post("/api/mock/{mock_id}/answers")
    def mock_answers(mock_id: int, body: MockAnswers):
        state = mock_state(mock_id)
        if "questions" not in state:
            raise HTTPException(400, "submit the code before answering follow-ups")
        py = exercises[state["python_id"]]
        transcript = "\n\n".join(f"Q: {q}\nA: {a}" for q, a in zip(state["questions"], body.answers))
        tag = f"mock:{mock_id}"  # kept apart from the exercise so mock reviews never affect step gates
        reviews = [
            do_review(tag, "code", py.rubric, {"task": py.prompt, "code": state["python_code"],
                                               "reference solution": py.solution}),
            do_review(tag, "prompt", None, {"task": py.prompt, "answer": state["prompt_text"]}),
            do_review(tag, "mock", None, {"task": py.prompt, "code": state["python_code"],
                                          "transcript": transcript}),
        ]
        score = mock.score(state["python"], state["sql"], [r["scores"] for r in reviews],
                           state["duration_s"])
        db.update_mock(conn, mock_id, state, score)
        return {"score": score, "reviews": reviews, "readiness": mock.readiness(conn)}

    app.mount("/", StaticFiles(directory=config.WEB_DIR, html=True), name="web")
    return app


def main():
    import uvicorn

    config.load_env()
    uvicorn.run(create_app(), host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_app.py -v`
Expected: 11 passed

- [ ] **Step 5: Run the whole suite**

Run: `uv run pytest`
Expected: 61 passed

- [ ] **Step 6: Commit**

```bash
git add gym/app.py web/index.html tests/test_app.py
git commit -m "feat: HTTP API"
```

---

### Task 10: Web page

**Files:**
- Create: `web/app.js`, `web/style.css`
- Modify: `web/index.html` (replace the placeholder)
- Create: `content/` by copying the fixtures (starter content, so the page has something to show)

**Interfaces:**
- Consumes: every route in the Task 9 table, with those exact request and response shapes.
- Produces: a page at `http://localhost:8000` with hash routes `#/` (journey and progress), `#/step/<id>`, `#/ex/<id>`, `#/cards`, `#/mock`.

There are no automated tests for the page. It is verified by hand in Step 5 against a checklist.

- [ ] **Step 1: Copy starter content**

```bash
cp -R tests/fixtures/content content
```

- [ ] **Step 2: Write `web/index.html`**

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Live Coding Gym</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.css">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <nav>
    <a href="#/">Journey</a>
    <a href="#/cards">Warm-up cards</a>
    <a href="#/mock">Mock round</a>
  </nav>
  <main id="main"></main>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/codemirror.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/python/python.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.16/mode/sql/sql.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.2/marked.min.js"></script>
  <script src="app.js"></script>
</body>
</html>
```

- [ ] **Step 3: Write `web/style.css`**

```css
body { font: 15px/1.5 system-ui, sans-serif; margin: 0; color: #1c1c1c; background: #fafafa; }
nav { background: #1c1c1c; padding: 10px 24px; }
nav a { color: #fff; margin-right: 20px; text-decoration: none; }
main { max-width: 960px; margin: 24px auto; padding: 0 24px; }
h1 { font-size: 22px; } h2 { font-size: 17px; margin-top: 28px; }
.row { display: flex; gap: 12px; align-items: center; padding: 10px 0; border-bottom: 1px solid #e3e3e3; }
.row .grow { flex: 1; }
.locked { opacity: 0.5; }
.ok { color: #1a7f37; } .bad { color: #c62828; } .muted { color: #777; }
button, select { font: inherit; padding: 6px 12px; cursor: pointer; }
.CodeMirror { border: 1px solid #ccc; height: 320px; font-size: 14px; }
pre { background: #f0f0f0; padding: 12px; overflow: auto; white-space: pre-wrap; }
textarea { width: 100%; min-height: 110px; font: inherit; box-sizing: border-box; }
.timer { font-variant-numeric: tabular-nums; font-weight: 600; }
.review { border-left: 4px solid #888; padding: 4px 14px; margin: 14px 0; background: #fff; }
.bar { display: flex; gap: 10px; align-items: center; margin: 12px 0; }
```

- [ ] **Step 4: Write `web/app.js`**

```javascript
const main = document.getElementById("main");
let tick = null; // the running timer, cleared on every route change

async function api(path, body) {
  const opts = body === undefined ? {} : {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
  };
  const r = await fetch("/api" + path, opts);
  if (!r.ok) throw new Error((await r.json()).detail || r.statusText);
  return r.json();
}

// h("div", {class: "row", onclick: fn}, child, "text", ...) builds a DOM node.
// Text is always inserted as text, never as HTML, except the explicit `html` attribute.
function h(tag, attrs = {}, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
    else if (k === "html") el.innerHTML = v;
    else el.setAttribute(k, v);
  }
  for (const kid of kids.flat()) if (kid !== null && kid !== undefined) el.append(kid);
  return el;
}

const md = (text) => h("div", { html: marked.parse(text) });
const fmt = (s) => `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(Math.floor(s % 60)).padStart(2, "0")}`;

function editor(parent, kind, value) {
  return CodeMirror(parent, {
    value, mode: kind === "sql" ? "text/x-sql" : "python", lineNumbers: true, indentUnit: 4,
    extraKeys: { Tab: (cm) => cm.replaceSelection("    ") },
  });
}

// Starts a visible clock and returns a function giving elapsed seconds.
function startTimer(el, limit) {
  const t0 = Date.now();
  const elapsed = () => (Date.now() - t0) / 1000;
  clearInterval(tick);
  tick = setInterval(() => {
    const s = elapsed();
    el.textContent = limit ? `${fmt(s)} / ${fmt(limit)}` : fmt(s);
    el.className = "timer" + (limit && s > limit ? " bad" : "");
  }, 500);
  return elapsed;
}

function mark(value) {
  if (value === null) return null;
  return h("span", { class: value ? "ok" : "bad" }, value ? "✓" : "✗");
}

function statusLine(st) {
  const part = (label, v) => (v === null ? null : h("span", {}, label, " ", mark(v), "  "));
  return h("span", {}, part("tests", st.tests), part("timed", st.timed), part("review", st.review));
}

function reviewBox(rev, onRetry) {
  if (!rev) return null;
  const box = h("div", { class: "review" });
  if (rev.status === "pending") {
    box.append(h("p", { class: "bad" }, rev.feedback), h("button", { onclick: onRetry }, "Retry review"));
    return box;
  }
  box.append(h("p", {}, h("strong", {}, rev.verdict)));
  for (const [criterion, score] of Object.entries(rev.scores)) {
    box.append(h("div", {}, `${score}/5  ${criterion}`));
  }
  box.append(h("p", {}, rev.feedback));
  return box;
}

function results(out, r) {
  out.textContent = "";
  for (const t of r.tests) out.append(`${t.passed ? "PASS" : "FAIL"}  ${t.name}\n`);
  out.append((r.tests.length ? "\n" : "") + r.output);
}

async function journeyView() {
  const j = await api("/journey");
  main.append(h("h1", {}, "Your journey"));
  if (j.errors.length) main.append(h("pre", { class: "bad" }, "Broken content:\n" + j.errors.join("\n")));
  main.append(h("p", {},
    j.readiness === null ? "Readiness: finish three mock rounds to get an estimate."
      : `Readiness estimate: ${j.readiness}/100 (average of your last three mock rounds).`,
    `  Cards due today: ${j.due_cards}.`));
  for (const s of j.steps) {
    const row = h("div", { class: "row" + (s.unlocked ? "" : " locked") },
      h("span", { class: "grow" }, s.unlocked
        ? h("a", { href: `#/step/${s.id}` }, `${s.order}. ${s.title}`) : `${s.order}. ${s.title}`),
      h("span", { class: s.passed ? "ok" : "muted" }, s.passed ? "passed" : `${s.done}/${s.total}`));
    if (!s.unlocked) {
      row.append(h("button", { onclick: async () => { await api("/unlock", { step_id: s.id }); route(); } },
        "Unlock anyway"));
    }
    main.append(row);
  }
  if (j.mocks.length) {
    main.append(h("h2", {}, "Mock history"));
    for (const m of j.mocks) main.append(h("div", { class: "row" }, `${m.started_at}  score ${m.total}/100`));
  }
}

async function stepView(id) {
  const s = await api(`/step/${id}`);
  main.append(h("h1", {}, s.title));
  for (const lesson of s.lessons) {
    main.append(h("details", {}, h("summary", {}, lesson.title), md(lesson.body)));
  }
  main.append(h("h2", {}, "Exercises"));
  for (const ex of s.exercises) {
    main.append(h("div", { class: "row" },
      h("a", { class: "grow", href: `#/ex/${ex.id}` }, ex.title),
      h("span", { class: "muted" }, ex.kind + (ex.required ? "" : " (optional)")),
      statusLine(ex.status)));
  }
}

async function exView(id, mode = "blank") {
  const ex = await api(`/exercise/${id}?mode=${mode}`);
  const coded = ex.modes.length > 0;
  main.append(h("h1", {}, ex.title), md(ex.prompt));
  if (ex.schema) main.append(h("details", {}, h("summary", {}, "Tables"), h("pre", {}, ex.schema)));

  const reviewSlot = h("div");
  const showReview = (rev) => reviewSlot.replaceChildren(reviewBox(rev, async () => {
    showReview(await api(`/reviews/${rev.review_id}/retry`, {}));
  }) || "");
  const text = h("textarea", { placeholder: coded
    ? "Explain your code as you would to the interviewer (sent with the review)." : "Your answer" });

  if (!coded) {
    main.append(text, h("div", { class: "bar" }, h("button", { onclick: async (e) => {
      e.target.disabled = true;
      showReview(await api("/review", { exercise_id: id, text: text.value }));
      e.target.disabled = false;
    } }, "Submit for review")), reviewSlot);
    showReview(ex.review);
    return;
  }

  const picker = h("select", { onchange: (e) => render(() => exView(id, e.target.value)) },
    ex.modes.map((m) => h("option", m === mode ? { value: m, selected: "" } : { value: m }, m)));
  const clock = h("span", { class: "timer" });
  const statusEl = h("span", {}, statusLine(ex.status));
  main.append(h("div", { class: "bar" }, "Mode ", picker, clock, statusEl));

  const holder = h("div");
  const out = h("pre");
  const reviewBtn = h("button", { disabled: "" }, "Get AI review of last passing submission");
  let cm = null, elapsed = () => 0, lastPassed = null;

  const begin = () => {
    holder.replaceChildren();
    cm = editor(holder, ex.kind, ex.code);
    elapsed = startTimer(clock, mode === "timed" ? ex.time_limit_s : 0);
  };
  if (mode === "retype") {
    holder.append(h("p", {}, "Read the solution until you can rebuild it, then hide it and type it from memory."),
      h("pre", {}, ex.solution), h("button", { onclick: begin }, "Hide and start"));
  } else begin();

  reviewBtn.addEventListener("click", async () => {
    reviewBtn.disabled = true;
    showReview(await api("/review", { exercise_id: id, attempt_id: lastPassed, text: text.value }));
    reviewBtn.disabled = false;
  });
  main.append(holder, h("div", { class: "bar" },
    h("button", { onclick: async () => cm && results(out, await api("/run", { exercise_id: id, code: cm.getValue() })) },
      "Run"),
    h("button", { onclick: async () => {
      if (!cm) return;
      const r = await api("/submit", { exercise_id: id, code: cm.getValue(), mode, duration_s: elapsed() });
      results(out, r);
      statusEl.replaceChildren(statusLine(r.status));
      if (r.passed) { lastPassed = r.attempt_id; reviewBtn.disabled = false; }
    } }, "Submit")), out, text, h("div", { class: "bar" }, reviewBtn), reviewSlot);
  showReview(ex.review);
}

async function cardsView() {
  const due = await api("/cards/due");
  main.append(h("h1", {}, "Warm-up cards"));
  if (!due.length) { main.append(h("p", {}, "Nothing due. Come back tomorrow.")); return; }
  const card = due[0];
  const back = h("pre", { hidden: "" }, card.back);
  const grade = async (correct) => { await api("/cards/grade", { card_id: card.id, correct }); route(); };
  const buttons = h("div", { class: "bar", hidden: "" },
    h("button", { onclick: () => grade(true) }, "Got it"),
    h("button", { onclick: () => grade(false) }, "Missed it"));
  main.append(h("p", { class: "muted" }, `${due.length} due`), md(card.front),
    h("textarea", { placeholder: "Type it from memory, then flip." }),
    h("div", { class: "bar" }, h("button", { onclick: () => { back.hidden = false; buttons.hidden = false; } }, "Flip")),
    back, buttons);
}

async function mockView() {
  main.append(h("h1", {}, "Mock round"),
    h("p", {}, "One Python task, one SQL task, the prompt you would give an AI assistant, then follow-up questions. 45 minutes."));
  main.append(h("button", { onclick: async () => {
    const m = await api("/mock/start", {});
    main.replaceChildren();
    const clock = h("span", { class: "timer" });
    const elapsed = startTimer(clock, m.time_limit_s);
    const pyHolder = h("div"), sqlHolder = h("div");
    const prompt = h("textarea", { placeholder: "The prompt you would give an AI assistant for the Python task. The interviewer judges this." });
    main.append(h("div", { class: "bar" }, h("strong", {}, "Mock round"), clock),
      h("h2", {}, "Python: " + m.python.title), md(m.python.prompt), pyHolder,
      h("h2", {}, "SQL: " + m.sql.title), md(m.sql.prompt), h("pre", {}, m.sql.schema), sqlHolder,
      h("h2", {}, "Your prompt for the AI assistant"), prompt);
    const py = editor(pyHolder, "python", m.python.code), sql = editor(sqlHolder, "sql", m.sql.code);
    main.append(h("div", { class: "bar" }, h("button", { onclick: async (e) => {
      e.target.disabled = true;
      const r = await api(`/mock/${m.mock_id}/submit`, {
        python_code: py.getValue(), sql_code: sql.getValue(), prompt_text: prompt.value, duration_s: elapsed() });
      clearInterval(tick);
      const pyOut = h("pre"), sqlOut = h("pre");
      results(pyOut, r.python); results(sqlOut, r.sql);
      const answers = r.questions.map(() => h("textarea"));
      main.replaceChildren(h("h1", {}, "Follow-up questions"), h("h2", {}, "Python result"), pyOut,
        h("h2", {}, "SQL result"), sqlOut,
        ...r.questions.flatMap((q, i) => [h("p", {}, h("strong", {}, q)), answers[i]]),
        h("div", { class: "bar" }, h("button", { onclick: async (ev) => {
          ev.target.disabled = true;
          const done = await api(`/mock/${m.mock_id}/answers`, { answers: answers.map((a) => a.value) });
          main.replaceChildren(h("h1", {}, `Score: ${done.score.total}/100`),
            h("p", {}, `Tests passed: ${Math.round(done.score.pass_rate * 100)}%. Review average: ${done.score.review_avg.toFixed(1)}/5. ` +
              `${done.score.in_time ? "Inside" : "Over"} the time limit. ` +
              (done.readiness === null ? "" : `Readiness estimate: ${done.readiness}/100.`)),
            ...done.reviews.map((rev) => reviewBox(rev, null)));
        } }, "Submit answers")));
    } }, "Finish coding")));
  } }, "Start"));
}

async function render(view) {
  clearInterval(tick);
  main.replaceChildren();
  try { await view(); } catch (e) { main.append(h("pre", { class: "bad" }, String(e))); }
}

function route() {
  const [, name, id] = location.hash.split("/");
  if (name === "step") render(() => stepView(id));
  else if (name === "ex") render(() => exView(id));
  else if (name === "cards") render(cardsView);
  else if (name === "mock") render(mockView);
  else render(journeyView);
}

window.addEventListener("hashchange", route);
route();
```

- [ ] **Step 5: Verify by hand in the browser**

Start the server in the background: `uv run python -m gym.app`, then open `http://localhost:8000`.

Check each line. Every one must hold before committing:

1. Journey shows two steps; step 3 is greyed with an "Unlock anyway" button; "Cards due today: 1".
2. Open step 1. The lesson expands and renders as formatted text. Two exercises are listed.
3. Open "Count words". Typing `cou` shows no autocomplete popup. Run with `print(1)` shows `1`.
4. Submit the starter code: three tests listed, two FAIL. The `tests` mark stays ✗.
5. Switch mode to `retype`: the solution is shown; "Hide and start" removes it and gives an empty editor with a running clock.
6. Switch mode to `gaps`: the editor shows the `____` blanks.
7. Switch mode to `timed`, type the solution, Submit: all PASS, `tests ✓ timed ✓`. Click "Get AI review": a real Gemini review appears with three scored criteria (this exercise's rubric) and feedback.
8. Open "Explain count_words", write two sentences, "Submit for review": a review appears.
9. Open step 3 via "Unlock anyway", open "Top customers": "Tables" shows the schema; `SELECT * FROM orders` with Run shows five rows; the reference query with Submit shows PASS.
10. "Warm-up cards": the card shows, Flip reveals the answer, "Got it" leads to "Nothing due".
11. "Mock round": Start shows both tasks and a clock; "Finish coding" shows results and three questions; "Submit answers" shows a score out of 100 and three reviews.
12. Reload the journey: mock history lists the round.

Stop the server when done. Fix anything that fails and repeat the affected checks.

- [ ] **Step 6: Commit**

```bash
git add web content
git commit -m "feat: web page and starter content"
```

---

### Task 11: Content checker and run instructions

**Files:**
- Create: `gym/check_content.py`, `README.md`
- Test: `tests/test_check_content.py`

**Interfaces:**
- Consumes: `load_content` (Task 1), `run_python_tests`, `check_sql` (Tasks 2 and 3).
- Produces: `check(content_dir) -> list[str]` returning one problem string per broken exercise (empty list means all good); command `uv run python -m gym.check_content` which prints problems and exits 1 if there are any.
- Checks: loader errors; every python and sql reference solution passes its own tests; every python `starter.py` fails its tests (a starter that already passes is a content bug).

- [ ] **Step 1: Write the failing test**

`tests/test_check_content.py`:

```python
import shutil

from gym.check_content import check
from tests.conftest import FIXTURES


def test_sample_content_is_clean():
    assert check(FIXTURES) == []


def test_wrong_reference_solution_is_reported(tmp_path):
    shutil.copytree(FIXTURES, tmp_path / "c")
    ex = tmp_path / "c" / "01-hand-python" / "exercises" / "count-words"
    (ex / "solution.py").write_text("def count_words(text):\n    return {}\n")
    problems = check(tmp_path / "c")
    assert len(problems) == 1 and "count-words" in problems[0] and "solution fails" in problems[0]


def test_starter_that_already_passes_is_reported(tmp_path):
    shutil.copytree(FIXTURES, tmp_path / "c")
    ex = tmp_path / "c" / "01-hand-python" / "exercises" / "count-words"
    shutil.copy(ex / "solution.py", ex / "starter.py")
    problems = check(tmp_path / "c")
    assert len(problems) == 1 and "starter already passes" in problems[0]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_check_content.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'gym.check_content'`

- [ ] **Step 3: Write the implementation**

`gym/check_content.py`:

```python
import sys

from . import config
from .content import load_content
from .runner import check_sql, run_python_tests


def check(content_dir):
    steps, problems = load_content(content_dir)
    problems = list(problems)
    for step in steps:
        for ex in step.exercises:
            if ex.kind == "python":
                if not run_python_tests(ex.solution, ex.dir / "tests").passed:
                    problems.append(f"{ex.id}: reference solution fails its own tests")
                if ex.starter and run_python_tests(ex.starter, ex.dir / "tests").passed:
                    problems.append(f"{ex.id}: starter already passes the tests")
            elif ex.kind == "sql":
                if not check_sql(ex.seed, ex.solution, ex.solution, ex.ordered).passed:
                    problems.append(f"{ex.id}: reference solution fails to run")
    return problems


if __name__ == "__main__":
    found = check(config.CONTENT_DIR)
    print("\n".join(found) if found else "content ok")
    sys.exit(1 if found else 0)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/test_check_content.py -v`
Expected: 3 passed

Run: `uv run python -m gym.check_content`
Expected: `content ok`

- [ ] **Step 5: Write `README.md`**

````markdown
# Live Coding Gym

Local training app for live-coding interviews on production ML systems.

## Run

```bash
uv run python -m gym.app
```

Open http://localhost:8000.

## Setup

`.env` in this folder holds `GEMINI_API_KEY` and `GEMINI_MODEL`. It is not committed.

## Adding content

Content lives in `content/<step>/`. See `docs/superpowers/specs/2026-11-14-live-coding-gym-design.md`, section 5, for the format. After adding or changing an exercise:

```bash
uv run python -m gym.check_content
```

Restart the server to load new content.

## Tests

```bash
uv run pytest
```

Progress is stored in `data/progress.db`. Delete that file to start over.
````

- [ ] **Step 6: Run the whole suite and commit**

Run: `uv run pytest`
Expected: 64 passed

```bash
git add gym/check_content.py tests/test_check_content.py README.md
git commit -m "feat: content checker and run instructions"
```

---

## After this plan

The app is complete and usable with three sample exercises. The next plan covers content: all 12 steps of the journey in the format the app loads, and migration of the 55 drills, lessons and mocks from `live-coding-gym.html`. It is written after this plan is executed, so that content is authored and checked (`python -m gym.check_content`) against the real app.
