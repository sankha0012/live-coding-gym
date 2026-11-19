# Design

The app trains one skill: **staying in control while an AI assistant writes code**, for an interview on software engineering for ML systems in production (robust, deterministic, reliable code against real data behaviour and common model failures; an assistant is allowed, the candidate explains the code afterwards and the prompt is judged; documentation can be consulted; Python).

The learner is the engineer and the assistant is the typist: plan before prompting, ask small, read every line, run it, catch what is wrong, fix it by hand, explain it.

## Competencies (from the recruiter's email)

C1 Coderbyte (stdin, stdout, run, test) · C2 production-quality Python for ML systems · C3 robust code · C4 deterministic code · C5 reliable code (retries, timeouts, fallbacks, idempotency) · C6 real data behaviour · C7 common model failures · C8 steering the assistant (the prompt is graded) · C9 explaining every line · C10 using the documentation given.

Every exercise names the competencies it serves in `serves:`.

## Steps

| Step | Folder | Moves |
|---|---|---|
| 1 Read Python fluently | `s01-read-python` | read |
| 2 The control loop on Coderbyte | `s02-control-loop` | build, prompts, documentation tasks |
| 3 Catch the assistant's mistakes | `s03-catch-mistakes` | catch |
| 4 Deterministic and robust code | `s04-robust-code` | read, build, catch, defend |
| 5 Real data behaviour | `s05-real-data` | same |
| 6 Common model failures | `s06-model-failures` | same |
| 7 ML systems in production | `s07-production-ml` | same |
| 8 Explain and defend | `s08-explain-defend` | defend |
| 9 Mock rounds | `s09-mock-rounds` | timed rounds |
| 10 SQL for data work (optional) | `s10-sql` | same four moves; always open, never blocks |

Each topic is taught in four moves: **read** it (What if: one line changes, what happens?), **build** it (plan in comments, small asks, run, the interviewer's questions about your code, a change by hand), **catch** it (assistant-written bug, assistant off, name the bug), **defend** it (the follow-up question). A step page groups exercises that way. `required: true` (the default) marks the core path that counts toward the step gate; `required: false` is extra practice. A step passes at 70% of its core exercises; a step unlocks when the previous one passes (or by hand).

## Mechanisms

- **Assistant policy per exercise** (`assistant:`): `train` (default for code: one small function per ask, bigger asks are sent back), `explain` (never writes code), `off`, `free` (mock rounds). Every reply carries a hidden small/large size mark. If the assistant writes code, the learner must explain it to finish the exercise.
- **What if** (readings only): a hand-written change to a reading's snippet, and you say what happens: the output stays the same, changes or crashes. Changes are authored in `whatif.yaml` and verified by running them. A wrong round shows the answers and is replaced by new questions.
- **The interviewer's questions about your own code** are the control check on builds (`part: defend` in `gym/interview.py`). After the tests pass, one AI call writes the questions from the task, your passing code with line numbers, the reference solution (private) and the step's theme: a design choice on a quoted line, an edge case or bad input, and (levels 2 and 3) a production concern. Each question carries private notes on a strong answer. They are asked one at a time as the written exchange below. The questions are written once and saved; new passing code or "Try again" gets new ones, with the old ones passed in to be avoided. If the AI cannot write them the route answers 502: a check without real questions proves nothing. The earlier design (a pass/fail What if on mutated lines, or two random lines explained) was dropped because it was guessable, judged by hidden tests the learner never sees, and mostly line deletions. Credit already earned under it still counts (`gates.defended`).
- **Levels** decide how much evaluation an exercise carries, so easy ones stay quick.
  - Core builds: level 1 (solution up to 10 lines) is 2 interviewer questions; levels 2 (11 to 20 lines) and 3 (over 20 lines) are 3 questions, then one small change by hand with the assistant locked (`change.md`, `change_tests/` and `change_solution.py`, or `change_solution.sql`). The level follows the size of the reference solution unless `level:` is set in `exercise.yaml`.
  - Readings carry `level:` in `exercise.yaml`: level 1 is a What if round of 2; level 2 adds one sentence naming the trap; level 3 adds a fix task (`fix.md`, `fix_expected.txt`, `fix_solution.py`) and a written explanation.
  - Extra-practice builds need no check, except 2 interviewer questions when the assistant wrote the code.
- **Kinds**: `python`, `sql`, `tests`, `read` (`snippet.py` with What if changes, no typing of outputs), `triage` (accept or reject proposed changes), `explain`, `open`, `prompt`, `quiz`.
- **Python options**: `name_bug` (needs `bug.md`), `plan_required` (comment lines before code), `grade_prompts` (the prompts to the assistant must pass the prompt review).
- **Documentation**: `docs.md` in an exercise is shown in a box on the exercise page and in mock rounds. A documentation task ships a helper module through `files:` and can only be solved by reading it.
- **Mock round**: two Python tasks with `mock: true`, 35 minutes, the assistant on and the docs open, code on the left; then the interviewer asks about two of your lines and three follow-ups with your code still on screen. Score: tests 35, review 25, time 10, small asks 10, ran code before accepting it 10, line explanations 10. Readiness is the average of the last three rounds.
- **Written answers are an exchange with an AI interviewer** (`gym/interview.py`): one question at a time, a short answer, at most one follow-up aimed at the gap, a hint (caps the question at partial) and skip (counts as missed). Verdicts are good, partial or missed; nothing missed passes. It covers readings, open, explain and prompt-writing exercises, naming the bug, the two lines of a level 3 build, and the follow-ups of a mock round. Accept-or-reject exercises are scored on the decisions, with the reasons shown after. The 1 to 5 reviewer (Gemini or Groq, settings menu; `min_score` 3) remains only for grading the prompts typed to the assistant and for the code review in a mock round.
- **Flashcards** ask "what does this do" and "what breaks here"; the daily deck uses the required steps.

## Content format

`content/<step>/step.yaml` (title, order, intro, gate, optional `optional: true`, `sequence`), `lessons/*.md` (four parts: what it is, how it breaks in production, the defence in code, what to say), `cards.yaml`, `exercises/<id>/` (`exercise.yaml`, `prompt.md`, `starter.*`, `solution.*`, `hint.md`, `guide.md`, `say.md`, `tests/test_hidden.py`, `wrong/`, and the optional files above). Exercise ids are global. `content/_kb` is the reference library (139 articles), `content/_shared` the delivery dataset used by SQL and pandas exercises.

## Checks

`uv run python -m gym.check_content` runs every reference solution against its tests, every wrong solution against the tests, the control checks, the readings and the curriculum rules (about 15 minutes). `uv run python -m tools.check_ids <ids | step:<folder> | kb>` does it for part of the content. `uv run pytest` tests the app.
