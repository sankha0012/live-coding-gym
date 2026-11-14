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
