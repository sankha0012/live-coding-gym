from gym import runner, whatif

CODE = '''def total(xs):
    # sum the items
    result = 0
    for x in xs:
        if x > 0:
            result += x
    return result
'''
TESTS = "from solution import total\n\ndef test_a():\n    assert total([1, -2, 3]) == 4\n\ndef test_b():\n    assert total([0]) == 0\n"


def test_candidates_change_one_line_and_skip_comments_and_strings():
    ms = whatif.candidates(CODE)
    assert ms and all(m["code"].count("\n") == CODE.count("\n") for m in ms)
    assert not any(m["line"] == 2 for m in ms)  # the comment line
    assert any(m["old"] == "if x > 0:" and m["new"] == "if x >= 0:" for m in ms)
    assert any(m["new"] == "pass" and m["old"] == "result += x" for m in ms)
    assert [m["new"] for m in whatif.candidates('print("a < b")\n')] == ["pass"]  # the string is left alone
    assert any(m["new"] == "result = 1" for m in ms)  # numbers are bumped


def test_pick_runs_the_changes_and_mixes_outcomes(tmp_path):
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_hidden.py").write_text(TESTS)
    judge = lambda code: "pass" if runner.run_python_tests(code, tmp_path / "tests").passed else "fail"
    qs = whatif.pick(CODE, 7, judge, want=3)
    assert 2 <= len(qs) <= 3 and {q["answer"] for q in qs} == {"pass", "fail"}
    assert all(q["change"].startswith("Line ") for q in qs)
    assert qs == whatif.pick(CODE, 7, judge, want=3)  # the same seed gives the same questions
    by_change = {q["change"]: q["answer"] for q in whatif.pick(CODE, 3, judge, want=6)}
    assert by_change.get("Line 5: `if x > 0:` becomes `if x >= 0:`.", "pass") == "pass"  # adding 0 changes nothing


def test_sql_changes():
    sql = "SELECT city, COUNT(*) AS n\nFROM orders\nWHERE amount > 10\nORDER BY n DESC\nLIMIT 3;"
    news = {m["new"] for m in whatif.candidates(sql, sql=True)}
    assert {"WHERE amount >= 10", "ORDER BY n ASC", "LIMIT 4;"} <= news
    assert not any(n == "pass" for n in news)
