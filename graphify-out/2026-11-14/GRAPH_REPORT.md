# Graph Report - live-coding-gym  (2026-11-14)

## Corpus Check
- 67 files · ~53,697 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 329 nodes · 537 edges · 42 communities (39 shown, 3 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a569a923`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- db.py
- runner.py
- load_content
- app.py
- app.js
- test_app.py
- File Structure
- reviewer.py
- Live Coding Gym: design spec
- test_cards.py
- Live Coding Gym: working rules
- count_words
- Live Coding Gym
- count_words
- content/01-hand-python/lessons/01-counting.md
- fixtures/content/01-hand-python/lessons/01-counting.md
- live-coding-gym
- Authoring protocol (applies to Tasks 8 to 19)
- test_content_extras.py

## God Nodes (most connected - your core abstractions)
1. `load_content()` - 14 edges
2. `Authoring protocol (applies to Tasks 8 to 19)` - 14 edges
3. `run_python_tests()` - 13 edges
4. `h()` - 13 edges
5. `exView()` - 13 edges
6. `check_sql()` - 12 edges
7. `run_test_writing()` - 12 edges
8. `File Structure` - 12 edges
9. `check()` - 11 edges
10. `create_app()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `test_box_is_capped_at_five()` --calls--> `record()`  [EXTRACTED]
  tests/test_cards.py → gym/cards.py
- `test_correct_answers_climb_boxes()` --calls--> `record()`  [EXTRACTED]
  tests/test_cards.py → gym/cards.py
- `test_duplicate_exercise_id_is_reported()` --calls--> `check()`  [EXTRACTED]
  tests/test_check_content.py → gym/check_content.py
- `test_missing_say_and_hint_are_reported()` --calls--> `check()`  [EXTRACTED]
  tests/test_check_content.py → gym/check_content.py
- `test_sample_content_is_clean()` --calls--> `check()`  [EXTRACTED]
  tests/test_check_content.py → gym/check_content.py

## Import Cycles
- None detected.

## Communities (42 total, 3 thin omitted)

### Community 0 - "db.py"
Cohesion: 0.11
Nodes (35): create_mock(), finished_mocks(), get_attempt(), get_mock(), get_review(), _insert(), latest_review(), passed_attempts() (+27 more)

### Community 1 - "runner.py"
Cohesion: 0.10
Nodes (35): check_sql(), _pytest(), _query(), Run hidden pytest tests against a submission saved as solution.py., Run code as a script with no tests, like the Run button on Coderbyte., Run pytest on test_candidate.py in a temp dir holding `files` (name -> text)., Run hidden pytest tests against a submission saved as solution.py., Grade a learner's test file: it must pass on `good` and fail on every `bads`… (+27 more)

### Community 2 - "load_content"
Cohesion: 0.13
Nodes (20): check(), check_exercise(), Exercise, _existing(), load_content(), load_exercise(), _read(), Step (+12 more)

### Community 3 - "app.py"
Cohesion: 0.14
Nodes (18): BaseModel, CardBody, main(), MockAnswers, MockSubmit, QuizBody, ReviewBody, RunBody (+10 more)

### Community 4 - "app.js"
Cohesion: 0.31
Nodes (20): api(), cardsView(), editor(), extrasPanel(), exView(), fmt(), h(), journeyView() (+12 more)

### Community 5 - "test_app.py"
Cohesion: 0.12
Nodes (16): create_app(), client(), fake_gemini(), client(), fake_gemini(), fixture, test_sql_schema_hides_insert_lines(), post() (+8 more)

### Community 6 - "File Structure"
Cohesion: 0.12
Nodes (15): After this plan, File Structure, Global Constraints, Live Coding Gym App Implementation Plan, Task 10: Web page, Task 11: Content checker and run instructions, Task 1: Project skeleton, config and content loader, Task 2: Python runner (+7 more)

### Community 7 - "reviewer.py"
Cohesion: 0.22
Nodes (13): build_prompt(), followups(), _material(), parse_review(), review(), test_default_rubric_used_when_none_given(), test_done_review_maps_scores_to_criteria(), test_followups_falls_back_when_gemini_fails() (+5 more)

### Community 8 - "Live Coding Gym: design spec"
Cohesion: 0.15
Nodes (12): 1. Purpose, 2. Scope decisions, 3. Architecture, 4. The journey, 5. Content format, 6. Error handling, 7. Testing, 8. Build order (+4 more)

### Community 9 - "test_cards.py"
Cohesion: 0.42
Nodes (7): due(), record(), test_box_is_capped_at_five(), test_card_returns_on_its_due_date(), test_correct_answers_climb_boxes(), test_unseen_cards_are_due(), test_wrong_answer_resets_and_stays_due()

### Community 10 - "Live Coding Gym: working rules"
Cohesion: 0.33
Nodes (5): Keeping the graph current, Live Coding Gym: working rules, Mandatory workflow tools, Project rules, Token habits

### Community 11 - "count_words"
Cohesion: 0.53
Nodes (4): count_words(), test_basic(), test_empty(), test_mixed_case()

### Community 12 - "Live Coding Gym"
Cohesion: 0.33
Nodes (5): Adding content, Live Coding Gym, Run, Setup, Tests

### Community 13 - "count_words"
Cohesion: 0.53
Nodes (4): count_words(), test_basic(), test_empty(), test_mixed_case()

### Community 28 - "Authoring protocol (applies to Tasks 8 to 19)"
Cohesion: 0.06
Nodes (30): Authoring protocol (applies to Tasks 8 to 19), File Structure, Global Constraints, Journey (fixed folder names and gates), Live Coding Gym Content Implementation Plan, Part 1: App extensions, Part 2: Shared dataset and migration, Part 3: Authoring (+22 more)

### Community 29 - "test_content_extras.py"
Cohesion: 0.50
Nodes (8): build(), load_one(), One step with one exercise 'e1'. files maps path-under-exercise -> text., test_extras_and_wrong_solutions(), test_files_are_resolved_and_must_exist(), test_quiz_loads_and_rejects_bad_answer_index(), test_sql_seed_file(), test_tests_kind_needs_good_and_bad_implementations()

## Knowledge Gaps
- **60 isolated node(s):** `live-coding-gym`, `main`, `Mandatory workflow tools`, `Keeping the graph current`, `Token habits` (+55 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_content()` connect `load_content` to `test_content_extras.py`, `app.py`, `test_app.py`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Why does `create_app()` connect `test_app.py` to `load_content`, `app.py`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Why does `run_test_writing()` connect `runner.py` to `load_content`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **What connects `live-coding-gym`, `main`, `Mandatory workflow tools` to the rest of the system?**
  _60 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `db.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11470985155195682 - nodes in this community are weakly interconnected._
- **Should `runner.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10256410256410256 - nodes in this community are weakly interconnected._
- **Should `load_content` be split into smaller, more focused modules?**
  _Cohesion score 0.12561576354679804 - nodes in this community are weakly interconnected._