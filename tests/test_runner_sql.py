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
