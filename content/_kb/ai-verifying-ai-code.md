---
title: Verifying AI-written code
summary: Read every line, run your own tests, try three edge inputs and scan for the usual AI mistakes.
tags: [ai, testing]
---
```text
1. Read every line. If you cannot explain a line, ask or rewrite it.
2. Run tests. Yours, written from your prompt, not only the assistant's.
3. Try three edge inputs: empty, one item, a bad value (None or NaN).
4. Scan for the usual mistakes:
   - off by one in ranges, slices, chunk ends
   - mutable default argument:  def f(x, seen=[])
   - NaN comparisons:           nan == nan is False
   - naive datetimes mixed with timezone-aware ones
   - swallowed exceptions:      except: pass
   - data leakage:              fit on all data before the split
   - the input is mutated
   - wrong tie behaviour in sorting and ranking
```

- Use it on every answer from the assistant, before you say "done".
- Key rule: the code is a draft until your own test has run against it.
- Say: "I match each line to a rule in my prompt, then I run the edges. I would rather find the bug than the interviewer."

<!-- more -->

## Details

AI code usually runs on the happy path. The bugs sit where you did not ask. A short example: the assistant wrote a function that collects tags.

```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags

add_tag("a")      # ['a']
add_tag("b")      # ['a', 'b']   expected ['b']: the default list is shared between calls
```

One call looks correct. The second call shows the bug. The fix is a `None` default and a new list:

```python
def add_tag(tag, tags=None):
    tags = [] if tags is None else list(tags)   # also: do not mutate the caller's list
    tags.append(tag)
    return tags

add_tag("a")      # ['a']
add_tag("b")      # ['b']
```

How to run the routine in practice:

- **Write one assert before reading the code.** Take it from your prompt. If the test is written from the code, both can be wrong together.
- **Check where loops end.** For each `range` and slice, say the last index out loud.
- **Search for `except`.** Each one must name an error type and do something visible.
- **Search for `now()`, `random` and `set`.** They are the usual sources of non-deterministic results.
- **Debug by reasoning.** When a test fails, find the line and say why it is wrong. Then fix it, or tell the assistant exactly what to change.

## Common mistakes

- Trusting the assistant's own tests.
- Testing only one normal input.
- Pasting the error back and hoping, without finding the faulty line.
- Fixing the visible bug and not adding a test for it.

## See also

- [Anatomy of a good prompt](#/kb/ai-prompt-anatomy)
- [What to test: behaviours, edges, failure paths](#/kb/test-what-to-test)
- [Functions: defaults, *args, **kwargs, the mutable default trap](#/kb/py-functions-args)
- [Floats, NaN, infinity and rounding](#/kb/py-math-nan)
