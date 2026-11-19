# Control check: an AI interviewer asks about your own code (2026-11-19)

## Problem
The control check on a build asked "line N changes: do the tests still pass or fail?". It was guessable (two answers), judged by hidden tests the learner never sees, mostly line deletions (6 of 7 possible changes on `cb-pairsum`), and unlike a real interview. Level 3 explained two random lines with no reference answer. 52 of 60 core builds (steps 2 to 10) used it.

## Decision
Replace both with interview questions written by the AI about the learner's own passing code. Kept as they were: change by hand, name the bug, prompt grading, What if on readings.

## Design
- `interview.make_questions(call, task, code, focus, n, reference, avoid)` returns `n` questions with private notes (`ref`) in one AI call: a design choice on a quoted line, an edge case or bad input, a production concern (dropped at n=2). Rules: answerable in 2 or 3 spoken sentences; never yes/no, about tests, "what does this line do", or an exact computed output.
- Interview part `defend` in `gym/app.py`: questions are written once per passing attempt and stored in the saved exchange; `ref` is the judge's reference for that question and never leaves the server. New passing code or "Try again" writes new questions, avoiding the old ones. AI failure is a 502, with no generic fallback questions.
- Pass rule unchanged: nothing missed. Level 1: 2 questions. Levels 2 and 3: 3 questions, then the change by hand. Assisted extras: 2 questions.
- `gates.defended` = defend review passed, or legacy credit (old What if ok, or old explained lines), so finished work stays finished.
- Mock rounds: the 3 follow-ups come from the same generator; the two line questions stay.
- Removed: `gym/whatif.py` (build mutations), the `lines` part, `reviewer.followups` and its fallback list.

## Known limits
Every core build needs the AI provider to finish its check. Answers are judged against notes the AI wrote itself; the prompt keeps questions to what can be judged from the code.
