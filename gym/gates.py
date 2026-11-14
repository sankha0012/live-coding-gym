import json
import math

from . import db
from .reviewer import REVIEW_KIND

TESTED = ("python", "sql", "quiz", "tests")


def _review_ok(conn, ex, min_score):
    row = db.latest_review(conn, ex.id, REVIEW_KIND[ex.kind])
    if row is None or row["status"] != "done":
        return False
    scores = json.loads(row["scores_json"])
    return bool(scores) and min(scores.values()) >= min_score


def exercise_status(conn, ex, step):
    coded = ex.kind in TESTED
    rows = db.passed_attempts(conn, ex.id) if coded else []
    status = {"tests": None, "timed": None, "review": None}
    if coded:
        status["tests"] = any(r["mode"] in ("blank", "timed") for r in rows)
        if step.timed_required:
            status["timed"] = any(
                r["mode"] == "timed" and r["duration_s"] <= ex.time_limit_s for r in rows)
    if ex.review or not coded:
        status["review"] = _review_ok(conn, ex, step.min_score)
    status["done"] = all(v for v in status.values() if v is not None)
    return status


def step_status(conn, step):
    exercises = {ex.id: exercise_status(conn, ex, step) for ex in step.exercises}
    required = [ex.id for ex in step.exercises if ex.required]
    done = sum(exercises[i]["done"] for i in required)
    return {"passed": bool(required) and done / len(required) >= step.pass_ratio,
            "done": done, "total": len(required), "exercises": exercises}


def journey(conn, steps):
    manual = db.unlocked(conn)
    out, previous_passed = [], True
    for step in steps:
        st = step_status(conn, step)
        out.append({"id": step.id, "title": step.title, "order": step.order,
                    "passed": st["passed"], "done": st["done"], "total": st["total"],
                    "pass_ratio": step.pass_ratio, "needed": math.ceil(step.pass_ratio * st["total"]),
                    "unlocked": previous_passed or step.id in manual})
        previous_passed = st["passed"]
    return out
