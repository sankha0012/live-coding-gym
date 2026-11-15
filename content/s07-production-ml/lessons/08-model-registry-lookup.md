# Model registry lookup

## What it is

A model registry is a catalogue on top of the stored model files. Each entry has a name, a version, a stage or alias such as staging or production, and metadata about the run and data that produced it. Serving code asks the registry for "the production version of eta" instead of hard-coding a file path, so promoting a new model or rolling back is a registry change, not a redeploy. The artifact store answers where the file is; the registry answers which model is live. See [joblib persistence](#/kb/ml-joblib-persistence) and [atomic writes](#/kb/prod-atomic-write).

## How it breaks in production

Version strings are the classic bug. Compared as text, `"1.9.0"` sorts after `"1.10.0"`, so a naive maximum quietly serves an older model. Padding is another: `"2.1"` and `"2.1.0"` are the same version. A lookup that returns `None` pushes the failure downstream as an unrelated `AttributeError`. A malformed record such as `"v1"` should not crash the lookup. Deployment adds risks: a file loaded with a different scikit-learn version can fail or change behaviour, joblib files are pickles and must come from a trusted store, and a response that omits the model version makes incidents hard to trace.

## The defence in code

```python
def parse(version: str):
    parts = version.split(".")
    if not all(p.isdigit() for p in parts):
        return None
    nums = [int(p) for p in parts]
    while len(nums) > 1 and nums[-1] == 0:     # "2.1.0" and "2.1" become the same key
        nums.pop()
    return tuple(nums)

def latest(records: list[dict], name: str, stage: str) -> dict:
    best, best_key = None, None
    for r in records:
        if r["name"] != name or r["stage"] != stage:
            continue
        key = parse(r["version"])
        if key is None:
            continue                            # skip bad records, do not crash
        if best_key is None or key > best_key:  # strict: a tie keeps the first record
            best, best_key = r, key
    if best is None:
        raise LookupError(f"no {stage} model named {name}")
    return best

registry = [
    {"name": "eta", "version": "1.9.0", "stage": "production"},
    {"name": "eta", "version": "1.10.0", "stage": "production"},
    {"name": "eta", "version": "v2", "stage": "production"},
]
print(latest(registry, "eta", "production")["version"])    # 1.10.0
print(max(r["version"] for r in registry[:2]))             # 1.9.0, the text-order mistake
try:
    latest(registry, "eta", "staging")
except LookupError as e:
    print("loud failure:", e)
```

Versions become integer tuples, and a missing model raises a clear `LookupError`.

## What to say in the interview

"Serving resolves the model through a registry by name and stage, and I compare versions as numeric tuples, never as strings. If nothing matches I fail loudly. I return the model version in every response and log it, so any prediction can be traced, and the previous version stays stored so rollback is a change of alias. I pin library versions and only load artifacts from a trusted store."
