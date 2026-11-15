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
