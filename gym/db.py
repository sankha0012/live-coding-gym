import json
import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY, exercise_id TEXT, mode TEXT, code TEXT,
    passed INTEGER, duration_s REAL, output TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY, exercise_id TEXT, attempt_id INTEGER, kind TEXT,
    material_json TEXT, status TEXT, scores_json TEXT, verdict TEXT, feedback TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS cards (card_id TEXT PRIMARY KEY, box INTEGER, due TEXT);
CREATE TABLE IF NOT EXISTS unlocks (step_id TEXT PRIMARY KEY);
CREATE TABLE IF NOT EXISTS mocks (
    id INTEGER PRIMARY KEY, started_at TEXT DEFAULT CURRENT_TIMESTAMP,
    state_json TEXT, score_json TEXT);
"""


def connect(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    # ponytail: one shared connection across FastAPI's worker threads. Fine for
    # a single local user; use a connection per request if writes ever overlap.
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn


def _insert(conn, sql, params):
    cur = conn.execute(sql, params)
    conn.commit()
    return cur.lastrowid


def record_attempt(conn, exercise_id, mode, code, passed, duration_s, output):
    return _insert(
        conn,
        "INSERT INTO attempts (exercise_id, mode, code, passed, duration_s, output) VALUES (?,?,?,?,?,?)",
        (exercise_id, mode, code, int(passed), duration_s, output),
    )


def get_attempt(conn, attempt_id):
    return conn.execute("SELECT * FROM attempts WHERE id = ?", (attempt_id,)).fetchone()


def passed_attempts(conn, exercise_id):
    return conn.execute(
        "SELECT * FROM attempts WHERE exercise_id = ? AND passed = 1", (exercise_id,)
    ).fetchall()


def save_review(conn, exercise_id, kind, material, result, attempt_id=None):
    return _insert(
        conn,
        "INSERT INTO reviews (exercise_id, attempt_id, kind, material_json, status, scores_json, verdict, feedback)"
        " VALUES (?,?,?,?,?,?,?,?)",
        (exercise_id, attempt_id, kind, json.dumps(material), result["status"],
         json.dumps(result["scores"]), result["verdict"], result["feedback"]),
    )


def update_review(conn, review_id, result):
    conn.execute(
        "UPDATE reviews SET status = ?, scores_json = ?, verdict = ?, feedback = ? WHERE id = ?",
        (result["status"], json.dumps(result["scores"]), result["verdict"], result["feedback"], review_id),
    )
    conn.commit()


def get_review(conn, review_id):
    return conn.execute("SELECT * FROM reviews WHERE id = ?", (review_id,)).fetchone()


def latest_review(conn, exercise_id, kind):
    return conn.execute(
        "SELECT * FROM reviews WHERE exercise_id = ? AND kind = ? ORDER BY id DESC LIMIT 1",
        (exercise_id, kind),
    ).fetchone()


def unlock(conn, step_id):
    conn.execute("INSERT OR IGNORE INTO unlocks (step_id) VALUES (?)", (step_id,))
    conn.commit()


def unlocked(conn):
    return {r["step_id"] for r in conn.execute("SELECT step_id FROM unlocks")}


def create_mock(conn, state):
    return _insert(conn, "INSERT INTO mocks (state_json) VALUES (?)", (json.dumps(state),))


def get_mock(conn, mock_id):
    return conn.execute("SELECT * FROM mocks WHERE id = ?", (mock_id,)).fetchone()


def update_mock(conn, mock_id, state, score=None):
    conn.execute(
        "UPDATE mocks SET state_json = ?, score_json = ? WHERE id = ?",
        (json.dumps(state), json.dumps(score) if score is not None else None, mock_id),
    )
    conn.commit()


def finished_mocks(conn):
    return conn.execute(
        "SELECT id, started_at, score_json FROM mocks WHERE score_json IS NOT NULL ORDER BY id DESC"
    ).fetchall()
