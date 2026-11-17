import json
import math

from . import db
from .reviewer import REVIEW_KIND

TESTED = ("python", "sql", "quiz", "tests", "read", "triage")
PASS_MODES = ("blank", "challenge")


def _review_ok(conn, exercise_id, kind, min_score):
    row = db.latest_review(conn, exercise_id, kind)
    if row is None or row["status"] != "done":
        return False
    scores = json.loads(row["scores_json"])
    return bool(scores) and min(scores.values()) >= min_score


def _whatif_ok(conn, exercise_id):
    row = db.get_whatif(conn, exercise_id)
    return bool(row and row["ok"])


def exercise_status(conn, ex, step):
    coded = ex.kind in TESTED
    rows = db.passed_attempts(conn, ex.id) if coded else []
    code_kind = ex.kind in ("python", "sql", "tests")
    assisted = code_kind and ex.assistant != "off" and db.is_assisted(conn, ex.id)
    status = {"tests": None, "review": None, "explain": None, "control": None, "bug": None, "prompts": None, "fix": None}
    if ex.kind == "read":  # the What if rounds are this kind's check; levels 2 and 3 add a written answer, level 3 a fix
        status["tests"] = _whatif_ok(conn, ex.id)
        if ex.level >= 2:
            status["review"] = _review_ok(conn, ex.id, REVIEW_KIND["read"], step.min_score)
        if ex.level >= 3:
            status["fix"] = any(r["mode"] == "fix" for r in rows)
    else:
        if coded:
            status["tests"] = any(r["mode"] in PASS_MODES for r in rows)
        if not coded:  # answer-writing kinds are judged by the interviewer
            status["review"] = _review_ok(conn, ex.id, REVIEW_KIND[ex.kind], step.min_score)
    level = ex.control_level
    if level:  # core build: prove you understand the passing code
        control = db.get_control(conn, ex.id)
        a, b = bool(control and control["a_ok"]), bool(control and control["b_ok"])
        w = _whatif_ok(conn, ex.id)
        status["control"] = {1: w, 2: w and b, 3: a and b}[level]
    elif assisted:  # the assistant wrote code here: it only counts once the learner shows they understand it
        status["explain"] = _whatif_ok(conn, ex.id)
    if ex.name_bug:
        status["bug"] = _review_ok(conn, ex.id, "bug", step.min_score)
    if ex.grade_prompts:
        status["prompts"] = _review_ok(conn, f"chat:{ex.id}", "prompt", step.min_score)
    status["done"] = all(v for v in status.values() if v is not None)
    status["assisted"] = assisted
    return status


def step_status(conn, step):
    exercises = {ex.id: exercise_status(conn, ex, step) for ex in step.exercises}
    required = [ex.id for ex in step.exercises if ex.required]
    done = sum(exercises[i]["done"] for i in required)
    return {"passed": bool(required) and done / len(required) >= step.pass_ratio,
            "done": done, "total": len(required), "exercises": exercises}


def journey(conn, steps, open_all=False):
    """One row per step. Steps unlock in order; an optional step is always open and never blocks the next one."""
    manual = db.unlocked(conn)
    out, previous_passed = [], True
    for step in steps:
        st = step_status(conn, step)
        row = {"id": step.id, "title": step.title, "order": step.order, "optional": step.optional,
               "passed": st["passed"], "done": st["done"], "total": st["total"],
               "pass_ratio": step.pass_ratio, "needed": math.ceil(step.pass_ratio * st["total"]),
               "unlocked": open_all or step.optional or previous_passed or step.id in manual}
        out.append(row)
        if not step.optional:
            previous_passed = st["passed"]
    return out
