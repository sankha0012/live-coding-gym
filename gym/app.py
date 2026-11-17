import base64
import inspect
import json
import math
import os
import random
import secrets
import subprocess
from dataclasses import asdict
from datetime import date

from fastapi import FastAPI, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import assistant, cards, config, control, db, gates, interview, mock, reviewer, runner, whatif
from .content import load_content
from .kb import load_kb

CODED = ("python", "sql", "tests")
# "challenge" starts from an empty editor: it counts like any pass but never gates anything
MODES = {"python": ["blank", "challenge"], "sql": ["blank", "challenge"], "tests": ["blank", "challenge"]}


class RunBody(BaseModel):
    exercise_id: str
    code: str
    scope: str = ""   # a mock round, so that running code can be counted


class ExerciseBody(BaseModel):
    exercise_id: str


class WhatIfStartBody(ExerciseBody):
    fresh: bool = False   # new questions instead of the open ones


class WhatIfAnswerBody(ExerciseBody):
    answers: list[str]


class FixBody(ExerciseBody):
    code: str


class TriageBody(ExerciseBody):
    decisions: list[dict]


class InterviewBody(ExerciseBody):
    part: str = "main"      # main: the exercise's own questions; bug: name the bug; lines: explain two lines of your code
    action: str = "answer"  # answer | hint | skip
    text: str = ""


class MockInterviewBody(BaseModel):
    action: str = "answer"
    text: str = ""


class InterviewPart(ExerciseBody):
    part: str = "main"


class ControlChangeBody(ExerciseBody):
    code: str


class SubmitBody(RunBody):
    mode: str = "blank"
    duration_s: float = 0


class QuizBody(BaseModel):
    exercise_id: str
    answers: list[int]


class CardBody(BaseModel):
    card_id: str
    correct: bool


class UnlockBody(BaseModel):
    step_id: str


class MockSubmit(BaseModel):
    codes: list[str]
    duration_s: float


def create_app(content_dir=config.CONTENT_DIR, db_path=config.DB_PATH, call=None):
    steps, errors = load_content(content_dir)
    conn = db.connect(db_path)
    topics, kb_errors = load_kb(content_dir)
    errors = errors + kb_errors
    step_by_id = {s.id: s for s in steps}
    exercises = {ex.id: ex for s in steps for ex in s.exercises}
    all_cards = [c for s in steps if not s.optional for c in s.cards]  # the daily deck: required steps only
    app = FastAPI()

    def dev():
        """Dev mode: see everything, no gates. GYM_DEV=1 forces it on; otherwise it is a switch in the top bar."""
        return os.environ.get("GYM_DEV") == "1" or db.get_setting(conn, "dev", "") == "1"

    password = os.environ.get("GYM_PASSWORD")
    if password:  # a public deployment runs the learner's code, so it needs a password (HTTP Basic, any user name)
        @app.middleware("http")
        async def basic_auth(request, call_next):
            given = request.headers.get("authorization", "")
            try:
                ok = given.lower().startswith("basic ") and secrets.compare_digest(
                    base64.b64decode(given[6:]).decode().split(":", 1)[1], password)
            except Exception:
                ok = False
            if ok:
                return await call_next(request)
            return Response("Password needed", status_code=401, headers={"WWW-Authenticate": 'Basic realm="Live Coding Gym"'})

    def ai_call(prompt, json_mode=True):
        """Send a prompt to the AI provider chosen in the settings menu. `call` replaces it in tests."""
        if call is not None:  # a test double; only some of them care about json_mode
            return call(prompt, json_mode=json_mode) if "json_mode" in inspect.signature(call).parameters else call(prompt)
        provider = db.get_setting(conn, "provider", "gemini")
        return reviewer.PROVIDERS[provider][1](prompt, json_mode=json_mode)

    @app.middleware("http")
    async def no_cache(request, call_next):
        # The page files change while the app is being built; never let the browser reuse an old copy.
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store"
        return response

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

    def next_exercise(ex):
        """Next exercise in the same step, else the first exercise of the next step."""
        here = step_by_id[ex.step_id]
        siblings = here.exercises
        i = siblings.index(ex)
        if i + 1 < len(siblings):
            nxt = siblings[i + 1]
        else:
            later = [s for s in steps if not s.optional and s.order > here.order and s.exercises]
            nxt = later[0].exercises[0] if later else None
        return {"id": nxt.id, "title": nxt.title} if nxt else None

    def group_of(ex):
        """Which of the four moves an exercise practises: read it, build it, catch the bug, defend it."""
        if ex.kind == "read":
            return "Read"
        if ex.kind == "triage" or ex.name_bug:
            return "Catch"
        return "Build" if ex.kind in ("python", "sql", "tests", "prompt") else "Defend"

    TRAP_QUESTION = "In one sentence: what is the trap or surprise in this code?"
    BUILD_CHOICES, READ_CHOICES = ["pass", "fail"], ["same", "different", "crash"]

    def whatif_info(ex):
        """The What if rounds of a reading, of a core build, or of an assisted extra build."""
        row = db.get_whatif(conn, ex.id)
        needed = ex.kind == "read" or ex.control_level in (1, 2) or (not ex.control_level and status_of(ex)["assisted"])
        return {"needed": needed, "started": row is not None, "ok": bool(row and row["ok"]),
                "choices": READ_CHOICES if ex.kind == "read" else BUILD_CHOICES,
                "questions": [{"change": q["change"]} for q in json.loads(row["questions_json"])] if row else []}

    def control_info(ex):
        level = ex.control_level
        if not level:
            return None
        row = db.get_control(conn, ex.id)
        started = row is not None
        a, b = bool(row and row["a_ok"]), bool(row and row["b_ok"])
        w = bool(db.get_whatif(conn, ex.id) and db.get_whatif(conn, ex.id)["ok"])
        complete = {1: w, 2: w and b, 3: a and b}[level]
        return {"level": level, "started": started, "complete": complete, "a_ok": a, "b_ok": b, "whatif_ok": w,
                "lines": json.loads(row["lines_json"]) if started else [],
                "change": ex.change if (started or dev()) and level >= 2 else "",
                "locked": started and not complete and not dev(),
                "ready": db.last_passed_attempt(conn, ex.id) is not None,
                "whatif": whatif_info(ex)}

    def payload(ex, mode="blank"):
        st = status_of(ex)
        written = ex.kind == "read" and ex.level >= 2  # the model answer would give the written part away
        revealed = dev() or (st["review"] is True if written else st["tests"] is True or st["review"] is True)
        rk = reviewer.REVIEW_KIND.get(ex.kind) if ex.kind != "read" or ex.level >= 2 else None
        mode = mode if mode in MODES.get(ex.kind, []) else "blank"
        code = "" if mode == "challenge" else ex.starter
        schema = "\n".join(l for l in ex.seed.splitlines() if not l.startswith("INSERT"))
        shown_output = ex.kind == "read" and (dev() or st["tests"] is True)
        return {"id": ex.id, "step_id": ex.step_id, "title": ex.title, "kind": ex.kind, "prompt": ex.prompt,
                "serves": ex.serves, "docs": ex.docs, "modes": MODES.get(ex.kind, []), "mode": mode, "code": code,
                "schema": schema, "assistant": ex.assistant, "plan_required": ex.plan_required,
                "grade_prompts": ex.grade_prompts, "name_bug": ex.name_bug,
                "snippet": ex.snippet, "level": ex.level if ex.kind == "read" else ex.control_level,
                "questions": [] if ex.kind != "read" or ex.level < 2 else [TRAP_QUESTION] if ex.level == 2 else ex.questions,
                "fix": ex.fix if ex.level >= 3 else "", "whatif": whatif_info(ex), "expected": ex.expected if shown_output else "",
                "proposals": [{"title": p["title"], "code": p["code"], **({"correct": p["correct"], "why": p.get("why", "")} if dev() else {})}
                              for p in ex.proposals],
                "bug": ex.bug if dev() else "", "change_solution": ex.change_solution if dev() else "",
                "control": control_info(ex),
                "hint": ex.hint, "say": ex.say if revealed else "",
                "guide": ex.guide if revealed else "",
                "reference": ex.solution if revealed and ex.kind in CODED else "",
                "dev": dev(),
                "model_prompt": ex.model_prompt if revealed else "",
                "quiz": [{"q": q["q"], "options": q["options"], **({"answer": q["answer"], "why": q.get("why", "")} if dev() else {})}
                         for q in ex.quiz],
                "pass_ratio": ex.pass_ratio, "status": st, "next": next_exercise(ex),
                "kb": [{"id": t.id, "title": t.title, "summary": t.summary, "brief": t.brief}
                       for t in (topics.get(i) for i in ex.kb) if t],
                "review": review_dict(db.latest_review(conn, ex.id, rk)) if rk else None}

    def grade(ex, code):
        if ex.kind == "python":
            return runner.run_python_tests(code, ex.dir / "tests", files=ex.files)
        if ex.kind == "tests":
            return runner.run_test_writing(code, ex.impl_good, ex.impls_bad)
        return runner.check_sql(ex.seed, code, ex.solution, ex.ordered)

    def do_review(exercise_id, kind, rubric, material, attempt_id=None):
        result = reviewer.review(kind, rubric, material, ai_call)
        review_id = db.save_review(conn, exercise_id, kind, material, result, attempt_id)
        return {"review_id": review_id, **result}

    def next_up(rows):
        """First required exercise not yet done, in the first unlocked step that has not passed."""
        for s, row in zip(steps, rows):
            if not s.optional and row["unlocked"] and not row["passed"]:
                st = gates.step_status(conn, s)
                for ex in s.exercises:
                    if ex.required and not st["exercises"][ex.id]["done"]:
                        return {"step_id": s.id, "step_title": s.title, "exercise_id": ex.id, "title": ex.title}
        return None

    @app.get("/api/kb")
    def kb_index():
        return [{"id": t.id, "title": t.title, "summary": t.summary, "tags": t.tags} for t in topics.values()]

    @app.get("/api/kb/{topic_id}")
    def kb_topic(topic_id: str):
        t = need(topics.get(topic_id), "topic")
        return {"id": t.id, "title": t.title, "summary": t.summary, "tags": t.tags, "brief": t.brief, "body": t.body}

    class ChatBody(BaseModel):
        scope: str
        message: str
        explain_only: bool = False   # "ask about this" from a What if answer: explains, never writes code, works even while the check is locked
        code: str = ""
        output: str = ""

    class ScopeBody(BaseModel):
        scope: str

    def chat_context(scope):
        """What the assistant is helping with and what it may do."""
        if scope.startswith("mock:"):
            try:
                state = mock_state(int(scope[5:]))
            except ValueError:
                raise HTTPException(404, "mock not found")
            task = "\n\n".join(f"Python task {i}: {exercises[x].title}\n{exercises[x].prompt}"
                               for i, x in enumerate(state["python_ids"], 1))
            return {"title": "Mock round", "kind": "python", "task": task, "schema": "",
                    "policy": "free", "assist_key": None, "locked": False}
        ex = get_ex(scope)
        if ex.kind == "quiz":
            raise HTTPException(400, "The assistant is not available on quizzes: they are the check itself.")
        info = control_info(ex)
        return {"title": ex.title, "kind": ex.kind, "task": ex.prompt, "schema": schema_of(ex),
                "policy": ex.assistant, "assist_key": ex.id if ex.kind in CODED else None,
                "locked": bool(info and info["locked"])}

    def schema_of(ex):
        return "\n".join(l for l in ex.seed.splitlines() if not l.startswith("INSERT"))

    def chat_state(scope, ctx):
        rows = db.chat_history(conn, scope)
        return {"messages": [{"role": r["role"], "content": r["content"], "size": r["size"]} for r in rows],
                "policy": ctx["policy"], "locked": ctx["locked"],
                "provider": db.get_setting(conn, "provider", "gemini"),
                "assisted": bool(ctx["assist_key"]) and db.is_assisted(conn, ctx["assist_key"])}

    @app.get("/api/chat")
    def chat_get(scope: str):
        return chat_state(scope, chat_context(scope))

    @app.post("/api/chat")
    def chat_send(body: ChatBody):
        ctx = chat_context(body.scope)
        shown = ctx  # what the panel keeps showing: the asking does not unlock the exercise
        if body.explain_only and ctx["policy"] != "free":
            ctx = {**ctx, "policy": "explain", "locked": False}
        if ctx["policy"] == "off":
            raise HTTPException(403, "The assistant is off on this exercise.")
        if ctx["locked"]:
            raise HTTPException(403, "The assistant is off during the control check. Make the change by hand.")
        if not body.message.strip():
            raise HTTPException(400, "write a message first")
        history = db.chat_history(conn, body.scope)
        prompt = assistant.build_prompt(ctx["policy"], ctx["title"], ctx["kind"], ctx["task"], ctx["schema"],
                                        body.code, body.output, [dict(h) for h in history], body.message)
        try:
            raw = ai_call(prompt, json_mode=False)
        except Exception as e:  # network, quota, bad key: say so, keep the conversation intact
            raise HTTPException(502, f"The AI provider did not answer: {e}")
        size, reply = assistant.split_size(raw)
        db.add_chat(conn, body.scope, "user", body.message, ctx["policy"])
        db.add_chat(conn, body.scope, "assistant", reply, ctx["policy"], size)
        if ctx["policy"] in ("train", "free") and ctx["assist_key"] and assistant.has_code_block(reply):
            db.mark_assisted(conn, ctx["assist_key"])
        return {"reply": reply, "size": size, **chat_state(body.scope, shown)}

    @app.post("/api/chat/clear")
    def chat_clear(body: ScopeBody):
        chat_context(body.scope)
        db.clear_chat(conn, body.scope)
        return {"ok": True}

    @app.post("/api/chat/grade")
    def chat_grade(body: ScopeBody):
        """Score the prompts the learner typed, the way the interviewer judges them."""
        ctx = chat_context(body.scope)
        typed = db.user_messages(conn, body.scope)
        if not typed:
            raise HTTPException(400, "You have not sent the assistant any prompts yet.")
        answer = "\n\n".join(f"Prompt {i}: {m}" for i, m in enumerate(typed, 1))
        # stored under a separate id so it never counts as the exercise's own prompt review
        return do_review(f"chat:{body.scope}", "prompt", None, {"task": ctx["task"], "answer": answer})

    @app.post("/api/progress/reset")
    def progress_reset():
        db.reset_progress(conn)
        return {"ok": True}

    class SettingsBody(BaseModel):
        provider: str

    def settings_payload():
        return {"provider": db.get_setting(conn, "provider", "gemini"), "providers": reviewer.provider_info()}

    @app.get("/api/settings")
    def settings():
        return settings_payload()

    @app.post("/api/settings")
    def settings_save(body: SettingsBody):
        info = {p["id"]: p for p in reviewer.provider_info()}
        if body.provider not in info:
            raise HTTPException(400, "unknown provider")
        if not info[body.provider]["configured"]:
            raise HTTPException(400, f"no API key for {info[body.provider]['label']} in .env")
        db.set_setting(conn, "provider", body.provider)
        return settings_payload()

    @app.get("/api/dev")
    def dev_get():
        return {"dev": dev(), "forced": os.environ.get("GYM_DEV") == "1"}

    class DevBody(BaseModel):
        dev: bool

    @app.post("/api/dev")
    def dev_set(body: DevBody):
        db.set_setting(conn, "dev", "1" if body.dev else "0")
        return dev_get()

    @app.get("/api/version")
    def version():
        """Short git commit of the code that is running, so you can tell which copy you are using."""
        try:
            out = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=config.ROOT,
                                 capture_output=True, text=True, timeout=5)
            return {"version": out.stdout.strip() or "unknown", "path": str(config.ROOT)}
        except Exception:
            return {"version": "unknown", "path": str(config.ROOT)}

    @app.get("/api/journey")
    def journey():
        mocks = [{"id": r["id"], "started_at": r["started_at"],
                  "total": json.loads(r["score_json"])["total"]} for r in db.finished_mocks(conn)]
        rows = gates.journey(conn, steps, dev())
        return {"dev": dev(), "steps": rows, "next": next_up(rows), "readiness": mock.readiness(conn), "mocks": mocks,
                "due_cards": len(cards.due(conn, all_cards, date.today())), "errors": errors}

    @app.get("/api/step/{step_id}")
    def step(step_id: str):
        s = need(step_by_id.get(step_id), "step")
        st = gates.step_status(conn, s)
        gate = {"min_score": s.min_score, "pass_ratio": s.pass_ratio,
                "total": st["total"], "done": st["done"], "needed": math.ceil(s.pass_ratio * st["total"])}
        return {"id": s.id, "title": s.title, "lessons": s.lessons, "gate": gate, "optional": s.optional, "intro": s.intro,
                "exercises": [{"id": ex.id, "title": ex.title, "kind": ex.kind, "required": ex.required,
                               "group": group_of(ex), "serves": ex.serves,
                               "status": st["exercises"][ex.id]} for ex in s.exercises]}

    @app.get("/api/exercise/{exercise_id}")
    def exercise(exercise_id: str, mode: str = "blank"):
        return payload(get_ex(exercise_id), mode)

    @app.post("/api/run")
    def run(body: RunBody):
        ex = get_ex(body.exercise_id)
        if body.scope.startswith("mock:"):
            db.add_event(conn, body.scope, "run")
        if ex.kind == "tests":
            return asdict(grade(ex, body.code))
        if ex.kind == "sql":
            return asdict(runner.run_sql_free(ex.seed, body.code))
        return asdict(runner.run_python_free(body.code))

    @app.post("/api/submit")
    def submit(body: SubmitBody):
        ex = get_ex(body.exercise_id)
        if ex.kind not in CODED:
            raise HTTPException(400, "this exercise has no code to submit; use review")
        plan_lines = sum(1 for line in body.code.splitlines() if line.strip().startswith("#"))
        if plan_lines < ex.plan_required:
            return {"passed": False, "tests": [], "timed_out": False, "plan_missing": True, "status": status_of(ex),
                    "output": f"Write your plan first, as comments (lines starting with #). This exercise asks for at "
                              f"least {ex.plan_required} plan lines before the code; you have {plan_lines}."}
        result = grade(ex, body.code)
        attempt_id = db.record_attempt(conn, ex.id, body.mode, body.code, result.passed,
                                       body.duration_s, result.output)
        return {**asdict(result), "attempt_id": attempt_id, "status": status_of(ex)}

    @app.post("/api/reviews/{review_id}/retry")
    def retry(review_id: int):
        row = need(db.get_review(conn, review_id), "review")
        ex = exercises.get(row["exercise_id"])
        rubric = ex.rubric if ex and reviewer.REVIEW_KIND.get(ex.kind) == row["kind"] else None
        result = reviewer.review(row["kind"], rubric, json.loads(row["material_json"]), ai_call)
        db.update_review(conn, review_id, result)
        return {"review_id": review_id, **result}

    def norm_output(text):
        return "\n".join(line.rstrip() for line in text.strip().splitlines())

    def judge_build(ex):
        """Run changed code the way the exercise grades code: ('pass' or 'fail', a short reason)."""
        def judge(code):
            r = grade(ex, code)
            if r.passed:
                return "pass", "The tests still pass."
            failed = [t["name"] for t in r.tests if not t["passed"]]
            last = next((l for l in reversed(r.output.strip().splitlines()) if l.strip()), "")
            return "fail", f"Failing: {', '.join(failed[:3])}." if failed else last[:160]
        return judge

    def make_questions(ex, rounds):
        """(source attempt id, questions with answers) for one round of What if."""
        if ex.kind == "read":
            want = 2 if ex.level == 1 else 3
            variants = list(ex.whatif)
            random.Random(f"{ex.id}{rounds}").shuffle(variants)
            both = [next((v for v in variants if (v["answer"] == "same") == flag), None) for flag in (True, False)]
            chosen = [v for v in both if v] + [v for v in variants if v not in both]
            return 0, [{"change": v["change"], "answer": v["answer"], "result": v.get("result", "")} for v in chosen[:want]]
        attempt = db.last_passed_attempt(conn, ex.id)
        if attempt is None:
            raise HTTPException(400, "Pass the tests first. What if works on your passing code.")
        want = 2 if ex.control_level == 1 or not ex.control_level else 3
        qs = whatif.pick(attempt["code"], attempt["id"] * 101 + rounds, judge_build(ex), want=want, sql=ex.kind == "sql")
        if not qs:
            raise HTTPException(400, "This code has no line that can be changed. Write a longer solution.")
        return attempt["id"], qs

    @app.post("/api/whatif/start")
    def whatif_start(body: WhatIfStartBody):
        """Open (or reopen, or refresh) the What if questions for an exercise."""
        ex = get_ex(body.exercise_id)
        if ex.kind != "read" and ex.kind not in ("python", "sql"):
            raise HTTPException(400, "this exercise has no What if rounds")
        row = db.get_whatif(conn, ex.id)
        newest = 0 if ex.kind == "read" else (db.last_passed_attempt(conn, ex.id) or {"id": None})["id"]
        if row and (row["ok"] or (not body.fresh and row["source_id"] == newest)):
            return {"whatif": whatif_info(ex), "status": status_of(ex)}
        source, qs = make_questions(ex, (row["rounds"] + 1) if row else 0)
        db.save_whatif(conn, ex.id, source, qs, (row["rounds"] + 1) if row else 0)
        return {"whatif": whatif_info(ex), "status": status_of(ex)}

    @app.post("/api/whatif/answer")
    def whatif_answer(body: WhatIfAnswerBody):
        ex = get_ex(body.exercise_id)
        row = need(db.get_whatif(conn, ex.id), "What if round")
        qs = json.loads(row["questions_json"])
        if len(body.answers) != len(qs):
            raise HTTPException(400, "answer every question")
        results = [{"correct": a == q["answer"], "answer": q["answer"], "result": q.get("result", "")} for a, q in zip(body.answers, qs)]
        ok = all(r["correct"] for r in results)
        if ok:
            db.set_whatif_ok(conn, ex.id, True)
        else:  # the answers were just shown, so the next try gets a new set
            source, fresh = make_questions(ex, row["rounds"] + 1)
            db.save_whatif(conn, ex.id, source, fresh, row["rounds"] + 1)
        return {"results": results, "ok": ok, "whatif": whatif_info(ex), "control": control_info(ex), "status": status_of(ex)}

    @app.post("/api/fix")
    def fix(body: FixBody):
        """Reading, level 3: change the code so that it prints the target output."""
        ex = get_ex(body.exercise_id)
        if ex.kind != "read" or ex.level < 3:
            raise HTTPException(400, "this exercise has no fix task")
        result = runner.run_python_free(body.code, timeout=30)
        passed = result.passed and norm_output(result.output) == norm_output(ex.fix_expected)
        db.record_attempt(conn, ex.id, "fix", body.code, passed, 0, result.output)
        return {"passed": passed, "output": result.output, "status": status_of(ex)}

    @app.post("/api/triage")
    def triage(body: TriageBody):
        """triage exercises: accept or reject each proposed change; the reasons are shown after."""
        ex = get_ex(body.exercise_id)
        if ex.kind != "triage":
            raise HTTPException(400, "this exercise is not a triage exercise")
        if len(body.decisions) != len(ex.proposals):
            raise HTTPException(400, "decide on every proposed change")
        results = [{"correct": d.get("choice") == p["correct"], "key": p["correct"], "why": p.get("why", "")}
                   for d, p in zip(body.decisions, ex.proposals)]
        correct = sum(r["correct"] for r in results)
        passed = correct / len(ex.proposals) >= ex.pass_ratio
        attempt_id = db.record_attempt(conn, ex.id, "blank", json.dumps(body.decisions), passed, 0,
                                       f"{correct}/{len(ex.proposals)}")
        return {"passed": passed, "correct": correct, "total": len(ex.proposals), "results": results,
                "attempt_id": attempt_id, "status": status_of(ex)}

    BUG_QUESTION = "In one sentence: what was the bug, where was it, and what did it cause?"

    def interview_def(ex, part):
        """(questions, reference answer, rubric, context) of one written exchange."""
        if part == "main" and ex.kind == "read" and ex.level >= 2:
            return ([TRAP_QUESTION] if ex.level == 2 else ex.questions), ex.say, [], ex.snippet
        if part == "main" and ex.kind in ("open", "explain"):
            return [ex.prompt], ex.say, ex.rubric, ""
        if part == "main" and ex.kind == "prompt":
            return [ex.prompt], ex.model_prompt or ex.say, ex.rubric, ""
        if part == "bug" and ex.name_bug:
            attempt = db.last_passed_attempt(conn, ex.id)
            if attempt is None:
                raise HTTPException(400, "Fix the code and pass the tests first.")
            return [BUG_QUESTION], ex.bug, [], f"The assistant's buggy code:\n{ex.starter}\n\nThe candidate's fixed code:\n{attempt['code']}"
        if part == "lines" and ex.control_level == 3:
            row, attempt = db.get_control(conn, ex.id), db.last_passed_attempt(conn, ex.id)
            if row is None or attempt is None:
                raise HTTPException(400, "Start the control check first.")
            return [f"Line {l['no']}: `{l['text'].strip()}`. What does this line do, and why is it there?"
                    for l in json.loads(row["lines_json"])], "", [], attempt["code"]
        raise HTTPException(400, "this exercise has no such written exchange")

    def interview_view(state):
        i = interview.current(state)
        return {"qs": [{"q": q["q"], "turns": q["turns"], "verdict": q["verdict"], "strong": q["strong"], "hinted": q["hinted"],
                        "followups": q["followups"]} for q in state["qs"]], "i": i, "done": state["done"], "passed": state["passed"]}

    def interview_state(ex, part):
        scope = f"{ex.id}:{part}"
        state = db.get_interview(conn, scope)
        if state is None:
            state = interview.new_state(interview_def(ex, part)[0])
            db.save_interview(conn, scope, state)
        return scope, state

    def interview_finish(ex, part, state):
        passed = state["passed"]
        if part == "lines":
            db.set_control_part(conn, ex.id, "a", passed)
        kind = {"main": reviewer.REVIEW_KIND.get(ex.kind), "bug": "bug", "lines": "line"}[part]
        attempt = db.last_passed_attempt(conn, ex.id)
        db.save_review(conn, ex.id, kind, {"interview": state},
                       {"status": "done", "scores": interview.scores(state),
                        "verdict": f"{sum(q['verdict'] != 'missed' for q in state['qs'])} of {len(state['qs'])} answered well",
                        "feedback": " ".join(q["strong"] for q in state["qs"] if q["strong"])}, attempt["id"] if attempt else None)

    @app.get("/api/interview")
    def interview_get(exercise_id: str, part: str = "main"):
        ex = get_ex(exercise_id)
        return interview_view(interview_state(ex, part)[1])

    @app.post("/api/interview/answer")
    def interview_answer(body: InterviewBody):
        ex = get_ex(body.exercise_id)
        if body.action not in ("answer", "hint", "skip"):
            raise HTTPException(400, "unknown action")
        questions, reference, rubric, context = interview_def(ex, body.part)
        scope, state = interview_state(ex, body.part)
        i = interview.current(state)
        if i is None:
            raise HTTPException(400, "This exchange is finished.")
        q = state["qs"][i]
        if body.action == "answer" and not body.text.strip():
            raise HTTPException(400, "Write your answer first.")
        if body.action == "hint" and q["hinted"]:
            raise HTTPException(400, "You already used the hint for this question.")
        if body.action == "skip":
            move = interview.skip_move(q, reference)
        else:
            try:
                move = interview.ask(ai_call, q, reference, rubric, context, body.action, body.text.strip())
            except RuntimeError as e:
                raise HTTPException(502, str(e))
        interview.apply(state, body.action, body.text.strip(), move)
        db.save_interview(conn, scope, state)
        if state["done"]:
            interview_finish(ex, body.part, state)
        return {**interview_view(state), "status": status_of(ex), "control": control_info(ex)}

    @app.post("/api/interview/reset")
    def interview_reset(body: InterviewPart):
        ex = get_ex(body.exercise_id)
        scope, state = interview_state(ex, body.part)
        if state["passed"]:
            raise HTTPException(400, "You passed this one.")
        db.delete_interview(conn, scope)
        return interview_view(interview_state(ex, body.part)[1])

    @app.post("/api/control/start")
    def control_start(body: ExerciseBody):
        """Begin the control check on the learner's latest passing code: two random lines to explain, then a change."""
        ex = get_ex(body.exercise_id)
        level = ex.control_level
        if not level:
            raise HTTPException(400, "this exercise has no control check")
        attempt = db.last_passed_attempt(conn, ex.id)
        if attempt is None:
            raise HTTPException(400, "Pass the tests first. The control check works on your passing code.")
        row = db.get_control(conn, ex.id)
        done = control_info(ex)["complete"]
        if row is None or (not done and row["attempt_id"] != attempt["id"]):
            db.start_control(conn, ex.id, attempt["id"], control.pick_lines(attempt["code"], attempt["id"]) if level == 3 else [])
            db.delete_interview(conn, f"{ex.id}:lines")
        if level < 3:
            whatif_start(WhatIfStartBody(exercise_id=ex.id))
        return {"control": control_info(ex), "code": attempt["code"], "status": status_of(ex)}

    @app.post("/api/control/change")
    def control_change(body: ControlChangeBody):
        ex = get_ex(body.exercise_id)
        row = db.get_control(conn, ex.id)
        if row is None or ex.control_level < 2 or not ex.change_dir:
            raise HTTPException(400, "Start the control check first.")
        if ex.kind == "sql":
            result = runner.check_sql(ex.seed, body.code, ex.change_solution, ex.ordered)
        else:
            result = runner.run_python_tests(body.code, ex.change_dir, files=ex.files)
        db.record_attempt(conn, ex.id, "change", body.code, result.passed, 0, result.output)
        db.set_control_part(conn, ex.id, "b", result.passed)
        return {**asdict(result), "control": control_info(ex), "status": status_of(ex)}

    @app.post("/api/quiz")
    def quiz(body: QuizBody):
        ex = get_ex(body.exercise_id)
        if ex.kind != "quiz":
            raise HTTPException(400, "this exercise is not a quiz")
        if len(body.answers) != len(ex.quiz):
            raise HTTPException(400, "answer every question")
        results = [{"correct": a == q["answer"], "answer": q["answer"], "why": q.get("why", "")}
                   for q, a in zip(ex.quiz, body.answers)]
        correct = sum(r["correct"] for r in results)
        passed = correct / len(ex.quiz) >= ex.pass_ratio
        attempt_id = db.record_attempt(conn, ex.id, "blank", json.dumps(body.answers), passed,
                                       0, f"{correct}/{len(ex.quiz)}")
        return {"passed": passed, "correct": correct, "total": len(ex.quiz), "results": results,
                "attempt_id": attempt_id, "status": status_of(ex)}

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

    def typed_prompts(mock_id):
        """The prompts the learner typed to the assistant during this mock round, numbered; '' if none."""
        msgs = db.user_messages(conn, f"mock:{mock_id}")
        return "\n\n".join(f"Prompt {i}: {m}" for i, m in enumerate(msgs, 1))

    @app.post("/api/mock/start")
    def mock_start():
        try:
            picked = mock.pick(steps)
        except ValueError as e:
            raise HTTPException(400, str(e))
        mock_id = db.create_mock(conn, {"python_ids": [ex.id for ex in picked]})
        return {"mock_id": mock_id, "time_limit_s": mock.MOCK_TIME_S, "tasks": [payload(ex) for ex in picked]}

    @app.post("/api/mock/{mock_id}/submit")
    def mock_submit(mock_id: int, body: MockSubmit):
        state = mock_state(mock_id)
        tasks = [exercises[i] for i in state["python_ids"]]
        codes = (body.codes + [""] * len(tasks))[:len(tasks)]
        # one line from each task (two from the only task), picked at random but fixed per mock round
        lines = []
        for i, (ex, code) in enumerate(zip(tasks, codes)):
            for ln in control.pick_lines(code, mock_id, 2 if len(tasks) == 1 else 1):
                lines.append({"task": i, **ln})
        all_task = "\n\n".join(f"Task {i}: {ex.prompt}" for i, ex in enumerate(tasks, 1))
        all_code = "\n\n".join(f"# Task {i}\n{c}" for i, c in enumerate(codes, 1))
        state.update(codes=codes, duration_s=body.duration_s, results=[asdict(grade(ex, c)) for ex, c in zip(tasks, codes)],
                     lines=lines[:2], questions=reviewer.followups(all_task, all_code, ai_call))
        db.update_mock(conn, mock_id, state)
        asked = [f"Task {l['task'] + 1}, line {l['no']}: `{l['text'].strip()}`. What does this line do, and why is it there?" for l in state["lines"]]
        db.save_interview(conn, f"mock:{mock_id}", interview.new_state(asked + state["questions"]))
        return {"results": state["results"], "interview": interview_view(db.get_interview(conn, f"mock:{mock_id}"))}

    def mock_behaviour(mock_id):
        """From the chat: share of small asks, share of code replies that were run before moving on."""
        scope = f"mock:{mock_id}"
        sizes = [r["size"] for r in db.chat_history(conn, scope) if r["role"] == "assistant" and r["size"]]
        coded = [r["id"] for r in db.chat_history(conn, scope) if r["role"] == "assistant" and assistant.has_code_block(r["content"])]
        ran = set(db.events(conn, scope, "run"))
        return mock.ratio(sizes.count("small"), len(sizes)), mock.ratio(sum(i in ran for i in coded), len(coded))

    def mock_context(state):
        tasks = [exercises[i] for i in state["python_ids"]]
        return "\n\n".join(f"Task {i}: {ex.prompt}\n\nThe candidate's code:\n{c}" for i, (ex, c) in enumerate(zip(tasks, state["codes"]), 1))

    def mock_finish(mock_id, state, view):
        """All follow-ups answered: review the code and the prompts, then score the round."""
        tasks = [exercises[i] for i in state["python_ids"]]
        tag = f"mock:{mock_id}"  # kept apart from the exercise so mock reviews never affect step gates
        reviews = [do_review(tag, "code", ex.rubric, {"task": ex.prompt, "code": code, "reference solution": ex.solution})
                   for ex, code in zip(tasks, state["codes"])]
        typed = typed_prompts(mock_id)
        if typed:
            reviews.append(do_review(tag, "prompt", None, {"task": tasks[0].prompt, "answer": typed}))
        talk = interview.get_scores(view)
        n_lines = len(state["lines"])
        line_scores, question_scores = talk[:n_lines], talk[n_lines:]
        asks, ran = mock_behaviour(mock_id)
        score = mock.score(state["results"], [r["scores"] for r in reviews] + [{f"Q{i}": v for i, v in enumerate(question_scores, 1)}],
                           state["duration_s"], asks, ran, mock.ratio(sum(line_scores), 5 * len(line_scores)))
        db.update_mock(conn, mock_id, state, score)
        return {"score": score, "reviews": reviews, "readiness": mock.readiness(conn)}

    @app.get("/api/mock/{mock_id}/interview")
    def mock_interview_get(mock_id: int):
        mock_state(mock_id)
        return interview_view(need(db.get_interview(conn, f"mock:{mock_id}"), "interview"))

    @app.post("/api/mock/{mock_id}/interview/answer")
    def mock_interview_answer(mock_id: int, body: MockInterviewBody):
        state = mock_state(mock_id)
        scope = f"mock:{mock_id}"
        talk = need(db.get_interview(conn, scope), "interview")
        i = interview.current(talk)
        if i is None or body.action not in ("answer", "hint", "skip"):
            raise HTTPException(400, "This exchange is finished or the action is unknown.")
        q = talk["qs"][i]
        if body.action == "answer" and not body.text.strip():
            raise HTTPException(400, "Write your answer first.")
        if body.action == "hint" and q["hinted"]:
            raise HTTPException(400, "You already used the hint for this question.")
        if body.action == "skip":
            move = interview.skip_move(q, "")
        else:
            try:
                move = interview.ask(ai_call, q, "", [], mock_context(state), body.action, body.text.strip())
            except RuntimeError as e:
                raise HTTPException(502, str(e))
        interview.apply(talk, body.action, body.text.strip(), move)
        db.save_interview(conn, scope, talk)
        view = interview_view(talk)
        return {**view, **(mock_finish(mock_id, state, talk) if talk["done"] else {})}

    app.mount("/", StaticFiles(directory=config.WEB_DIR, html=True), name="web")
    return app


def main():
    import uvicorn

    config.load_env()
    uvicorn.run(create_app(), host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
