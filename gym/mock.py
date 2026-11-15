import json
import random

from . import db

MOCK_TIME_S = 35 * 60  # coding time; the follow-ups come after


def pick(steps, rng=random):
    """Up to two Python tasks flagged mock: true."""
    python = [ex for step in steps for ex in step.exercises if ex.mock and ex.kind == "python"]
    if not python:
        raise ValueError("a mock round needs at least one python exercise with mock: true")
    return rng.sample(python, min(2, len(python)))


def ratio(hits, total):
    """Share of good behaviours; no data counts as full credit."""
    return hits / total if total else 1.0


def score(results, review_scores, duration_s, asks=1.0, ran=1.0, lines=1.0):
    """results: one test result per task. asks, ran, lines: 0..1 shares (small asks, ran before accepting, line explanations)."""
    tests = [t for r in results for t in r["tests"]]
    pass_rate = sum(t["passed"] for t in tests) / len(tests) if tests else 0
    values = [v for scores in review_scores for v in scores.values()]
    review_avg = sum(values) / len(values) if values else 0
    in_time = duration_s <= MOCK_TIME_S
    total = round(100 * (0.35 * pass_rate + 0.25 * review_avg / 5 + 0.10 * in_time + 0.10 * asks + 0.10 * ran + 0.10 * lines))
    return {"pass_rate": pass_rate, "review_avg": review_avg, "in_time": in_time, "asks": asks, "ran": ran,
            "lines": lines, "total": total}


def readiness(conn):
    rows = db.finished_mocks(conn)[:3]
    if len(rows) < 3:
        return None
    return round(sum(json.loads(r["score_json"])["total"] for r in rows) / 3)
