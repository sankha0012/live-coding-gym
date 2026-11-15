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
    assert by_id["py-city"].say.strip() == "It is a sum." and by_id["py-city"].hint.strip() == "Use sum."
    py_step = next(s for s in steps if s.id == "01-hand-python")
    assert py_step.lessons[0]["title"] == "Python core" and "<p>Hello</p>" in py_step.lessons[0]["body"]
    assert py_step.cards[0]["id"] == "python-count"
    assert [p for p in check(tmp_path) if "guide.md" not in p] == []  # guides are written after migration


def test_migrate_does_not_overwrite_existing_work(tmp_path):
    (tmp_path / "_shared").mkdir()
    (tmp_path / "_shared" / "delivery.sql").write_text("CREATE TABLE restaurants (restaurant_id INTEGER, city TEXT);\n")
    migrate(OLD, tmp_path)
    solution = tmp_path / "01-hand-python" / "exercises" / "py-city" / "solution.py"
    solution.write_text("def total(xs):\n    return 6 if xs else 0\n")
    migrate(OLD, tmp_path)
    assert "return 6" in solution.read_text()
