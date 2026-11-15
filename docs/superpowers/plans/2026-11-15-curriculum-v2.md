# Curriculum v2: implementation plan

Design: "Live coding gym: curriculum design v2" (artifact `NnTx8NJaBmKSCTySMcRAVZ`). Status: **awaiting the user's approval. Do not start before it.**

User decisions (2026-11-15): keep SQL and fit it into the new scheme; keep pandas; delete the Library and all legacy code; keep every exercise; plan first, then ask permission.

## Target state

Ten step folders under `content/`, no Library, no `shelf`, no `includes`. Every existing exercise lives in exactly one step. `required: true` marks the core path (counts toward the gate); `required: false` marks extra practice.

| Folder | Step | Exercises moved in | New content |
|---|---|---|---|
| `s01-read-python` | Read Python fluently | 12 `rd-*` | 6 readings of pandas and scikit-learn code |
| `s02-control-loop` | The control loop on Coderbyte | 20 `cb-*`/`rt-*`, 40 `py1-*`/`py-*` (extra), 10 `pa-*`, 4 `ai-chunk/json/topk/trim` | 4 documentation tasks; lessons merged from old steps 2 and 10 |
| `s03-catch-mistakes` | Catch the assistant's mistakes | 6 `va-*`, 2 `tg-*` | none |
| `s04-robust-code` | Deterministic and robust code | 20 from old step 4, 13 from old step 5 | 8 readings, 4 catch, 3 defend |
| `s05-real-data` | Real data behaviour | 24 Python and quiz from old step 6 (pandas kept) | 8 readings, 4 catch, 3 defend |
| `s06-model-failures` | Common model failures | 15 from old step 9, `ai-eval`, `ai-prf`, `ai-psi` | 8 readings, 4 catch, 3 defend |
| `s07-production-ml` | ML systems in production | 17 from old step 8, 18 from old step 7 | 8 readings, 4 catch, 3 defend |
| `s08-explain-defend` | Explain and defend | 16 from old step 11 | lessons merged from old step 11 |
| `s09-mock-rounds` | Mock rounds | none | lessons from old step 12; new task pool |
| `s10-sql` | SQL for data work (optional step) | 46 from old step 3, 6 `dq-*` | 8 readings (explain a query), 6 catch, 3 defend |

Step 10 is `optional: true`: always open, never blocks another step, not needed for readiness. It is the only use of an optional flag.

## Phases

Each phase ends with `uv run pytest`, the relevant `tools.check_ids` runs, `graphify update .`, and one commit. The full `gym.check_content` runs at the end of phases 2, 5 and 7.

### Phase 1: app model (code, test first)

1. `step.yaml`: replace `shelf` and `includes` with `optional`. Keep `sequence` and `intro`. Delete the include-moving code in `gym/content.py` and the Library branches in `gym/gates.py`, `gym/app.py`, `web/app.js`.
2. `exercise.yaml`: add `serves: [C1..C10]` (competency tags, shown as badges) and optional `docs.md` (a documentation page shown in a collapsible box and in mock rounds).
3. Step page groups exercises into Read, Build, Catch, Defend (derived from kind and `name_bug`), and splits core from extra practice.
4. SQL in the four moves: control check for SQL (`change.md` plus `change_solution.sql`; part B compares the learner's changed query with it on the seed data), `name_bug` for SQL, and explain-kind readings that show a query with its tables.
5. `gym/check_content.py`: every exercise has `serves`; every core build has a control check; SQL change rules (the unchanged solution must not match `change_solution.sql`).
6. Tests for all of the above in `tests/test_redesign.py`; fixtures updated.

### Phase 2: move every exercise (no content edits)

A script moves exercise folders into the ten step folders with `git mv`, writes each `step.yaml` (title, order, intro, sequence), merges lessons and cards, and deletes the twelve old step folders and the six `t*` folders. Check: the count of exercise ids before and after is identical, and `gym.check_content` passes.

### Phase 3: steps 5 and 6 (the biggest gap)

For each concept in the design: a lesson in the four-part form (what it is, how it breaks, the defence in code, what to say), a reading built from an existing reference solution, control-check files on the core builds, catch exercises built from existing `wrong/` solutions, defend questions, `serves` tags, and flashcards rewritten as "what does this do" and "what breaks here". Authored by a workflow of agents with one independent reviewer per batch, gated by `tools.check_ids`.

### Phase 4: steps 4 and 7

Same recipe. Old step 5 (testing) becomes the "prove it with tests" concept in step 4. Old step 7 (tools) becomes talking-point lessons and cards, a quiz, and scikit-learn readings in step 7.

### Phase 5: steps 1, 2, 8 and 10

Six pandas and scikit-learn readings (step 1). Four documentation tasks and merged lessons (step 2); the 40 hand-coding drills become extra practice with the `train` assistant. Merged lessons (step 8). SQL step: readings, catch exercises, control checks on 12 core queries, defend questions.

### Phase 6: mock rounds

`mock: true` moves from the algorithm puzzles to about 24 tasks in steps 4 to 7, each with a `docs.md`. The mock page shows the documentation box. Strategy lessons move to step 9.

### Phase 7: delete legacy code

Remove: `live-coding-gym.html`, `tools/extract_old_gym.js`, `tools/migrate_old_gym.py`, `tools/old_gym.json`, `tests/test_migrate.py`, all `gaps.*` files (34) and the `gaps` field, `time_limit_s` and the `timed` gate, the `timed_required` step option, superseded plan and spec files in `docs/superpowers/` (replaced by one current design note), and any function a `ponytail-audit` pass shows is unused. Update `README.md`, `CLAUDE.md`, `docs/kb-topics.md` and the project memory. Final full check, browser pass on the scratch server (port 8001, scratch database), push.

## Defaults I chose (say so if you want otherwise)

- Control checks are written for core builds only (about 80 exercises: 22 exist). Extra-practice builds keep the explain-it-back rule.
- Core is about 80 exercises across steps 1 to 8; everything else is extra practice in the same step.
- SQL is step 10 and optional, because the iFood email does not ask for it.
- Your progress database is reset-compatible but old progress on moved exercises is kept, since exercise ids do not change.

## Size

87 new exercises (readings, catch, defend, documentation tasks), about 60 new control checks, about 45 rewritten lessons, about 300 flashcards revised. Phases 3 to 5 are the bulk and run as parallel author-and-review batches.
