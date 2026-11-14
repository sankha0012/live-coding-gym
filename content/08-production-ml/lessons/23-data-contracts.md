# Data contracts

## The problem it solves

A model trusts its inputs. If an upstream team renames a column, changes a unit, or starts sending nulls, the model does not crash. It quietly produces nonsense. A data contract is a written, checked agreement about what the data looks like: field names, types, allowed ranges, and what each field means. It turns silent failures into loud ones at the door.

A contract usually covers:

- **Schema:** required fields and their types.
- **Ranges and values:** distance between 0 and 100 km, status in a fixed set, rate between 0 and 1.
- **Nullability:** which fields may be missing.
- **Version:** a number that changes when the shape changes.
- **Ownership:** who to call when it breaks.

## The smallest runnable example

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

print(validate({"distance_km": 3.2, "status": "open"}))
print(validate({"distance_km": "3", "status": "paused"}))
print(validate({"distance_km": 500, "status": "open"}))
```

It returns every problem, not only the first, so the sender can fix them in one pass. The `bool` check matters: in Python `True` is an `int`, so without it a boolean would pass as a number.

## Versioning

Contracts change. Handle that explicitly. Put a `schema_version` in each payload and accept the versions you support.

```python
def normalize(payload: dict) -> dict:
    version = payload.get("schema_version", 1)
    if version == 1:
        return {"distance_km": payload["distance"], "status": payload["status"]}
    if version == 2:
        return {"distance_km": payload["distance_km"], "status": payload["status"]}
    raise ValueError(f"unsupported schema_version {version}")

print(normalize({"distance": 2.0, "status": "open"}))
print(normalize({"schema_version": 2, "distance_km": 2.0, "status": "open"}))
```

Both versions turn into one internal shape, so the model code never sees the difference. Adding an optional field is a safe change. Renaming, removing, or changing a unit is a breaking change and needs a new version, plus time for producers to migrate.

## What to do on violation

Decide this per field, in advance, and write it down. The options are:

- **Reject** the record or request with a clear error. Best for online APIs and for fields the model cannot live without.
- **Quarantine** the record into a separate table with the reason, and continue with the rest. Best for batch jobs: one bad row should not kill a million good ones.
- **Default or impute** a safe value and flag it. Only for fields where a default is truly harmless, and always count how often it happens.
- **Alert** when the violation rate rises. A sudden 20 percent of rows failing is an upstream incident, not 20 percent of bad luck.

## The three traps

**1. Validating types but not meaning.** A field can be a valid float and still be wrong: negative durations, a latitude of 0 and a longitude of 0, a price in cents where you expected reais. Range checks and a few sanity rules catch much more than type checks.

**2. Silently fixing bad data.** Replacing every bad value with zero keeps the pipeline green and the model wrong. If you repair, count it, log it, and alert on the rate. A hidden repair is worse than a visible failure.

**3. Strict on the wrong side of a change.** If the consumer rejects any unknown field, a producer adding an optional field breaks you. A good rule is to be strict about what you need, and tolerant of extra fields you ignore. Reject missing or wrong required fields, but do not fail on harmless additions.

Also keep the contract in one place and share it between training and serving. If training allows a value that serving rejects, or the reverse, you have created skew.

## Say it like this

"A data contract is a checked agreement on schema, types, ranges, nullability and version. I validate at the entry point and return all errors at once. On a violation I decide by case: reject in an online API, quarantine the bad rows in a batch job, and only impute when a default is harmless, always counting it. I carry a schema version and map every supported version to one internal shape, so old and new payloads both work. I am strict about required fields and tolerant of extra ones, and I alert when the violation rate climbs."
