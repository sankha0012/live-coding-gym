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

Content lives in `content/<step>/`. See `docs/design.md` for the design and the file format. After adding or changing an exercise:

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

## Design

See `docs/design.md`: ten steps, the four moves (read, build, catch, defend), the assistant policies, the control check and the mock round.
