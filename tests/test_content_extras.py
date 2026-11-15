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


def test_exercises_sort_by_order_then_id(tmp_path):
    step = tmp_path / "01-s"
    (step / "exercises").mkdir(parents=True)
    (step / "step.yaml").write_text("title: S\norder: 1\n")
    for name, order in (("a-late", 60), ("b-first", 10), ("c-default", None)):
        d = step / "exercises" / name
        d.mkdir()
        (d / "exercise.yaml").write_text(f"title: {name}\nkind: open\n" + (f"order: {order}\n" if order else ""))
        (d / "prompt.md").write_text("p")
    steps, _ = load_content(tmp_path)
    assert [e.id for e in steps[0].exercises] == ["b-first", "c-default", "a-late"]


def test_sql_extra_seed_wrong_and_alt_queries(tmp_path):
    (tmp_path / "_shared").mkdir()
    (tmp_path / "_shared" / "s.sql").write_text("CREATE TABLE t (x INTEGER);\nINSERT INTO t VALUES (1);\n")
    build(tmp_path, "sql", {"solution.sql": "SELECT MAX(x) FROM t;", "seed_extra.sql": "INSERT INTO t VALUES (5);\n",
                            "wrong/first.sql": "SELECT x FROM t LIMIT 1;", "alt/order.sql": "SELECT x FROM t ORDER BY x DESC LIMIT 1;"},
          meta="seed_file: ../../../_shared/s.sql\n")
    ex, errors = load_one(tmp_path)
    assert errors == [] and "VALUES (5)" in ex.seed and "VALUES (1)" in ex.seed
    assert list(ex.wrong) == ["first"] and list(ex.alt) == ["order"]
