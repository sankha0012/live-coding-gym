import random

import pytest

from gym import db, mock

PY_OK = {"passed": True, "tests": [{"name": "a", "passed": True}, {"name": "b", "passed": True}]}
PY_BAD = {"passed": False, "tests": [{"name": "c", "passed": False}]}


def test_pick_returns_the_python_mock_tasks(steps):
    assert [ex.id for ex in mock.pick(steps, random.Random(0))] == ["count-words"]


def test_pick_fails_without_mock_exercises(steps):
    for s in steps:
        for ex in s.exercises:
            ex.mock = False
    with pytest.raises(ValueError):
        mock.pick(steps)


def test_score_formula():
    s = mock.score([PY_OK, PY_BAD], [{"a": 5, "b": 3}, {"c": 4}], duration_s=100, asks=0.5, ran=0.0, lines=1.0)
    assert s["pass_rate"] == pytest.approx(2 / 3)
    assert s["review_avg"] == pytest.approx(4.0)
    assert s["total"] == round(100 * (0.35 * 2 / 3 + 0.25 * 4 / 5 + 0.10 + 0.10 * 0.5 + 0 + 0.10))


def test_score_missing_behaviour_data_counts_as_full_credit_and_over_time_loses_points():
    s = mock.score([PY_OK], [{}], duration_s=mock.MOCK_TIME_S + 1)
    assert s["in_time"] is False and s["total"] == round(100 * (0.35 + 0 + 0 + 0.3))
    assert mock.ratio(0, 0) == 1.0 and mock.ratio(1, 4) == 0.25


def test_readiness_needs_three_mocks_and_uses_last_three(conn):
    for total in (10, 60, 70):
        m = db.create_mock(conn, {})
        db.update_mock(conn, m, {}, {"total": total})
        expected = None if total != 70 else round((10 + 60 + 70) / 3)
        assert mock.readiness(conn) == expected
    m = db.create_mock(conn, {})
    db.update_mock(conn, m, {}, {"total": 80})
    assert mock.readiness(conn) == 70
