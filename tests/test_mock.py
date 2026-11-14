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
