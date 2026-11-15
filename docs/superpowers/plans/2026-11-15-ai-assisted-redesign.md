# AI-assisted redesign: implementation plan

Approved design: "Live coding gym redesign: AI-assisted coding" (artifact `2qNaJe1kNPDGQcHjdGs13U`), approved by the user on 2026-11-15 with its three defaults (SQL off the main path, chat assistant only with no inline autocomplete, timeline counted from approval).

Philosophy: the learner is the engineer and the assistant is the typist. Plan before prompting, ask small, read every line, verify, fix by hand, explain. Hand-coding grows out of small manual fixes. Reading fluency is taught first.

## Structure

Six track steps replace the twelve. The twelve old steps become the **Library** (an unlocked optional shelf, `shelf: true` in `step.yaml`).

| Track step | Folder | Content |
|---|---|---|
| 1 Read Python fluently | `t1-read-python` | `read` exercises (predict the output, explain lines), reading flashcards |
| 2 The control loop | `t2-control-loop` | plan as comments, prompt one piece at a time, Coderbyte stdin format |
| 3 Catch the assistant's mistakes | `t3-catch-mistakes` | `python` exercises that start from assistant-written buggy code (assistant off, name the bug), `triage` exercises (accept or reject proposed changes) |
| 4 Robust ML systems, assisted | `t4-robust-ml` | existing robust-ML drills (moved in with `includes`), built with the assistant |
| 5 Explain and defend | `t5-explain-defend` | existing explain exercises and follow-ups, tools as talking-point cards |
| 6 Mock rounds | `t6-mock-rounds` | 35 minutes assisted coding plus 20 minutes of follow-ups |

`step.yaml` gains `shelf`, `includes` (ids of exercises moved here from other steps), `sequence` (explicit order).

## Mechanisms

1. **One assistant, policy per exercise** (`assistant:` in `exercise.yaml`): `train` (default for coded kinds: at most one function per reply; oversized asks are sent back to be broken down), `explain` (default for answer-writing kinds and step 1: explains only, never writes code), `off`, `free` (mock rounds). Every reply starts with a `SIZE: small|large` line that the server strips and stores; the size of each ask feeds the mock score. A "Explain this line" button uses the editor cursor line. Tutor and interview modes are removed.
2. **Control check** (`change.md`, `change_tests/`, `change_solution.py` in an exercise folder): after the tests pass, the app picks two lines of the learner's passing code at random (fixed per attempt); the learner explains them (AI review, kind `line`), then makes one small change by hand with the assistant locked (hidden `change_tests`). Both parts must pass. Checker rules: the change tests pass on `change_solution.py` and fail on the unchanged reference solution.
3. **New kinds**: `read` (predict the exact output of `snippet.py` from `expected.txt`, plus a reviewed explanation of questions in the exercise), `triage` (accept or reject each proposed change in `proposals.yaml`, with a reason; decisions are scored exactly, reasons AI-reviewed). `python` exercises gain `name_bug: true` (the learner names the bug in one sentence, reviewed against `bug.md`), `plan_required: N` (at least N comment lines in the submission), `grade_prompts: true` (the learner's prompts to the assistant must pass the prompt review).
4. **Cuts**: retype, fill-the-gaps and timed modes, timed gates. Blank editor stays as an optional "Challenge: empty editor" mode that counts but never gates. SQL and the old drills live in the Library.
5. **Flashcards** flip to "what does this snippet do". Only track cards are in the daily deck.
6. **Mock rounds**: two Python tasks plus the assistant in `free` policy; follow-ups are two "explain this line" questions plus three AI questions; score adds the size of each ask, whether code was run before accepting it, and the line-explanation result.

## Delivery

Part 1: app mechanisms and steps 1 to 3 (so practice can start). Part 2: steps 4 to 6 and the mock changes.
