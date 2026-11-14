# Graph Report - live-coding-gym  (2026-11-14)

## Corpus Check
- 952 files · ~165,508 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2091 nodes · 2009 edges · 773 communities (729 shown, 44 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 30 edges (avg confidence: 0.72)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bfe72f7e`
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
- ____
- Counter
- LRUCache
- BankAccount
- Stack
- Dicts and sets
- fib
- Types and strings
- Functions
- Classes and dataclasses
- Errors, files, JSON and dates
- two_sum
- caesar
- chunks
- rotate
- word_count_top
- Lists and loops
- longest_unique
- merge_intervals
- Window functions
- Dialect notes: what changes outside SQLite
- Version
- py1-json-roundtrip/tests/test_hidden.py
- running_sum
- pairs
- first_unique
- is_valid_ip
- Joins explained
- test_cards.py
- common_keys
- compose
- compress_spaces
- count_vowels
- days_between
- group_by_length
- is_palindrome
- safe_int
- set_diff_report
- rank
- title_case
- anagram_groups
- first_index
- rotate
- top_k
- Clarifying questions
- Testing in 30 seconds
- When you are stuck
- GROUP BY and HAVING
- Subqueries and CTEs
- NULLs, dates and de-duplication
- apply_n_times
- Counter
- Counter
- Counter
- flatten
- invert_dict
- merge_dicts_sum
- parse_csv_line
- reverse_words
- Stack
- Stack
- Stack
- unique
- parse_logs
- roman_to_int
- BankAccount
- BankAccount
- BankAccount
- LRUCache
- LRUCache
- LRUCache
- LRUCache
- LRUCache
- py1-dataclass-order/starter.py
- field_order.py
- no_order.py
- not_frozen.py

## God Nodes (most connected - your core abstractions)
1. `load_content()` - 18 edges
2. `Authoring protocol (applies to Tasks 8 to 19)` - 14 edges
3. `check()` - 13 edges
4. `run_python_tests()` - 13 edges
5. `h()` - 13 edges
6. `exView()` - 13 edges
7. `LRUCache` - 12 edges
8. `check_sql()` - 12 edges
9. `run_test_writing()` - 12 edges
10. `File Structure` - 12 edges

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

## Communities (773 total, 44 thin omitted)

### Community 0 - "db.py"
Cohesion: 0.09
Nodes (41): create_mock(), finished_mocks(), get_attempt(), get_mock(), get_review(), _insert(), latest_review(), passed_attempts() (+33 more)

### Community 1 - "runner.py"
Cohesion: 0.10
Nodes (35): check_sql(), _pytest(), _query(), Run hidden pytest tests against a submission saved as solution.py., Run code as a script with no tests, like the Run button on Coderbyte., Run pytest on test_candidate.py in a temp dir holding `files` (name -> text)., Run hidden pytest tests against a submission saved as solution.py., Grade a learner's test file: it must pass on `good` and fail on every `bads`… (+27 more)

### Community 2 - "load_content"
Cohesion: 0.07
Nodes (41): check(), check_exercise(), Exercise, _existing(), load_content(), load_exercise(), _read(), Step (+33 more)

### Community 3 - "prod-debug/tests/test_hidden.py"
Cohesion: 0.47
Nodes (10): _close(), _ns(), test_check_1(), test_check_2(), test_check_3(), test_check_4(), test_check_5(), test_check_6() (+2 more)

### Community 4 - "app.js"
Cohesion: 0.31
Nodes (20): api(), cardsView(), editor(), extrasPanel(), exView(), fmt(), h(), journeyView() (+12 more)

### Community 5 - "app.py"
Cohesion: 0.08
Nodes (28): BaseModel, CardBody, create_app(), main(), MockAnswers, MockSubmit, QuizBody, ReviewBody (+20 more)

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

### Community 323 - "____"
Cohesion: 0.05
Nodes (19): ____, apply_n_times(), BankAccount, chunks(), common_keys(), count_vowels(), sort_versions(), Version (+11 more)

### Community 324 - "Counter"
Cohesion: 0.22
Nodes (6): Counter, test_add_and_count(), test_instances_are_separate(), test_missing_item_is_zero(), test_most_common_edges(), test_most_common_with_ties()

### Community 325 - "LRUCache"
Cohesion: 0.24
Nodes (8): LRUCache, test_capacity_one(), test_example(), test_falsy_values(), test_missing(), test_put_refreshes(), test_update_existing_no_evict(), test_update_newest_keeps_oldest()

### Community 326 - "BankAccount"
Cohesion: 0.24
Nodes (6): BankAccount, test_balance_read_only(), test_deposit_and_withdraw(), test_non_positive_amounts(), test_overdraft_raises_and_keeps_balance(), test_withdraw_whole_balance()

### Community 327 - "Stack"
Cohesion: 0.23
Nodes (5): Stack, test_empty_raises(), test_len_tracks_pushes_and_pops(), test_lifo(), test_peek_does_not_remove()

### Community 328 - "Dicts and sets"
Cohesion: 0.17
Nodes (11): Dicts and sets, Inverting a dict whose values repeat, Merging two dicts and summing values, Order, Say it like this, Sets, The problem it solves, The smallest runnable example (+3 more)

### Community 329 - "fib"
Cohesion: 0.27
Nodes (7): fib(), CountingDict, test_cache_is_filled_once(), test_default_cache_persists(), test_large_value(), test_small_values(), dict

### Community 330 - "Types and strings"
Cohesion: 0.18
Nodes (10): Characters and numbers, Checks to run in the live round, Say it like this, The problem it solves, The smallest runnable example, Trap 1: thinking a method changes the string, Trap 2: `split(" ")` versus `split()`, Trap 3: building strings in a loop with `+=` and using `str` as a name (+2 more)

### Community 331 - "Functions"
Cohesion: 0.18
Nodes (10): Functions, Return values, Say it like this, Small useful patterns, Sorting with a key, The problem it solves, The smallest runnable example, Trap 1: the mutable default argument (+2 more)

### Community 332 - "Classes and dataclasses"
Cohesion: 0.18
Nodes (10): A class with a rule: the bank account, Classes and dataclasses, Dataclasses, Say it like this, The problem it solves, The smallest runnable example, Trap 1: forgetting `self`, Trap 2: class attributes shared by all instances (+2 more)

### Community 333 - "Errors, files, JSON and dates"
Cohesion: 0.18
Nodes (10): Dates, Errors, files, JSON and dates, Files, Say it like this, The problem it solves, The smallest runnable example, Trap 1: the bare except, Trap 2: JSON does not round-trip everything (+2 more)

### Community 334 - "two_sum"
Cohesion: 0.33
Nodes (9): two_sum(), test_basic(), test_duplicates_and_negatives(), test_empty(), test_not_found(), test_same_position_not_twice(), test_smallest_j(), test_smallest_j_beats_smallest_i() (+1 more)

### Community 335 - "caesar"
Cohesion: 0.36
Nodes (8): caesar(), test_accented_unchanged(), test_basic(), test_big_shift(), test_keeps_other_chars(), test_negative(), test_upper_wrap_and_big_negative(), test_zero_and_empty()

### Community 336 - "chunks"
Cohesion: 0.33
Nodes (8): chunks(), parametrize, test_bad_n(), test_bad_n_with_empty_list(), test_basic(), test_empty(), test_exact_fit(), test_n_bigger_than_list()

### Community 337 - "rotate"
Cohesion: 0.36
Nodes (8): rotate(), test_basic(), test_empty(), test_input_unchanged(), test_k_larger_than_length(), test_negative(), test_negative_wraps(), test_zero()

### Community 338 - "word_count_top"
Cohesion: 0.36
Nodes (8): word_count_top(), test_basic(), test_empty(), test_lowercases(), test_n_larger_than_distinct(), test_punctuation_is_not_stripped(), test_splits_on_any_whitespace(), test_ties_alphabetical()

### Community 339 - "Lists and loops"
Cohesion: 0.20
Nodes (9): Lists and loops, Rotating and chunking, Say it like this, Slicing rules, The problem it solves, The smallest runnable example, Trap 1: `sort()` returns `None`, Trap 2: changing a list while you loop over it (+1 more)

### Community 340 - "longest_unique"
Cohesion: 0.36
Nodes (8): longest_unique(), test_all_same(), test_basic(), test_case_matters(), test_empty(), test_keeps_overlap_after_repeat(), test_whole_string_unique(), test_window_must_not_move_back()

### Community 341 - "merge_intervals"
Cohesion: 0.36
Nodes (8): merge_intervals(), test_basic(), test_chain_and_point(), test_contained(), test_empty_and_single(), test_input_not_changed(), test_touching(), test_unsorted()

### Community 342 - "Window functions"
Cohesion: 0.20
Nodes (9): Neighbours: lag, lead, first_value, Ranking: row_number, rank, dense_rank, Running totals and frames, Say it like this, The problem it solves, The shape, The smallest example: the latest order per customer, The three traps (+1 more)

### Community 343 - "Dialect notes: what changes outside SQLite"
Cohesion: 0.20
Nodes (9): Date arithmetic, Dialect notes: what changes outside SQLite, FILTER, LIMIT, TOP and friends, QUALIFY, Say it like this, The problem it solves, The smallest example: one query, four spellings (+1 more)

### Community 344 - "Version"
Cohesion: 0.44
Nodes (7): sort_versions(), Version, test_compare(), test_empty_and_input_untouched(), test_field_names_and_order(), test_frozen(), test_sort()

### Community 345 - "py1-json-roundtrip/tests/test_hidden.py"
Cohesion: 0.42
Nodes (7): from_json(), to_json(), test_empty_dict(), test_invalid_returns_none(), test_nested_keys_sorted(), test_roundtrip(), test_sorted_compact()

### Community 346 - "running_sum"
Cohesion: 0.39
Nodes (7): running_sum(), test_basic(), test_empty(), test_floats(), test_input_unchanged(), test_negative(), test_single()

### Community 347 - "pairs"
Cohesion: 0.39
Nodes (7): pairs(), test_basic(), test_duplicates_kept(), test_empty(), test_returns_tuples(), test_single(), test_two()

### Community 348 - "first_unique"
Cohesion: 0.39
Nodes (7): first_unique(), test_basic(), test_case_matters(), test_empty(), test_none(), test_single(), test_unique_after_repeats()

### Community 349 - "is_valid_ip"
Cohesion: 0.39
Nodes (7): is_valid_ip(), test_bad_characters_and_empty(), test_leading_zero(), test_out_of_range(), test_signs_and_non_ascii_digits(), test_valid(), test_wrong_part_count()

### Community 350 - "Joins explained"
Cohesion: 0.22
Nodes (8): Finding rows with no match, Joining three tables and a table to itself, Joins explained, Say it like this, The four kinds you need, The problem it solves, The smallest example, The three traps

### Community 351 - "test_cards.py"
Cohesion: 0.42
Nodes (7): due(), record(), test_box_is_capped_at_five(), test_card_returns_on_its_due_date(), test_correct_answers_climb_boxes(), test_unseen_cards_are_due(), test_wrong_answer_resets_and_stays_due()

### Community 352 - "common_keys"
Cohesion: 0.43
Nodes (6): common_keys(), test_basic(), test_empty_list(), test_no_overlap(), test_single_dict(), test_three_dicts_sorted()

### Community 353 - "compose"
Cohesion: 0.43
Nodes (6): compose(), test_empty_is_identity(), test_reusable_and_args_not_mutated(), test_right_to_left(), test_single(), test_three_functions()

### Community 354 - "compress_spaces"
Cohesion: 0.43
Nodes (6): compress_spaces(), test_already_clean(), test_basic(), test_long_runs(), test_only_spaces_and_empty(), test_other_whitespace_kept()

### Community 355 - "count_vowels"
Cohesion: 0.43
Nodes (6): count_vowels(), test_basic(), test_empty(), test_none_and_y(), test_repeats_and_mixed_case(), test_upper()

### Community 356 - "days_between"
Cohesion: 0.39
Nodes (6): days_between(), parametrize, test_backward_is_positive(), test_bad_input_raises(), test_forward(), test_same_day_and_leap_year()

### Community 357 - "group_by_length"
Cohesion: 0.43
Nodes (6): group_by_length(), test_basic(), test_duplicates_kept(), test_empty(), test_empty_string_has_length_zero(), test_input_order_kept()

### Community 358 - "is_palindrome"
Cohesion: 0.43
Nodes (6): is_palindrome(), test_case(), test_digits_are_ignored(), test_empty_and_no_letters(), test_not_palindrome(), test_sentence()

### Community 359 - "safe_int"
Cohesion: 0.43
Nodes (6): safe_int(), test_bad_text_gives_default(), test_floats(), test_int_passes_through(), test_none_gives_default(), test_strings()

### Community 360 - "set_diff_report"
Cohesion: 0.43
Nodes (6): set_diff_report(), test_basic(), test_empty(), test_identical(), test_many_items_come_back_sorted(), test_sorted_and_deduplicated()

### Community 361 - "rank"
Cohesion: 0.43
Nodes (6): rank(), test_empty_and_no_mutation(), test_mixed(), test_negative_scores_and_returns_new_list(), test_score_desc(), test_ties_by_name()

### Community 362 - "title_case"
Cohesion: 0.43
Nodes (6): title_case(), test_apostrophe_and_edge_spaces(), test_basic(), test_empty(), test_keeps_spaces(), test_single_letter_words()

### Community 363 - "anagram_groups"
Cohesion: 0.43
Nodes (6): anagram_groups(), test_basic(), test_duplicates_kept(), test_empty(), test_single_and_empty_word(), test_sorted_by_first_word_not_by_key()

### Community 364 - "first_index"
Cohesion: 0.43
Nodes (6): first_index(), test_basic(), test_duplicates_first(), test_empty_and_single(), test_ends(), test_missing()

### Community 365 - "rotate"
Cohesion: 0.43
Nodes (6): rotate(), test_1x1_and_empty(), test_2x2(), test_3x3(), test_input_not_changed(), test_returns_lists()

### Community 366 - "top_k"
Cohesion: 0.43
Nodes (6): top_k(), test_basic(), test_empty_and_zero(), test_k_too_big(), test_ties_all_equal(), test_ties_by_first_appearance()

### Community 367 - "Clarifying questions"
Cohesion: 0.25
Nodes (7): A short checklist for the first two minutes, Clarifying questions, Say it like this, The five questions, The problem it solves, The smallest runnable example, Three traps people hit

### Community 368 - "Testing in 30 seconds"
Cohesion: 0.25
Nodes (7): Say it like this, Testing in 30 seconds, The method, The problem it solves, The smallest runnable example, Three traps people hit, Which edge case should I pick?

### Community 369 - "When you are stuck"
Cohesion: 0.25
Nodes (7): Say it like this, The problem it solves, The smallest runnable example, Three traps people hit, What to do, in order, What to say in common stuck moments, When you are stuck

### Community 370 - "GROUP BY and HAVING"
Cohesion: 0.25
Nodes (7): GROUP BY and HAVING, Say it like this, Several group columns and conditional aggregates, The order the database thinks in, The problem it solves, The smallest example, The three traps

### Community 371 - "Subqueries and CTEs"
Cohesion: 0.25
Nodes (7): CTEs: name your steps, Say it like this, Subqueries and CTEs, Subquery in FROM, The problem it solves, The smallest example, The three traps

### Community 372 - "NULLs, dates and de-duplication"
Cohesion: 0.25
Nodes (7): Dates in SQLite, De-duplication with row_number, NULLs, dates and de-duplication, NULLs: the smallest example, Say it like this, The problem it solves, The three traps

### Community 373 - "apply_n_times"
Cohesion: 0.48
Nodes (5): apply_n_times(), test_call_count(), test_double(), test_strings(), test_zero_returns_input_without_calls()

### Community 377 - "flatten"
Cohesion: 0.48
Nodes (5): flatten(), test_basic(), test_does_not_change_input(), test_empty(), test_one_level_only()

### Community 378 - "invert_dict"
Cohesion: 0.48
Nodes (5): invert_dict(), test_all_unique(), test_empty(), test_keys_sorted(), test_repeated_values()

### Community 379 - "merge_dicts_sum"
Cohesion: 0.48
Nodes (5): merge_dicts_sum(), test_basic(), test_empty_list_and_empty_dicts(), test_input_not_changed(), test_many_dicts()

### Community 380 - "parse_csv_line"
Cohesion: 0.48
Nodes (5): parse_csv_line(), test_empty_fields(), test_empty_line(), test_plain(), test_quoted_comma()

### Community 381 - "reverse_words"
Cohesion: 0.48
Nodes (5): reverse_words(), test_basic(), test_empty(), test_extra_spaces(), test_single_word()

### Community 385 - "unique"
Cohesion: 0.48
Nodes (5): unique(), test_already_unique(), test_basic(), test_empty(), test_strings_and_order()

### Community 386 - "parse_logs"
Cohesion: 0.48
Nodes (5): parse_logs(), test_basic(), test_empty(), test_malformed_skipped(), test_message_keeps_spaces()

### Community 387 - "roman_to_int"
Cohesion: 0.48
Nodes (5): roman_to_int(), test_empty(), test_long(), test_simple(), test_subtractive()

## Knowledge Gaps
- **194 isolated node(s):** `Version`, `Version`, `Version`, `Version`, `Version` (+189 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **44 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_content()` connect `load_content` to `app.py`?**
  _High betweenness centrality (0.001) - this node is a cross-community bridge._
- **Why does `create_app()` connect `app.py` to `load_content`?**
  _High betweenness centrality (0.000) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `____` (e.g. with `apply_n_times()` and `.withdraw()`) actually correct?**
  _`____` has 18 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Version`, `Version`, `Version` to the rest of the system?**
  _194 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `db.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09042553191489362 - nodes in this community are weakly interconnected._
- **Should `runner.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10256410256410256 - nodes in this community are weakly interconnected._
- **Should `load_content` be split into smaller, more focused modules?**
  _Cohesion score 0.0734006734006734 - nodes in this community are weakly interconnected._