# Live Coding Gym

A local app for preparing live-coding interviews on software engineering for production ML systems, where an AI assistant is allowed and the candidate must understand and explain every line. It trains control over the assistant, not typing from memory. Design and file formats: `docs/design.md`.

## Quick start

```bash
git clone git@github.com:sankha0012/live-coding-gym.git && cd live-coding-gym
cp .env.example .env        # add GEMINI_API_KEY and/or GROQ_API_KEY
uv sync                     # Python 3.12, installs everything including scikit-learn
uv run python -m gym.app    # http://localhost:8000
```

Progress is stored in `data/progress.db` (git-ignored). Delete it, or use "Reset all progress" on the track page, to start over. The AI provider (Gemini or Groq) is chosen in the top bar. The nav label shows the git commit that is running.

## What is in it

- Ten steps in `content/`: read Python, the control loop on Coderbyte, catching the assistant's mistakes, robust code, real data behaviour, model failures, ML systems in production, explain and defend, mock rounds, and an optional SQL step. 359 exercises, 139 reference articles, flashcards.
- **What if**: the app changes one line of code and you say what happens; it runs the change to know. Levels 1 to 3 decide how much evaluation each reading or build carries.
- **An AI interviewer** for written answers: one question at a time, one follow-up, hint and skip.
- **Assistant policies** per exercise (train, explain, off, free), a **control check** after core builds, **mock rounds** with documentation and an assistant, **Dev mode** (Dev button: everything open and revealed, no progress shown).
- Layout: code on the left, task, questions, help and assistant on the right.

## Commands

```bash
uv run pytest                              # app tests (about 30 s)
uv run python -m gym.check_content         # runs every solution, wrong solution, What if change and rule (about 25 min)
uv run python -m tools.check_ids <ids>     # the same for some exercises, or step:<folder>, or kb (seconds)
```

Run `check_content` after any content change. No exercise ships if its own solution fails its own tests. Restart the server to load new content.

## Adding or changing content

Everything the learner sees lives in `content/` as plain files; app code never contains lesson or exercise text. The folder layout and every `exercise.yaml` option are in `docs/design.md` ("Content format"). Reference articles: `content/_kb/<id>.md`, listed in `docs/kb-topics.md`.

## Project rules for contributors

`CLAUDE.md` holds the working rules (least code, tests first, keep the graph current with `graphify update .`, never commit keys). The code map is in `graphify-out/`.

## Deploy on Vercel

Ready to import (`vercel.json`, `api/index.py`); not yet tried on a real Vercel build. Set `GEMINI_API_KEY` and/or `GROQ_API_KEY`, `GYM_PASSWORD` (HTTP Basic login, any user name; required because the site runs code), and optionally `GYM_DEV=1`. Limits: progress lives in `/tmp` and is lost on restarts (use dev mode); scikit-learn exercises do not run (the build leaves it out for Vercel's 250 MB limit); 60 s per run.

## Known limits and ideas

- The SQL graph and some doc files are not in the graphify graph (`uv pip install "graphifyy[sql]"` to add SQL).
- The step-through idea (pause a run and ask for a value) was not built.
- Flashcards still use the type-then-flip screen; quizzes are unchanged.
- Optional `uv sync --group tools` installs MLflow and the Prometheus client, used only to check the tools-lesson examples.
