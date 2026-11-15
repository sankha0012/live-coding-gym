# Writing a good small prompt

The size of a prompt decides how much you can check. A small prompt returns a short answer that you can read in a minute. A big prompt returns a long answer where a wrong decision hides easily, and you will not be able to explain it afterwards.

## Too big versus right size

| Too big | Right size |
|---|---|
| "Solve this task" with the whole statement pasted | "Write `parse(text)` that turns `'1,5,3'` into `[1, 5, 3]`" |
| "Build a log analyser with filters and a report" | "Write `level(line)`. Later, separately, `count_levels(lines)`" |
| "Make it better" | "Replace the inner loop with a set lookup" |
| "Fix the bugs" | "On `[]` line 4 raises `IndexError`; return `0` instead" |
| "Write tests for everything" | "Write three asserts for `merge`: both empty, one empty, overlapping" |

A right-size prompt has one result you can look at and judge as correct or not.

## One task in four asks

Task: lines look like `ERROR disk full`; count how many lines have each level.

1. "Write `level(line)` returning the first word of a line, or `None` for an empty line."
2. "Write `count_levels(lines)` that uses `level` and returns a dict from level to count, skipping `None`."
3. "Write the main block: read stdin, call `count_levels`, print `LEVEL count` in alphabetical order."
4. "Write three asserts for `count_levels`: empty list, one level repeated, two levels."

Here is what asks 1 and 2 might return, and a check:

```python
def level(line):
    parts = line.split()
    return parts[0] if parts else None

def count_levels(lines):
    counts = {}
    for line in lines:
        lv = level(line)
        if lv is not None:
            counts[lv] = counts.get(lv, 0) + 1
    return counts

assert count_levels([]) == {}
assert count_levels(["ERROR x", "ERROR y", "", "INFO z"]) == {"ERROR": 2, "INFO": 1}
print("ok")
```

Each ask is followed by read, run, explain. Four small checks are easier and more reliable than one large one.

## Habits that help

- **Show an example.** One real input and its exact expected output removes most guessing.
- **Say what not to do:** "standard library only", "do not change the signature".
- **State the input type.** In Coderbyte tasks the input is text, and the assistant will not know unless you say so.
- **Ask for the plain version** when you want to read fast: "simple loop, no comprehension."

If the answer is bigger than you asked for, say "that is more than I asked, I only want X" or delete the extra code. Do not try to review code you did not request.

Related: [Anatomy of a good prompt](#/kb/ai-prompt-anatomy), [Context budget](#/kb/ai-context-budget).
