# Data contracts and schema evolution

## What it is

A data contract is a written and enforced agreement about the data that crosses a boundary: field names, types, allowed ranges, which fields may be null, and a version number. The producer promises it and the consumer checks it at the entry point. Schema evolution is the discipline of changing that contract without breaking anyone. See [input validation](#/kb/prod-input-validation) and [schema evolution](#/kb/prod-schema-evolution) for the detailed patterns.

## How it breaks in production

A model trusts its inputs, so a bad input rarely crashes it; it produces a quietly wrong score. An upstream team renames a column, switches distance from kilometres to metres, or starts sending nulls, and every dashboard stays green. Type checks alone miss this: a distance of 3000 is a valid float and still wrong. Python adds its own trap, because `True` is an instance of `int`, so a boolean passes a naive number check. Evolution breaks things in two directions. If the consumer rejects every unknown field, a producer adding an optional field takes you down. If the producer renames a field without a version, old consumers read nothing.

## The defence in code

```python
def validate(row: dict) -> list[str]:
    errors = []
    d = row.get("distance_km")
    if not isinstance(d, (int, float)) or isinstance(d, bool):
        errors.append("distance_km must be a number")
    elif not 0 <= d <= 100:
        errors.append("distance_km out of range")
    if row.get("status") not in {"open", "closed"}:
        errors.append("status must be open or closed")
    return errors

def normalize(payload: dict) -> dict:
    version = payload.get("schema_version", 1)
    if version == 1:                       # old name
        return {"distance_km": payload["distance"], "status": payload["status"]}
    if version == 2:                       # extra fields are ignored, not rejected
        return {"distance_km": payload["distance_km"], "status": payload["status"]}
    raise ValueError(f"unsupported schema_version {version}")

print(validate({"distance_km": True, "status": "paused"}))
print(validate({"distance_km": 500, "status": "open"}))
print(normalize({"distance": 2.0, "status": "open"}))
print(normalize({"schema_version": 2, "distance_km": 2.0, "status": "open", "note": "new"}))
```

Every supported version maps to one internal shape. On a violation, reject in an online API, quarantine in a batch job, impute only when harmless, and always count the rate.

## What to say in the interview

"I validate at the boundary for types, ranges, nullability and a schema version, and I return every error at once. On a violation I choose by case: reject online, quarantine in batch, and only impute when it is harmless, always counting it. I map each supported version to one internal shape, and I am strict about required fields but tolerant of extra ones, so an added optional field does not break me."
