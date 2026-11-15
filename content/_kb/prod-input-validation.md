---
title: Input validation and data contracts
summary: Check type, presence and range at the edge of the system and report every problem, before a model sees the row.
tags: [production, validation]
---
```python
import math

def validate(row: dict) -> list[str]:
    problems = []
    age = row.get("age")
    if isinstance(age, bool) or not isinstance(age, int):
        problems.append("age: must be an int")
    elif not 0 <= age <= 120:
        problems.append("age: out of range")
    score = row.get("score")
    if not isinstance(score, float) or math.isnan(score):
        problems.append("score: must be a real float")
    return problems          # empty list means the row is valid
```

- Use it at every boundary: API request, file row, feature vector, model output.
- Key rule: check presence, then type, then range, and collect all problems instead of stopping at the first.
- Say: "I validate at the edge so bad data fails loudly here and not silently inside the model."

<!-- more -->

## Details

A data contract is the written list of fields, types, ranges and allowed values. The validator is that contract as code.

```python
validate({"age": 30, "score": 0.5})              # []
validate({"age": 200})                           # ['age: out of range', 'score: must be a real float']
validate({"age": True, "score": float("nan")})   # ['age: must be an int', 'score: must be a real float']
```

For each bad value you must choose a policy, and say it out loud:

- **Reject**: raise or return the problems. Right for requests and config.
- **Repair**: use a default or clip to the range, and record that you did. Right when a prediction is still needed.
- **Quarantine**: put the row in an error list and continue the batch.

Never repair silently. A counter of repaired rows is how you notice an upstream bug.

Build a new clean row. Do not change the caller's dict.

For model outputs the same idea applies: a score must be finite and inside its range before you return it.

## Common mistakes

- Forgetting that `bool` is a subclass of `int`, so `True` passes `isinstance(x, int)`.
- Forgetting NaN and infinity: `float("nan")` is a float and fails every range comparison quietly.
- Using `if not value` for "missing": it also rejects `0`, `0.0` and `""`.
- Stopping at the first problem, so the caller fixes one field per round trip.
- Converting with `float(x)` and catching nothing: `float("abc")` raises `ValueError`, `float(None)` raises `TypeError`.

## See also

- [Floats, NaN, infinity and rounding](#/kb/py-math-nan)
- [Dataclasses](#/kb/py-dataclasses)
- [Schema versions and evolution](#/kb/prod-schema-evolution)
- [Chunked batch processing and isolating bad records](#/kb/prod-chunked-batch-processing)
