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

## AI assistant

The right-hand sidebar has an Assistant tab on every exercise (not quizzes) and in mock rounds. Tutor mode (the only mode in steps 1 to 3, and for answer-writing exercises) explains and hints but never writes the solution. Interview mode behaves like the real interview's assistant. If it writes code for an exercise, that exercise only counts after you explain the code and pass the AI review. The assistant never sees the reference solution or the hidden tests.
