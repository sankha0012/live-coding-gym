---
title: Schema versions and evolution
summary: Put a version on every record and upgrade old ones step by step, so code handles one current shape.
tags: [production, schema]
---
```python
def v1_to_v2(r):
    return {**r, "version": 2, "currency": "EUR"}       # new field gets a default

def v2_to_v3(r):
    r = {**r, "version": 3, "amount_cents": round(r["amount"] * 100)}
    del r["amount"]                                     # renamed and re-typed
    return r
MIGRATIONS = {1: v1_to_v2, 2: v2_to_v3}
LATEST = 3

def upgrade(record):
    while (v := record.get("version", 1)) < LATEST:
        record = MIGRATIONS[v](record)                  # each step returns a new dict
    return record
```

- Use it for stored records, messages, feature rows and saved model inputs that outlive one release.
- Key rule: one small migration per version step, applied in a chain. The rest of the code sees only the latest version.
- Say: "Old and new writers exist at the same time during a deploy, so readers must accept both."

<!-- more -->

## Details

```python
old = {"id": 1, "amount": 19.99}                 # no version field: treated as v1
upgrade(old)     # {'id': 1, 'version': 3, 'currency': 'EUR', 'amount_cents': 1999}
old              # {'id': 1, 'amount': 19.99}    the input is not changed
upgrade({"id": 2, "version": 3, "currency": "USD", "amount_cents": 500})
# {'id': 2, 'version': 3, 'currency': 'USD', 'amount_cents': 500}
```

A v1 record goes through both steps. A v3 record passes through unchanged. Adding v4 later means one new function and one new dict entry.

Two words to know:

- **Backward compatible**: new code can read old data. Needed for everything already stored.
- **Forward compatible**: old code can read new data. Needed while old and new versions run side by side.

Safe changes: add an optional field with a default, and ignore fields you do not know. Risky changes: remove a field, rename it, change its type or its unit. Do those in steps: write both forms, move the readers, then stop writing the old form.

A version **newer** than the code knows must not be guessed at. Raise a clear error:

```python
def check_version(record):
    if record.get("version", 1) > LATEST:
        raise ValueError(f"unsupported version {record['version']}")
```

## Common mistakes

- No version field at all, so the code guesses the shape from which keys are present.
- One big function with `if version == ...` branches all through the business logic.
- Mutating the caller's record during the upgrade.
- Reusing an old field name with a new meaning or unit.
- Silently accepting a future version and dropping its new fields.

## See also

- [Input validation and data contracts](#/kb/prod-input-validation)
- [Dictionaries: get, setdefault, items, membership](#/kb/py-dicts)
- [Training-serving skew](#/kb/prod-train-serve-skew)
