# Input validation and typed contracts

## What it is

An input contract states what a record must look like: which fields exist, their types and their allowed ranges. Validation checks it once, at the boundary where data enters your code, and either returns a clean object or raises a clear error. A typed contract expresses the clean object as a dataclass, so the rest of the code works with known fields instead of loose dictionaries. See [Input validation](#/kb/prod-input-validation), [Dataclasses](#/kb/py-dataclasses) and [NaN and infinity](#/kb/py-math-nan).

## How it breaks in production

Real feeds send missing keys, `None`, strings instead of numbers, `NaN`, negative ages and booleans in numeric columns. Type hints are not enforced at run time. Without validation at the edge, the bad value travels deep into the code and fails somewhere unrelated, or does not fail at all. `NaN` is the classic case: `nan < 0` and `nan > 1` are both false, so a range check written as "reject if below 0 or above 1" lets `NaN` through, and it then poisons every sum and mean it touches. A `bool` is an `int` in Python, so `True` passes an `isinstance(x, int)` check.

## The defence in code

```python
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Row:
    user_id: str
    age: int
    score: float


def parse_row(raw):
    uid = raw.get("user_id")
    if not isinstance(uid, str) or not uid:
        raise ValueError("user_id must be a non-empty string")
    age = raw.get("age")
    if isinstance(age, bool) or not isinstance(age, int) or not 0 <= age <= 120:
        raise ValueError(f"age must be an int in [0, 120], got {age!r}")
    score = raw.get("score")
    if isinstance(score, bool) or not isinstance(score, (int, float)) or not math.isfinite(score):
        raise ValueError(f"score must be a finite number, got {score!r}")
    return Row(uid, age, float(score))


assert parse_row({"user_id": "u1", "age": 30, "score": 1}) == Row("u1", 30, 1.0)
for bad in ({"user_id": "u1", "age": 30, "score": float("nan")},
            {"user_id": "u1", "age": True, "score": 0.5},
            {"user_id": "", "age": 30, "score": 0.5},
            {"age": 30, "score": 0.5}):
    try:
        parse_row(bad)
    except ValueError as e:
        print("rejected:", e)
    else:
        raise AssertionError("should have been rejected")
```

Each message names the field and shows the bad value. `math.isfinite` rejects both `NaN` and infinity. `frozen=True` makes the row immutable. In a batch, call `parse_row` in a try block and count the rejects.

## What to say in the interview

"I validate once at the boundary and turn the raw dictionary into a frozen dataclass, so the rest of the code works with known fields. I check types, ranges and finiteness explicitly, because type hints are not enforced and NaN passes a naive range check. Errors name the field and the value. In a batch I count what I reject rather than failing silently or crashing."
