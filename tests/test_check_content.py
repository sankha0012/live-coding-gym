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
