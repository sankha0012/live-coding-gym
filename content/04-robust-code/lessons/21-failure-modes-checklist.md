# The failure modes checklist

## The problem it solves

In a live round the prompt is short and the easy case is obvious. Interviewers for ML systems roles are looking at what you do next. Real data is messy and real dependencies fail. If you ask the right questions before you code, you write fewer bugs and you show that you think like someone who has run a system in production.

Use a fixed list. Do not rely on memory under stress. Say the questions out loud, then write the code.

## The ten questions

1. **What is the input contract?** Types, required fields, allowed ranges. Where does validation happen: at the boundary, once.
2. **What if a value is missing?** None, empty string, a missing key. Decide: reject, default or skip. Record it.
3. **What if a value is NaN or infinite?** `float("nan") != float("nan")`, so `x == x` is false for NaN. Use `math.isfinite`.
4. **What if the input is empty?** Empty list, empty batch, zero rows. Averages and divisions break here.
5. **What if it is huge?** Can it fit in memory? Use an iterator and process in chunks.
6. **What if a dependency fails or is slow?** Set a timeout. Retry only transient errors. Fall back to a safe default.
7. **What if the same input arrives twice?** Make the work idempotent. Dedupe by a key.
8. **What if events arrive out of order?** Decide which one wins, with a clear rule such as the highest `(timestamp, id)`.
9. **What if it runs twice, or crashes half way?** Write atomically. Never leave a half-written file.
10. **How will I know it broke?** Count the bad rows, the fallbacks and the retries. Log structured records. Silent failure is the worst failure.

## The smallest runnable example

This function applies several of the questions in a few lines.

```python
import math


def safe_mean(values):
    """Mean of the usable numbers. Returns (mean, skipped)."""
    good = []
    skipped = 0
    for v in values:
        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
            skipped += 1
            continue
        good.append(v)
    if not good:
        return None, skipped
    return sum(good) / len(good), skipped


assert safe_mean([1, 2, 3]) == (2.0, 0)
assert safe_mean([1, None, float("nan"), 3]) == (2.0, 2)
assert safe_mean([]) == (None, 0)
print(safe_mean([4, "x", 6]))
```

It handles missing values (question 2), NaN and inf (3), the empty input (4) and it counts what it skipped (10). The `bool` check is on purpose: `True` is an int in Python, and a flag in a metric column is almost always a bug.

## Three traps people hit

1. **Handling only the happy path and the one error in the prompt.** The prompt names one edge case. The interviewer has three more ready. Run the list every time.
2. **Catching everything.** A bare `except Exception: pass` hides real bugs and turns a loud failure into a silent one. Catch the specific error, handle it, and count it.
3. **Fixing silently.** If you replace a bad value with a default and say nothing, the metric is wrong and nobody knows. Return or log how many values you repaired.

## How to use it in the interview

After you read the prompt, take thirty seconds. Say: "Before I code, I want to check a few failure cases." Name three or four of the ten that apply. Then write the simplest correct code, and add a small assert for each case you named. You do not need all ten every time. Pick the ones that matter for the data in the prompt, and say why you skipped the others.

When you use an AI assistant, paste the relevant questions into your prompt. "Handle None, NaN, empty input and return a count of skipped rows" is a much better prompt than "write a mean function", and the interviewer sees you directing the tool.

## Say it like this

"Before I code I check the failure modes. What is the input contract, and what happens with missing values, NaN, or an empty batch? If there is a dependency, I want a timeout and a fallback. If events can repeat or arrive late, I need idempotency and a clear ordering rule. And I want to count what I skip or repair so a silent failure shows up. For this task the main risks are the empty input and NaN, so I handle those first and test them."
