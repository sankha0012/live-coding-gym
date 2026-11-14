# Live Coding Gym: design spec

Date: 2026-11-14. Status: awaiting approval.

## 1. Purpose

A local training app that takes one person from "knows Python and SQL theory but has always coded with AI tools, so cannot write code by hand" to "ready for a live-coding interview on software engineering for production ML systems".

The target interview (iFood, on Coderbyte) has these known rules:

- Live practical coding on robust, deterministic, reliable ML systems facing real data behaviour and common model failures.
- Python is allowed. Exercise documentation can be consulted.
- Coderbyte's own AI assistant is off, but another AI assistant may be used.
- The candidate must explain the code afterwards, and the interviewer also evaluates the prompt that was used.

Success means: whoever passes every gate in the journey can (a) write working Python and SQL by hand in a blank editor under time pressure, (b) build robust ML-system code, (c) talk credibly about common AI/ML engineering tools, (d) use an AI assistant in a way an observer respects, and (e) explain the resulting code.

## 2. Scope decisions

- One user, on one Mac. No accounts, no hosting, no payments. Rough visual finish is acceptable.
- Comprehensive content and a clear step-by-step journey matter more than anything else.
- Evaluation is automatic tests in real Python or SQL plus an AI review against a rubric. The reviewer is Gemini, using the user's key in `.env` (`GEMINI_API_KEY`).
- No diagnostic step. The starting level is known: theory is solid, manual coding is close to zero.
- SQL is a first-class track next to Python.

Out of scope for now: voice input, multiple users, mobile layout, languages other than Python and SQL, a sandbox for untrusted code (the only code that runs is the user's own).

## 3. Architecture

A small local web app with four parts.

**Server** (`gym/`, Python, FastAPI and uvicorn). Serves the page and a JSON API. Started with one command; opens at `http://localhost:8000`.

**Runner** (`gym/runner.py`). Runs a submission and returns structured results.

- Python exercises: copy the submission and the exercise's hidden tests into a temporary directory, run `pytest` in a subprocess with a timeout, parse pass or fail per test, return output and tracebacks.
- SQL exercises: build a fresh in-memory SQLite database from the exercise's seed script, run the user's query and the reference query, and compare result sets (order-sensitive only when the exercise says so). Uses the standard-library `sqlite3` module.
- Free-run mode: run the code or query without tests so the user can experiment, as on Coderbyte.

**Reviewer** (`gym/reviewer.py`). Calls the Gemini REST API with the standard library (no SDK). The model name comes from `GEMINI_MODEL` in `.env`. Each call sends a rubric and the material to judge, and asks for JSON: a score per rubric criterion, an overall verdict, and specific feedback. Five review kinds:

1. Code review: correctness beyond the tests, edge cases, readability, production thinking.
2. Explanation review: the user's written explanation of their own code.
3. Prompt review: the prompt the user would give an AI assistant, judged as the interviewer would judge it.
4. Open-answer grading: theory questions, mainly in the tools tour.
5. Mock interviewer: follow-up questions about the submitted code, then a graded transcript.

If Gemini is unreachable or returns unusable output, tests still work and the review is stored as pending so it can be retried. A review failure never loses a submission.

**Page** (`web/`, plain HTML, CSS and JavaScript, no build step). CodeMirror loaded from a CDN as the editor, with autocomplete switched off on purpose so the editor behaves like a bare interview editor. Views: journey map, lesson, exercise (instructions, editor, run, submit, results, review), flashcards, mock round, progress.

**Storage**. Content is plain files (section 5). Progress is one SQLite file, `data/progress.db`: attempts, test results, reviews, gate status, flashcard schedule, mock history.

## 4. The journey

Twelve steps. Every step has the same shape: short theory, worked examples, drills with hidden tests, an AI-reviewed piece, and a gate. The next step unlocks when the gate passes (an "unlock anyway" switch exists, because the user is the only user).

| # | Step | Focus |
|---|------|-------|
| 1 | Hand-coding Python from zero | Typing core Python from memory: loops, conditionals, strings, lists, dicts, sets, comprehensions, functions, classes, dataclasses, exceptions, files and JSON, type hints, `collections`, `itertools`, `datetime`. |
| 2 | The live-coding routine | The six-step routine from the existing gym, applied to classic Coderbyte-style problems under a clock. |
| 3 | Hand-coding SQL | SELECT, filtering, joins, GROUP BY and HAVING, subqueries, CTEs, window functions, NULL handling, deduplication, date logic. |
| 4 | Robust code | Input validation, error handling, determinism (seeds, ordering, time), idempotency, retries and backoff, timeouts, logging. |
| 5 | Testing your own code | Writing pytest tests by hand: fixtures, parametrize, edge cases, testing failure paths. |
| 6 | Real data behaviour | Nulls, duplicates, schema drift, type drift, outliers, leakage, train and test splits, in pandas and in SQL (data-quality queries). |
| 7 | AI/ML engineering tools tour | Theory and examples only: scikit-learn pipelines, experiment tracking (MLflow), orchestration (Airflow), containers (Docker), model serving (FastAPI), feature stores, data and model versioning, monitoring and drift tools, CI/CD for ML, cloud ML platforms. For each tool: what problem it solves, a minimal real example, where it sits in a pipeline, and how to speak about it honestly. |
| 8 | Production ML systems | Batch and online inference, input contracts, fallbacks, circuit breakers, caching, event handling, monitoring, drift detection. |
| 9 | Common model failures | Missing features, out-of-range inputs, stale models, NaN outputs, score drift, silent failure, and the code that defends against each. |
| 10 | Using an AI assistant while observed | Writing a prompt the interviewer will judge, constraining the assistant, verifying its output, catching its mistakes. |
| 11 | Explaining your code | Walking through code you wrote or accepted: structure, trade-offs, complexity, failure modes, what you would do next. |
| 12 | Mock rounds and readiness | Timed, Coderbyte-shaped rounds mixing Python, SQL, AI use and explanation, with Gemini asking follow-ups, ending in a readiness score. |

### How step 1 and step 3 build manual skill

These steps exist because the user's gap is recall and typing, not understanding. They use four exercise modes, in increasing difficulty:

1. **Retype**: read a short solution, hide it, reproduce it from memory. Tests decide.
2. **Fill the gaps**: code with missing lines.
3. **Blank editor**: only the task statement.
4. **Timed blank editor**: the same, against a clock.

Small patterns (a dict count, a group-by, a window function) also become **flashcards** on a simple spaced-repetition schedule (Leitner boxes), so they return until they are automatic. A short daily warm-up serves the cards that are due.

### Gates

A step's gate passes when all of these hold:

- Every required drill passes its hidden tests in blank-editor mode.
- The step's AI-reviewed pieces score at or above the threshold on every rubric criterion.
- For steps 1 and 3, the timed drills are completed inside their time limits.

Step 12's readiness score combines the last three mock rounds: test pass rate, time used, and Gemini's rubric scores for code, prompt and explanation. The app states plainly that the score is an estimate.

## 5. Content format

Content lives in `content/`, one folder per step, so writing content never touches app code.

```
content/
  04-robust-code/
    step.yaml            # title, order, gate rules
    lessons/01-validation.md
    exercises/validate-payload/
      exercise.yaml      # kind (python|sql|open|prompt|explain), modes, time limit, rubric
      prompt.md
      starter.py
      solution.py
      tests/test_hidden.py
    cards.yaml           # flashcards for this step
```

SQL exercises carry `seed.sql` and `solution.sql` in place of the Python files.

The 55 drills, the lessons and the mocks in the existing `live-coding-gym.html` are migrated into this format and placed in the matching steps.

## 6. Error handling

- Submission timeout or crash: reported as a failed run with the output, never as a server error.
- Infinite loops: the subprocess is killed at the time limit.
- Gemini failure, quota or malformed JSON: one retry, then the review is stored as pending.
- Broken content file: the server lists the broken exercise at start-up and skips it; the rest of the app runs.

## 7. Testing

- Unit tests for the runner (pass, fail, timeout, syntax error), the SQL comparer (order, duplicates, NULLs), gate logic, and the flashcard schedule.
- Reviewer tests with a stubbed Gemini response, including malformed output.
- A content check that runs every exercise's reference solution against its own hidden tests. No exercise ships if its own solution fails.
- One live check of the Gemini key and model name before the reviewer is built on it.

## 8. Build order

1. App skeleton: server, runner, exercise page, progress storage, with one Python and one SQL exercise working end to end.
2. Reviewer with all five review kinds, and gates.
3. Flashcards and the four exercise modes.
4. Content, in journey order, starting with steps 1 to 3 because they address the user's main gap. Existing gym content is migrated along the way.
5. Mock rounds and the readiness score.

The app is usable for practice from the end of phase 1, and each later phase adds to a working app.

## 9. Open points

- Interview date is not known. If it is close, content for steps 4, 8, 9, 10 and 11 moves ahead of the full versions of steps 5 to 7.
- The exact Gemini model is chosen at build time from what the key can access.
