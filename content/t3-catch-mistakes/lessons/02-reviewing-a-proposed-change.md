# How to review a proposed change

## The problem it solves

When the assistant proposes an edit to code that already works, the question is not "is this code good?" but "is this change what I asked for, and is it safe?" A checklist makes the decision quick and consistent: accept, reject, or shrink.

## The process

1. **Restate the request** in one sentence before you look at the change.
2. **Read the diff**, every added and removed line, not only the part you expected.
3. **Run your tests**: the ones you had before the change, unmodified.
4. **Decide** with the checklist below.
5. **If you accept, say why** in one sentence. If you reject, say which rule failed.

## Accept / reject checklist

Reject, or ask for a smaller change, if any answer is "yes":

- Does it change something I did not ask about (another function, a default, a return type, an output format)?
- Does it touch a test, an expected value or a check so that a failing case passes?
- Does it add a dependency, a new file, a new class or a configuration option I did not request?
- Does it catch a broad exception or add a fallback that hides errors?
- Does it change the order of results, tie-breaking, rounding or the types of values?
- Does it mutate an argument or global state that was not mutated before?
- Does it change the time complexity for large inputs?
- Is there a line I cannot explain?

Accept only if all of these hold:

- [ ] The change does what I asked, and nothing else.
- [ ] I can explain every changed line.
- [ ] My tests pass, and no test was modified.
- [ ] I tried an edge input (empty, one item, a bad value) on the new code.

## An example

Request: "`count_words` should ignore case."

Proposed change:

```diff
 def count_words(text):
-    counts = {}
-    for word in text.split():
-        counts[word] = counts.get(word, 0) + 1
-    return counts
+    from collections import Counter
+    return dict(Counter(w.strip(".,!?").lower() for w in text.split()))
```

Review: the request was about case. The change also strips punctuation, which was not asked for, and replaces the loop with `Counter`. Both change behaviour: `"hi,"` and `"hi"` now count together. The rewrite is not needed to satisfy the request.

Decision: **reject, ask for a smaller change.** The right edit is one line, `for word in text.lower().split():`. The reason you give: "it does more than I asked; it changes how punctuation is treated".

Another case: the proposal fixes a crash on empty input by adding `except Exception: return {}` around the loop. Reject: it hides every other error. Ask instead for an explicit check, `if not text.strip(): return {}`.

## Accepting partially

You can keep part of a proposal. Apply the lines you understand and want, discard the rest, and run the tests again. A smaller change is easier to defend.

## When to accept quickly

A small, local change that matches the request, with unmodified tests that pass and a diff you can read in a minute: accept. The goal is not to distrust everything, it is to keep each decision informed.

## Common mistakes

- Judging the change by how clean it looks.
- Accepting because the tests passed, when the tests were edited in the same change.
- Reviewing the new code but not what it removed.
- Accepting a large change "to save time" and paying later in debugging.

## Related

- [Verifying AI-written code](#/kb/ai-verifying-ai-code)
- [Testing: what to test](#/kb/test-what-to-test)
- [Prompt anatomy](#/kb/ai-prompt-anatomy)
