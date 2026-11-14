from gym.content import load_content


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
