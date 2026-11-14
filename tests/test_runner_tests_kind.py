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
