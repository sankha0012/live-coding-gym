import json
from dataclasses import asdict
from datetime import date

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import cards, config, db, gates, mock, reviewer, runner
from .content import load_content

CODED = ("python", "sql")


class RunBody(BaseModel):
    exercise_id: str
    code: str


class SubmitBody(RunBody):
    mode: str = "blank"
    duration_s: float = 0


class ReviewBody(BaseModel):
    exercise_id: str
    attempt_id: int | None = None
    text: str = ""


class CardBody(BaseModel):
    card_id: str
    correct: bool


class UnlockBody(BaseModel):
    step_id: str


class MockSubmit(BaseModel):
    python_code: str
    sql_code: str
    prompt_text: str
    duration_s: float


class MockAnswers(BaseModel):
    answers: list[str]


def create_app(content_dir=config.CONTENT_DIR, db_path=config.DB_PATH, call=reviewer.call_gemini):
    steps, errors = load_content(content_dir)
    conn = db.connect(db_path)
    step_by_id = {s.id: s for s in steps}
    exercises = {ex.id: ex for s in steps for ex in s.exercises}
    all_cards = [c for s in steps for c in s.cards]
    app = FastAPI()

    def need(found, what):
        if found is None:
            raise HTTPException(404, f"{what} not found")
        return found

    def get_ex(exercise_id):
        return need(exercises.get(exercise_id), "exercise")

    def status_of(ex):
        return gates.exercise_status(conn, ex, step_by_id[ex.step_id])

    def review_dict(row):
        if row is None:
            return None
        return {"review_id": row["id"], "status": row["status"], "scores": json.loads(row["scores_json"]),
                "verdict": row["verdict"], "feedback": row["feedback"]}

    def payload(ex, mode="blank"):
        coded = ex.kind in CODED
        modes = (["retype"] + (["gaps"] if ex.gaps else []) + ["blank", "timed"]) if coded else []
        code = {"retype": "", "gaps": ex.gaps}.get(mode, ex.starter)
        return {"id": ex.id, "title": ex.title, "kind": ex.kind, "prompt": ex.prompt,
                "time_limit_s": ex.time_limit_s, "modes": modes, "mode": mode, "code": code,
                "solution": ex.solution if mode == "retype" else "", "schema": ex.seed,
                "status": status_of(ex),
                "review": review_dict(db.latest_review(conn, ex.id, reviewer.REVIEW_KIND[ex.kind]))}

    def grade(ex, code):
        if ex.kind == "python":
            return runner.run_python_tests(code, ex.dir / "tests")
        return runner.check_sql(ex.seed, code, ex.solution, ex.ordered)

    def do_review(exercise_id, kind, rubric, material, attempt_id=None):
        result = reviewer.review(kind, rubric, material, call)
        review_id = db.save_review(conn, exercise_id, kind, material, result, attempt_id)
        return {"review_id": review_id, **result}

    @app.get("/api/journey")
    def journey():
        mocks = [{"id": r["id"], "started_at": r["started_at"],
                  "total": json.loads(r["score_json"])["total"]} for r in db.finished_mocks(conn)]
        return {"steps": gates.journey(conn, steps), "readiness": mock.readiness(conn), "mocks": mocks,
                "due_cards": len(cards.due(conn, all_cards, date.today())), "errors": errors}

    @app.get("/api/step/{step_id}")
    def step(step_id: str):
        s = need(step_by_id.get(step_id), "step")
        st = gates.step_status(conn, s)
        return {"id": s.id, "title": s.title, "lessons": s.lessons,
                "exercises": [{"id": ex.id, "title": ex.title, "kind": ex.kind, "required": ex.required,
                               "status": st["exercises"][ex.id]} for ex in s.exercises]}

    @app.get("/api/exercise/{exercise_id}")
    def exercise(exercise_id: str, mode: str = "blank"):
        return payload(get_ex(exercise_id), mode)

    @app.post("/api/run")
    def run(body: RunBody):
        ex = get_ex(body.exercise_id)
        if ex.kind == "sql":
            return asdict(runner.run_sql_free(ex.seed, body.code))
        return asdict(runner.run_python_free(body.code))

    @app.post("/api/submit")
    def submit(body: SubmitBody):
        ex = get_ex(body.exercise_id)
        if ex.kind not in CODED:
            raise HTTPException(400, "this exercise has no code to submit; use review")
        result = grade(ex, body.code)
        attempt_id = db.record_attempt(conn, ex.id, body.mode, body.code, result.passed,
                                       body.duration_s, result.output)
        return {**asdict(result), "attempt_id": attempt_id, "status": status_of(ex)}

    @app.post("/api/review")
    def review(body: ReviewBody):
        ex = get_ex(body.exercise_id)
        if ex.kind in CODED:
            attempt = need(db.get_attempt(conn, body.attempt_id), "attempt")
            material = {"task": ex.prompt, "code": attempt["code"],
                        "candidate explanation": body.text, "reference solution": ex.solution}
        else:
            material = {"task": ex.prompt, "answer": body.text}
        return do_review(ex.id, reviewer.REVIEW_KIND[ex.kind], ex.rubric, material, body.attempt_id)

    @app.post("/api/reviews/{review_id}/retry")
    def retry(review_id: int):
        row = need(db.get_review(conn, review_id), "review")
        ex = exercises.get(row["exercise_id"])
        rubric = ex.rubric if ex and reviewer.REVIEW_KIND[ex.kind] == row["kind"] else None
        result = reviewer.review(row["kind"], rubric, json.loads(row["material_json"]), call)
        db.update_review(conn, review_id, result)
        return {"review_id": review_id, **result}

    @app.get("/api/cards/due")
    def cards_due():
        return cards.due(conn, all_cards, date.today())

    @app.post("/api/cards/grade")
    def cards_grade(body: CardBody):
        return cards.record(conn, body.card_id, body.correct, date.today())

    @app.post("/api/unlock")
    def unlock(body: UnlockBody):
        need(step_by_id.get(body.step_id), "step")
        db.unlock(conn, body.step_id)
        return {"ok": True}

    def mock_state(mock_id):
        return json.loads(need(db.get_mock(conn, mock_id), "mock")["state_json"])

    @app.post("/api/mock/start")
    def mock_start():
        try:
            py, sql = mock.pick(steps)
        except ValueError as e:
            raise HTTPException(400, str(e))
        mock_id = db.create_mock(conn, {"python_id": py.id, "sql_id": sql.id})
        return {"mock_id": mock_id, "time_limit_s": mock.MOCK_TIME_S,
                "python": payload(py), "sql": payload(sql)}

    @app.post("/api/mock/{mock_id}/submit")
    def mock_submit(mock_id: int, body: MockSubmit):
        state = mock_state(mock_id)
        py, sql = exercises[state["python_id"]], exercises[state["sql_id"]]
        state.update(
            python_code=body.python_code, prompt_text=body.prompt_text, duration_s=body.duration_s,
            python=asdict(grade(py, body.python_code)), sql=asdict(grade(sql, body.sql_code)),
            questions=reviewer.followups(py.prompt, body.python_code, call))
        db.update_mock(conn, mock_id, state)
        return {"python": state["python"], "sql": state["sql"], "questions": state["questions"]}

    @app.post("/api/mock/{mock_id}/answers")
    def mock_answers(mock_id: int, body: MockAnswers):
        state = mock_state(mock_id)
        if "questions" not in state:
            raise HTTPException(400, "submit the code before answering follow-ups")
        py = exercises[state["python_id"]]
        transcript = "\n\n".join(f"Q: {q}\nA: {a}" for q, a in zip(state["questions"], body.answers))
        tag = f"mock:{mock_id}"  # kept apart from the exercise so mock reviews never affect step gates
        reviews = [
            do_review(tag, "code", py.rubric, {"task": py.prompt, "code": state["python_code"],
                                               "reference solution": py.solution}),
            do_review(tag, "prompt", None, {"task": py.prompt, "answer": state["prompt_text"]}),
            do_review(tag, "mock", None, {"task": py.prompt, "code": state["python_code"],
                                          "transcript": transcript}),
        ]
        score = mock.score(state["python"], state["sql"], [r["scores"] for r in reviews],
                           state["duration_s"])
        db.update_mock(conn, mock_id, state, score)
        return {"score": score, "reviews": reviews, "readiness": mock.readiness(conn)}

    app.mount("/", StaticFiles(directory=config.WEB_DIR, html=True), name="web")
    return app


def main():
    import uvicorn

    config.load_env()
    uvicorn.run(create_app(), host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
