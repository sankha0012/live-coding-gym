# Graph Report - live-coding-gym  (2026-11-14)

## Corpus Check
- 372 files · ~132,153 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 918 nodes · 1053 edges · 323 communities (297 shown, 26 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.6)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4d5d53f1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- db.py
- runner.py
- load_content
- prod-debug/tests/test_hidden.py
- app.js
- app.py
- File Structure
- reviewer.py
- Live Coding Gym: design spec
- prod-monitor/tests/test_hidden.py
- Live Coding Gym: working rules
- py-merge/tests/test_hidden.py
- Live Coding Gym
- count_words
- py-session/tests/test_hidden.py
- prod-split/tests/test_hidden.py
- prod-debug/starter.py
- fixtures/content/01-hand-python/lessons/01-counting.md
- ai-chunk/tests/test_hidden.py
- ai-json/tests/test_hidden.py
- make_delivery_data.py
- live-coding-gym
- Authoring protocol (applies to Tasks 8 to 19)
- py-assign/tests/test_hidden.py
- py-second/tests/test_hidden.py
- py-topk/tests/test_hidden.py
- py-window/tests/test_hidden.py
- ai-retry/tests/test_hidden.py
- prod-events/tests/test_hidden.py
- prod-validate/tests/test_hidden.py
- dbg-avg/tests/test_hidden.py
- st-auc/tests/test_hidden.py
- ai-prf/tests/test_hidden.py
- ai-psi/tests/test_hidden.py
- ai-topk/tests/test_hidden.py
- ai-trim/tests/test_hidden.py
- extract_old_gym.js
- py-avg/tests/test_hidden.py
- py-city/tests/test_hidden.py
- py-latest/tests/test_hidden.py
- py-newret/tests/test_hidden.py
- prod-batch/tests/test_hidden.py
- prod-breaker/tests/test_hidden.py
- dbg-late/tests/test_hidden.py
- dbg-tags/tests/test_hidden.py
- st-boot/tests/test_hidden.py
- st-ks/tests/test_hidden.py
- st-z/tests/test_hidden.py
- ai-eval/tests/test_hidden.py
- CircuitBreaker
- CircuitBreaker
- dbg-tags/starter.py
- st-meanstd/tests/test_hidden.py
- test_io
- test_io
- test_io
- test_io
- test_io
- test_io
- test_io
- test_io
- 02-coderbyte.md
- average_delivery_minutes
- 04-python.md
- 01-routine.md
- 07-patterns.md
- 06-sql.md
- 03-robust.md
- 05-pandas.md
- 08-traps.md
- 09-stats.md
- 10-ai.md
- 11-senior.md
- 12-phrases.md

## God Nodes (most connected - your core abstractions)
1. `load_content()` - 16 edges
2. `Authoring protocol (applies to Tasks 8 to 19)` - 14 edges
3. `check()` - 13 edges
4. `run_python_tests()` - 13 edges
5. `h()` - 13 edges
6. `exView()` - 13 edges
7. `check_sql()` - 12 edges
8. `run_test_writing()` - 12 edges
9. `File Structure` - 12 edges
10. `create_app()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `build_rows()` --calls--> `pick()`  [INFERRED]
  tools/make_delivery_data.py → gym/mock.py
- `test_migrate_does_not_overwrite_existing_work()` --calls--> `migrate()`  [INFERRED]
  tests/test_migrate.py → tools/migrate_old_gym.py
- `test_box_is_capped_at_five()` --calls--> `record()`  [EXTRACTED]
  tests/test_cards.py → gym/cards.py
- `test_correct_answers_climb_boxes()` --calls--> `record()`  [EXTRACTED]
  tests/test_cards.py → gym/cards.py
- `test_duplicate_exercise_id_is_reported()` --calls--> `check()`  [EXTRACTED]
  tests/test_check_content.py → gym/check_content.py

## Import Cycles
- None detected.

## Communities (323 total, 26 thin omitted)

### Community 0 - "db.py"
Cohesion: 0.09
Nodes (41): create_mock(), finished_mocks(), get_attempt(), get_mock(), get_review(), _insert(), latest_review(), passed_attempts() (+33 more)

### Community 1 - "runner.py"
Cohesion: 0.08
Nodes (44): check(), check_exercise(), check_sql(), _pytest(), _query(), Run hidden pytest tests against a submission saved as solution.py., Run code as a script with no tests, like the Run button on Coderbyte., Run pytest on test_candidate.py in a temp dir holding `files` (name -> text). (+36 more)

### Community 2 - "load_content"
Cohesion: 0.09
Nodes (30): Exercise, _existing(), load_content(), load_exercise(), _read(), Step, connect(), conn() (+22 more)

### Community 3 - "prod-debug/tests/test_hidden.py"
Cohesion: 0.47
Nodes (10): _close(), _ns(), test_check_1(), test_check_2(), test_check_3(), test_check_4(), test_check_5(), test_check_6() (+2 more)

### Community 4 - "app.js"
Cohesion: 0.31
Nodes (20): api(), cardsView(), editor(), extrasPanel(), exView(), fmt(), h(), journeyView() (+12 more)

### Community 5 - "app.py"
Cohesion: 0.07
Nodes (35): BaseModel, CardBody, create_app(), main(), MockAnswers, MockSubmit, QuizBody, ReviewBody (+27 more)

### Community 6 - "File Structure"
Cohesion: 0.12
Nodes (15): After this plan, File Structure, Global Constraints, Live Coding Gym App Implementation Plan, Task 10: Web page, Task 11: Content checker and run instructions, Task 1: Project skeleton, config and content loader, Task 2: Python runner (+7 more)

### Community 7 - "reviewer.py"
Cohesion: 0.22
Nodes (13): build_prompt(), followups(), _material(), parse_review(), review(), test_default_rubric_used_when_none_given(), test_done_review_maps_scores_to_criteria(), test_followups_falls_back_when_gemini_fails() (+5 more)

### Community 8 - "Live Coding Gym: design spec"
Cohesion: 0.15
Nodes (12): 1. Purpose, 2. Scope decisions, 3. Architecture, 4. The journey, 5. Content format, 6. Error handling, 7. Testing, 8. Build order (+4 more)

### Community 9 - "prod-monitor/tests/test_hidden.py"
Cohesion: 0.56
Nodes (8): _close(), _ns(), test_check_1(), test_check_2(), test_check_3(), test_check_4(), test_check_5(), test_check_6()

### Community 10 - "Live Coding Gym: working rules"
Cohesion: 0.33
Nodes (5): Keeping the graph current, Live Coding Gym: working rules, Mandatory workflow tools, Project rules, Token habits

### Community 11 - "py-merge/tests/test_hidden.py"
Cohesion: 0.67
Nodes (6): _close(), _ns(), test_check_1(), test_check_2(), test_check_3(), test_check_4()

### Community 12 - "Live Coding Gym"
Cohesion: 0.33
Nodes (5): Adding content, Live Coding Gym, Run, Setup, Tests

### Community 13 - "count_words"
Cohesion: 0.53
Nodes (4): count_words(), test_basic(), test_empty(), test_mixed_case()

### Community 14 - "py-session/tests/test_hidden.py"
Cohesion: 0.67
Nodes (6): _close(), _ns(), test_check_1(), test_check_2(), test_check_3(), test_check_4()

### Community 15 - "prod-split/tests/test_hidden.py"
Cohesion: 0.67
Nodes (6): _close(), _ns(), test_check_1(), test_check_2(), test_check_3(), test_check_4()

### Community 16 - "prod-debug/starter.py"
Cohesion: 0.29
Nodes (6): mean_score(), normalize(), Average of the scores, ignoring None. Empty or all-None -> None., The k feature names with the largest absolute weight; ties broken by name., Scale 'amount' to [0, 1] within the batch. Must NOT modify the input. If all…, top_features()

### Community 20 - "ai-chunk/tests/test_hidden.py"
Cohesion: 0.67
Nodes (6): _close(), _ns(), test_check_1(), test_check_2(), test_check_3(), test_check_4()

### Community 21 - "ai-json/tests/test_hidden.py"
Cohesion: 0.67
Nodes (6): _close(), _ns(), test_check_1(), test_check_2(), test_check_3(), test_check_4()

### Community 22 - "make_delivery_data.py"
Cohesion: 0.43
Nodes (5): test_dataset_shape_and_determinism(), build_rows(), generate(), Generate the shared food-delivery dataset used by SQL and pandas exercises.…, sql_value()

### Community 28 - "Authoring protocol (applies to Tasks 8 to 19)"
Cohesion: 0.06
Nodes (30): Authoring protocol (applies to Tasks 8 to 19), File Structure, Global Constraints, Journey (fixed folder names and gates), Live Coding Gym Content Implementation Plan, Part 1: App extensions, Part 2: Shared dataset and migration, Part 3: Authoring (+22 more)

### Community 29 - "py-assign/tests/test_hidden.py"
Cohesion: 0.73
Nodes (5): _close(), _ns(), test_check_1(), test_check_2(), test_check_3()

### Community 30 - "py-second/tests/test_hidden.py"
Cohesion: 0.73
Nodes (5): _close(), _ns(), test_check_1(), test_check_2(), test_check_3()

### Community 32 - "py-topk/tests/test_hidden.py"
Cohesion: 0.73
Nodes (5): _close(), _ns(), test_check_1(), test_check_2(), test_check_3()

### Community 33 - "py-window/tests/test_hidden.py"
Cohesion: 0.73
Nodes (5): _close(), _ns(), test_check_1(), test_check_2(), test_check_3()

### Community 34 - "ai-retry/tests/test_hidden.py"
Cohesion: 0.73
Nodes (5): _close(), _ns(), test_check_1(), test_check_2(), test_check_3()

### Community 35 - "prod-events/tests/test_hidden.py"
Cohesion: 0.73
Nodes (5): _close(), _ns(), test_check_1(), test_check_2(), test_check_3()

### Community 36 - "prod-validate/tests/test_hidden.py"
Cohesion: 0.73
Nodes (5): _close(), _ns(), test_check_1(), test_check_2(), test_check_3()

### Community 42 - "dbg-avg/tests/test_hidden.py"
Cohesion: 0.73
Nodes (5): _close(), _ns(), test_check_1(), test_check_2(), test_check_3()

### Community 43 - "st-auc/tests/test_hidden.py"
Cohesion: 0.73
Nodes (5): _close(), _ns(), test_check_1(), test_check_2(), test_check_3()

### Community 44 - "ai-prf/tests/test_hidden.py"
Cohesion: 0.73
Nodes (5): _close(), _ns(), test_check_1(), test_check_2(), test_check_3()

### Community 45 - "ai-psi/tests/test_hidden.py"
Cohesion: 0.73
Nodes (5): _close(), _ns(), test_check_1(), test_check_2(), test_check_3()

### Community 46 - "ai-topk/tests/test_hidden.py"
Cohesion: 0.73
Nodes (5): _close(), _ns(), test_check_1(), test_check_2(), test_check_3()

### Community 47 - "ai-trim/tests/test_hidden.py"
Cohesion: 0.73
Nodes (5): _close(), _ns(), test_check_1(), test_check_2(), test_check_3()

### Community 48 - "extract_old_gym.js"
Cohesion: 0.33
Nodes (4): code, fs, html, out

### Community 49 - "py-avg/tests/test_hidden.py"
Cohesion: 0.80
Nodes (4): _close(), _ns(), test_check_1(), test_check_2()

### Community 50 - "py-city/tests/test_hidden.py"
Cohesion: 0.80
Nodes (4): _close(), _ns(), test_check_1(), test_check_2()

### Community 51 - "py-latest/tests/test_hidden.py"
Cohesion: 0.80
Nodes (4): _close(), _ns(), test_check_1(), test_check_2()

### Community 52 - "py-newret/tests/test_hidden.py"
Cohesion: 0.80
Nodes (4): _close(), _ns(), test_check_1(), test_check_2()

### Community 53 - "prod-batch/tests/test_hidden.py"
Cohesion: 0.80
Nodes (4): _close(), _ns(), test_check_1(), test_check_2()

### Community 54 - "prod-breaker/tests/test_hidden.py"
Cohesion: 0.80
Nodes (4): _close(), _ns(), test_check_1(), test_check_2()

### Community 55 - "dbg-late/tests/test_hidden.py"
Cohesion: 0.80
Nodes (4): _close(), _ns(), test_check_1(), test_check_2()

### Community 56 - "dbg-tags/tests/test_hidden.py"
Cohesion: 0.80
Nodes (4): _close(), _ns(), test_check_1(), test_check_2()

### Community 57 - "st-boot/tests/test_hidden.py"
Cohesion: 0.80
Nodes (4): _close(), _ns(), test_check_1(), test_check_2()

### Community 58 - "st-ks/tests/test_hidden.py"
Cohesion: 0.80
Nodes (4): _close(), _ns(), test_check_1(), test_check_2()

### Community 59 - "st-z/tests/test_hidden.py"
Cohesion: 0.80
Nodes (4): _close(), _ns(), test_check_1(), test_check_2()

### Community 60 - "ai-eval/tests/test_hidden.py"
Cohesion: 0.80
Nodes (4): _close(), _ns(), test_check_1(), test_check_2()

### Community 64 - "st-meanstd/tests/test_hidden.py"
Cohesion: 0.83
Nodes (3): _close(), _ns(), test_check_1()

## Knowledge Gaps
- **76 isolated node(s):** `live-coding-gym`, `fs`, `html`, `code`, `out` (+71 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **26 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_content()` connect `load_content` to `runner.py`, `app.py`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **Why does `pick()` connect `db.py` to `make_delivery_data.py`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **Why does `build_rows()` connect `make_delivery_data.py` to `db.py`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **What connects `live-coding-gym`, `fs`, `html` to the rest of the system?**
  _76 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `db.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09042553191489362 - nodes in this community are weakly interconnected._
- **Should `runner.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08326530612244898 - nodes in this community are weakly interconnected._
- **Should `load_content` be split into smaller, more focused modules?**
  _Cohesion score 0.09358974358974359 - nodes in this community are weakly interconnected._