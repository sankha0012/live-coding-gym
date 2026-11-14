# Defensive patterns

## The problem it solves

You cannot stop a model from ever producing a bad answer. You can decide what your system does when it happens. Defensive code is a small set of habits: validate, clip, fall back, alarm. The last question, whether to fail closed or open, is a product decision that you should say out loud.

## The five moves

1. **Validate** inputs at the edge. Check type, presence and range before the model sees them.
2. **Clip** values that are slightly out of range into the valid range, when that is safe.
3. **Fall back** when the model cannot answer: a simpler rule, then a constant.
4. **Alarm** when repairs become frequent. A rising fallback rate is the real signal.
5. **Decide closed or open** for the case where you cannot trust anything.

## The smallest runnable example

A fallback chain with a counter. The model and the rule are parameters, so it is easy to test.

```python
import math
from collections import Counter


def predict(row, model, rule, default=0.5, stats=None):
    stats = stats if stats is not None else Counter()
    try:
        score = model(row)
        if isinstance(score, (int, float)) and math.isfinite(score):
            stats["model"] += 1
            return min(1.0, max(0.0, score))
    except Exception:
        stats["model_error"] += 1
    try:
        score = rule(row)
        stats["rule"] += 1
        return score
    except Exception:
        stats["default"] += 1
        return default


def broken_model(row):
    raise RuntimeError("down")


stats = Counter()
assert predict({"x": 1}, broken_model, lambda r: 0.7, stats=stats) == 0.7
assert predict({"x": 1}, lambda r: float("nan"), lambda r: 0.2, stats=stats) == 0.2
assert predict({}, broken_model, lambda r: r["x"], stats=stats) == 0.5
print(dict(stats))
```

The chain is model, then rule, then constant. Each step has a counter. If `stats["default"]` grows, somebody gets paged.

## Fail closed or fail open

When the model cannot be trusted, you have two choices.

- **Fail closed:** refuse the action. Use it when a wrong "yes" is expensive, for example approving a payment or a loan. You lose some good cases, but you never let a bad one through.
- **Fail open:** let the action happen with a safe default. Use it when blocking is expensive, for example showing a restaurant list. A generic, popular ranking is better than an empty page.

There is no universal answer. Ask: which mistake costs more? Then say which side you picked and why. An interviewer cares more about the reasoning than the choice.

## Three traps people hit

1. **A bare `except:` that swallows everything.** It hides real bugs, including your own typos. Catch `Exception` at the row boundary, record it, and let programming errors show up in tests.
2. **Fallbacks that nobody counts.** If the fallback quietly serves 40 percent of traffic, you are running the rule, not the model, and nobody knows. Log and alarm on the rate.
3. **A fallback that can also fail.** The last step must be a constant that cannot raise. A chain whose final link can throw is not a chain.

Also remember the order of checks. Test for NaN before you clip: `min(1.0, max(0.0, nan))` returns a surprising value that depends on argument order, not an error.

## Say it like this

"I validate at the edge, clip small range errors and count them, and fall back from the model to a rule and then to a constant that cannot fail. Every fallback increments a counter and I would alarm on the rate. For the unsafe case I choose fail closed when a wrong yes is costly, and fail open when blocking users is costly. Here I would fail open with the constant, because an empty answer hurts more than a generic one."
