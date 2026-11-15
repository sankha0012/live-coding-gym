# Live Coding Gym

Local training app for live-coding interviews on production ML systems.

## Run

```bash
uv run python -m gym.app
```

Open http://localhost:8000.

## Setup

`.env` in this folder holds `GEMINI_API_KEY` and `GEMINI_MODEL`. It is not committed.

## Adding content

Content lives in `content/<step>/`. See `docs/superpowers/specs/2026-11-14-live-coding-gym-design.md`, section 5, for the format. After adding or changing an exercise:

```bash
uv run python -m gym.check_content
```

Restart the server to load new content.

## Tests

```bash
uv run pytest
```

Progress is stored in `data/progress.db`. Delete that file to start over.

## Knowledge base

Reference articles live in `content/_kb/<topic-id>.md` (front matter: title, summary, tags; the text before `<!-- more -->` is the brief shown in the Help sidebar). `docs/kb-topics.md` lists every topic. An exercise names its topics with `kb: [id, id]` in `exercise.yaml`. Check with:

```bash
uv run python -m tools.check_ids kb
```

## Optional tools

MLflow (slim package) and the Prometheus client are an optional dependency group, used only to check the examples in the ML tools lessons. Install them with `uv sync --group tools`. The app does not need them.

## AI provider

Reviews, prompt grading and mock-round questions can use Gemini or Groq. Put the keys in `.env` (`GEMINI_API_KEY`, `GROQ_API_KEY`, and optionally `GEMINI_MODEL`, `GROQ_MODEL`) and pick the provider in the top bar. The choice is remembered.

## Design: AI-assisted coding, in control

The track has six steps (read Python, the control loop, catching mistakes, robust ML systems, explain and defend, mock rounds). The twelve older steps live in the optional Library on the journey page.

- **One assistant, a policy per exercise** (`assistant:` in `exercise.yaml`): `train` (default for code: one small function per ask, big asks are sent back), `explain` (never writes code), `off`, `free` (mock rounds). Each reply carries a hidden small/large size mark that feeds the mock score. If it writes code, you must explain it to finish the exercise.
- **Control check** (`change.md`, `change_tests/`, `change_solution.py` in an exercise folder): after the tests pass, explain two random lines of your own code, then make one small change by hand while the assistant is locked.
- **Kinds**: `read` (predict the output of `snippet.py`, then explain), `triage` (accept or reject proposed changes), `python` with `name_bug`, `plan_required`, `grade_prompts`.
- **Step options**: `shelf`, `includes`, `sequence` in `step.yaml`.
- **Mock round**: two Python tasks with the assistant on, 35 minutes, then two "explain this line" questions and three follow-ups. Score: tests 35, review 25, time 10, small asks 10, ran-before-accepting 10, lines 10.
