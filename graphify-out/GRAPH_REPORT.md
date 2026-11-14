# Graph Report - live-coding-gym  (2026-11-14)

## Corpus Check
- 51 files · ~39,626 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 243 nodes · 418 edges · 28 communities (25 shown, 3 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3320bc0a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- db.py
- check_sql
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

## God Nodes (most connected - your core abstractions)
1. `load_content()` - 12 edges
2. `check_sql()` - 12 edges
3. `File Structure` - 12 edges
4. `h()` - 11 edges
5. `exView()` - 11 edges
6. `run_python_tests()` - 10 edges
7. `Live Coding Gym: design spec` - 10 edges
8. `exercise_status()` - 9 edges
9. `review()` - 9 edges
10. `mockView()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `test_box_is_capped_at_five()` --calls--> `record()`  [EXTRACTED]
  tests/test_cards.py → gym/cards.py
- `test_correct_answers_climb_boxes()` --calls--> `record()`  [EXTRACTED]
  tests/test_cards.py → gym/cards.py
- `test_sample_content_is_clean()` --calls--> `check()`  [EXTRACTED]
  tests/test_check_content.py → gym/check_content.py
- `test_starter_that_already_passes_is_reported()` --calls--> `check()`  [EXTRACTED]
  tests/test_check_content.py → gym/check_content.py
- `test_wrong_reference_solution_is_reported()` --calls--> `check()`  [EXTRACTED]
  tests/test_check_content.py → gym/check_content.py

## Import Cycles
- None detected.

## Communities (28 total, 3 thin omitted)

### Community 0 - "db.py"
Cohesion: 0.11
Nodes (35): create_mock(), finished_mocks(), get_attempt(), get_mock(), get_review(), _insert(), latest_review(), passed_attempts() (+27 more)

### Community 1 - "check_sql"
Cohesion: 0.16
Nodes (22): check_sql(), _query(), Run hidden pytest tests against a submission saved as solution.py., Run code as a script with no tests, like the Run button on Coderbyte., run_python_free(), run_python_tests(), run_sql_free(), RunResult (+14 more)

### Community 2 - "load_content"
Cohesion: 0.15
Nodes (14): check(), Exercise, load_content(), load_exercise(), _read(), Step, connect(), conn() (+6 more)

### Community 3 - "app.py"
Cohesion: 0.14
Nodes (17): BaseModel, CardBody, main(), MockAnswers, MockSubmit, ReviewBody, RunBody, SubmitBody (+9 more)

### Community 4 - "app.js"
Cohesion: 0.33
Nodes (18): api(), cardsView(), editor(), exView(), fmt(), h(), journeyView(), main (+10 more)

### Community 5 - "test_app.py"
Cohesion: 0.19
Nodes (12): create_app(), client(), fake_gemini(), post(), fixture, test_cards_and_unlock(), test_failed_submission_is_recorded_but_not_passed(), test_full_step_flow_passes_gate_and_unlocks_next() (+4 more)

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

## Knowledge Gaps
- **35 isolated node(s):** `live-coding-gym`, `main`, `Mandatory workflow tools`, `Keeping the graph current`, `Token habits` (+30 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_content()` connect `load_content` to `app.py`, `test_app.py`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `run_python_tests()` connect `check_sql` to `load_content`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **What connects `live-coding-gym`, `main`, `Mandatory workflow tools` to the rest of the system?**
  _35 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `db.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11470985155195682 - nodes in this community are weakly interconnected._
- **Should `app.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._
- **Should `File Structure` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._