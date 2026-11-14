import json
import random

from . import db

MOCK_TIME_S = 45 * 60


def pick(steps, rng=random):
    pool = [ex for step in steps for ex in step.exercises if ex.mock]
    python = [ex for ex in pool if ex.kind == "python"]
    sql = [ex for ex in pool if ex.kind == "sql"]
    if not python or not sql:
        raise ValueError("a mock round needs at least one python and one sql exercise with mock: true")
    return rng.choice(python), rng.choice(sql)


def score(python_result, sql_result, review_scores, duration_s):
    tests = python_result["tests"] + sql_result["tests"]
    pass_rate = sum(t["passed"] for t in tests) / len(tests) if tests else 0
    values = [v for scores in review_scores for v in scores.values()]
    review_avg = sum(values) / len(values) if values else 0
    in_time = duration_s <= MOCK_TIME_S
    total = round(100 * (0.5 * pass_rate + 0.4 * review_avg / 5 + 0.1 * in_time))
    return {"pass_rate": pass_rate, "review_avg": review_avg, "in_time": in_time, "total": total}


def readiness(conn):
    rows = db.finished_mocks(conn)[:3]
    if len(rows) < 3:
        return None
    return round(sum(json.loads(r["score_json"])["total"] for r in rows) / 3)
