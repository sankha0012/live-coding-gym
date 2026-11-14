import json

from gym import db

DONE = {"status": "done", "scores": {"a": 4}, "verdict": "ok", "feedback": "fine"}
PENDING = {"status": "pending", "scores": {}, "verdict": "", "feedback": "down"}


def test_attempts_round_trip(conn):
    a = db.record_attempt(conn, "ex", "blank", "code", True, 12.5, "out")
    db.record_attempt(conn, "ex", "blank", "bad", False, 3, "out")
    assert db.get_attempt(conn, a)["code"] == "code"
    rows = db.passed_attempts(conn, "ex")
    assert [(r["mode"], r["duration_s"]) for r in rows] == [("blank", 12.5)]


def test_latest_review_is_per_kind(conn):
    db.save_review(conn, "ex", "code", {"code": "x"}, DONE)
    rid = db.save_review(conn, "ex", "code", {"code": "y"}, PENDING)
    db.save_review(conn, "ex", "explain", {"answer": "z"}, DONE)
    latest = db.latest_review(conn, "ex", "code")
    assert latest["id"] == rid and latest["status"] == "pending"
    assert json.loads(latest["material_json"]) == {"code": "y"}


def test_update_review(conn):
    rid = db.save_review(conn, "ex", "code", {}, PENDING)
    db.update_review(conn, rid, DONE)
    row = db.get_review(conn, rid)
    assert row["status"] == "done" and json.loads(row["scores_json"]) == {"a": 4}


def test_unlocks(conn):
    db.unlock(conn, "03-hand-sql")
    db.unlock(conn, "03-hand-sql")
    assert db.unlocked(conn) == {"03-hand-sql"}


def test_mocks(conn):
    m = db.create_mock(conn, {"python_id": "a"})
    assert db.finished_mocks(conn) == []
    db.update_mock(conn, m, {"python_id": "a", "done": True}, {"total": 70})
    rows = db.finished_mocks(conn)
    assert json.loads(rows[0]["score_json"]) == {"total": 70}
    assert json.loads(db.get_mock(conn, m)["state_json"])["done"] is True
