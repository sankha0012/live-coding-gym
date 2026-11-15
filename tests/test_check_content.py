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
    files = {"exercise.yaml": "title: T\nkind: tests\n", "prompt.md": "p", "hint.md": "h", "say.md": "s", "guide.md": "g",
             "starter.py": "from solution import f\n",
             "solution.py": "from solution import f\n\ndef test_f():\n    assert f() == 1\n",
             "impl_good.py": "def f(): return 1\n", "impl_bad_1.py": "def f(): return 2\n"}
    for name, text in files.items():
        (ex / name).write_text(text)
    assert check(tmp_path / "c") == []
    (ex / "solution.py").write_text("from solution import f\n\ndef test_f():\n    assert f() in (1, 2)\n")
    assert any("do not catch every bug" in p for p in check(tmp_path / "c"))


def test_sql_wrong_and_alt_queries_are_checked(tmp_path):
    step = tmp_path / "c" / "01-s"
    ex = step / "exercises" / "q1"
    (ex / "wrong").mkdir(parents=True)
    (ex / "alt").mkdir()
    (step / "step.yaml").write_text("title: S\norder: 1\n")
    files = {"exercise.yaml": "title: Q\nkind: sql\n", "prompt.md": "p", "hint.md": "h", "say.md": "s", "guide.md": "g",
             "seed.sql": "CREATE TABLE t (x INTEGER);\nINSERT INTO t VALUES (1), (3);\n",
             "solution.sql": "SELECT MAX(x) FROM t;", "starter.sql": "SELECT",
             "wrong/min.sql": "SELECT MIN(x) FROM t;", "alt/order.sql": "SELECT x FROM t ORDER BY x DESC LIMIT 1;"}
    for name, text in files.items():
        (ex / name).write_text(text)
    assert check(tmp_path / "c") == []
    (ex / "wrong" / "same.sql").write_text("SELECT x FROM t ORDER BY x DESC LIMIT 1;")
    (ex / "alt" / "bad.sql").write_text("SELECT MIN(x) FROM t;")
    problems = check(tmp_path / "c")
    assert any("wrong query same gives the reference result" in p for p in problems)
    assert any("alternative query bad does not match" in p for p in problems) and len(problems) == 2


def test_curriculum_rules(steps):
    from gym.check_content import check_curriculum
    problems = check_curriculum(steps)
    assert any("missing serves" in p for p in problems) and any("mock task needs docs.md" in p for p in problems)
    ex = steps[0].exercises[0]
    ex.serves, ex.docs, ex.change = ["C2"], "docs", "change"
    assert not [p for p in check_curriculum(steps) if p.startswith(ex.id)]
