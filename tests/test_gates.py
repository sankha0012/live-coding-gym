from gym import db, gates


def good(score=4):
    return {"status": "done", "scores": {"a": score, "b": 5}, "verdict": "v", "feedback": "f"}


def test_fresh_journey_only_first_step_unlocked(conn, steps):
    j = gates.journey(conn, steps)
    assert [(s["id"], s["unlocked"], s["passed"]) for s in j] == [
        ("01-hand-python", True, False), ("03-hand-sql", False, False)]
    assert j[0]["total"] == 2 and j[0]["done"] == 0


def test_passes_in_other_modes_do_not_count(conn, steps):
    step, ex = steps[0], steps[0].exercises[0]
    db.record_attempt(conn, ex.id, "retype", "c", True, 10, "")
    db.record_attempt(conn, ex.id, "change", "c", True, 10, "")
    assert gates.exercise_status(conn, ex, step)["tests"] is False


def test_review_must_be_done_and_meet_min_score(conn, steps):
    step, ex = steps[0], steps[0].exercises[0]
    assert gates.exercise_status(conn, ex, step)["review"] is False
    db.save_review(conn, ex.id, "code", {}, good(score=3))
    assert gates.exercise_status(conn, ex, step)["review"] is False
    db.save_review(conn, ex.id, "code", {}, good(score=4))
    assert gates.exercise_status(conn, ex, step)["review"] is True
    db.save_review(conn, ex.id, "code", {}, {"status": "pending", "scores": {}, "verdict": "", "feedback": ""})
    assert gates.exercise_status(conn, ex, step)["review"] is False


def test_uncoded_exercise_needs_only_review(conn, steps):
    step, ex = steps[0], steps[0].exercises[1]
    st = gates.exercise_status(conn, ex, step)
    assert st["tests"] is None and st["review"] is False
    db.save_review(conn, ex.id, "explain", {}, good())
    assert gates.exercise_status(conn, ex, step)["done"] is True


def test_step_passes_and_unlocks_next(conn, steps):
    code_ex, explain_ex = steps[0].exercises
    db.record_attempt(conn, code_ex.id, "blank", "c", True, 100, "")
    db.save_review(conn, code_ex.id, "code", {}, good())
    db.save_review(conn, explain_ex.id, "explain", {}, good())
    j = gates.journey(conn, steps)
    assert j[0]["passed"] is True and j[0]["done"] == 2
    assert j[1]["unlocked"] is True


def test_sql_step_without_timed_or_review(conn, steps):
    step, ex = steps[1], steps[1].exercises[0]
    db.record_attempt(conn, ex.id, "blank", "q", True, 5000, "")
    st = gates.exercise_status(conn, ex, step)
    assert st == {"tests": True, "review": None, "explain": None, "control": None, "bug": None,
                  "prompts": None, "fix": None, "done": True, "assisted": False}
    assert gates.step_status(conn, step)["passed"] is True


def test_manual_unlock(conn, steps):
    db.unlock(conn, "03-hand-sql")
    assert gates.journey(conn, steps)[1]["unlocked"] is True


def test_step_with_no_required_exercises_never_passes(conn, steps):
    step = steps[1]
    step.exercises[0].required = False
    assert gates.step_status(conn, step)["passed"] is False


def test_step_passes_at_the_pass_ratio(conn, steps):
    step = steps[0]
    step.pass_ratio = 0.5
    code_ex, explain_ex = step.exercises
    db.record_attempt(conn, code_ex.id, "blank", "c", True, 100, "")
    db.save_review(conn, code_ex.id, "code", {}, good())
    st = gates.step_status(conn, step)
    assert st["done"] == 1 and st["total"] == 2 and st["passed"] is True
    step.pass_ratio = 1.0
    assert gates.step_status(conn, step)["passed"] is False


def test_journey_reports_needed_count(conn, steps):
    steps[0].pass_ratio = 0.7
    j = gates.journey(conn, steps)[0]
    assert j["needed"] == 2 and j["pass_ratio"] == 0.7  # ceil(0.7 * 2)
