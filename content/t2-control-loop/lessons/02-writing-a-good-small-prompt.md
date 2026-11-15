# How to write a good small prompt

## The problem it solves

The size of your prompt decides how much you can check. A small prompt gives a short answer you can read in a minute. A big prompt gives a long answer in which a wrong choice is easy to miss. A good small prompt names the function, the input, the output and the edge cases that matter.

## The parts of a small prompt

1. **The unit**: one function or one step. "Write a function `parse_line(line)`".
2. **The input**: its type and an example. "`line` is a string like `'2024-01-05 ERROR disk full'`".
3. **The output**: type, format and an example. "Return a tuple `(date, level, message)`".
4. **The edge cases you care about**: empty input, a malformed line, ties.
5. **Constraints**: no imports beyond the standard library, do not modify the input, keep it under ten lines.

## Too big versus right-size

| Too big | Right-size |
|---|---|
| "Solve this task" (pasting the whole statement) | "Write `parse(text)` that returns a list of ints from a comma-separated string" |
| "Build a log analyser with filtering, counting and a report" | "Write `parse_line(line)`; then, separately, `count_levels(rows)`" |
| "Make it better" | "Replace the inner loop with a set lookup so the function is O(n)" |
| "Fix the bugs" | "On input `[]` this raises `IndexError` at line 4; return `0` instead" |
| "Write tests for everything" | "Write three asserts for `merge(a, b)`: both empty, one empty, overlapping" |

The right-size prompts each have one result you can look at and judge.

## Example: building up a task in four asks

Task: read lines like `ERROR disk full` and print how many lines have each level.

1. "Write `level(line)` that returns the first word of a non-empty line, or `None` for an empty line."
2. "Write `count_levels(lines)` that uses `level` and returns a dict from level to count; skip lines whose level is `None`."
3. "Write the main block: read stdin, call `count_levels` and print `LEVEL count` per level in alphabetical order."
4. "Write three asserts for `count_levels`: an empty list, one level repeated, two different levels."

After each answer: read, run, explain, change one thing. Four small checks are easier than one big one.

## Prompt habits

- **Show an example.** One input and its exact expected output removes most guessing.
- **Say what not to do.** "Do not use pandas", "do not change the function signature".
- **Ask for the plain version.** "Use a simple loop, no comprehension" if you will read it faster.
- **Ask one question at a time** when you want an explanation, and name the line.
- **Quote your plan comment** from the file so the answer matches your steps.

## What to do with a bad answer

If the answer is bigger than what you asked for, do not try to review it. Say "that is more than I asked; I only want X" or just delete the extras. If it is wrong, report a failing input rather than a general complaint, and name the function that is at fault.

## Common mistakes

- Pasting the full task statement and accepting the first answer.
- Leaving the output format unstated, then being surprised by `True` instead of `"true"`.
- Asking for several functions in one prompt.
- Not saying the input type. The assistant will guess, and the guess may differ from the real input, which in Coderbyte tasks is text.

## Related

- [Prompt anatomy](#/kb/ai-prompt-anatomy)
- [Context budget](#/kb/ai-context-budget)
- [Verifying AI-written code](#/kb/ai-verifying-ai-code)
