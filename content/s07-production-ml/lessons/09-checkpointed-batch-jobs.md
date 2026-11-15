# Checkpointed batch jobs

## What it is

A checkpointed batch job processes data in chunks and records its progress after each chunk, so after a crash it resumes from the last good point and not from the start. Two properties make this safe. The job must be idempotent, so processing the same chunk twice gives the same result and no duplicates. The checkpoint itself must be written atomically, so a crash in the middle of writing never leaves a half-written file. See [checkpointing](#/kb/prod-checkpointing), [chunked processing](#/kb/prod-chunked-batch-processing), [idempotency](#/kb/prod-idempotency) and [atomic writes](#/kb/prod-atomic-write).

## How it breaks in production

A job over a million rows fails at row 900,000, and without a checkpoint it re-scores everything. The checkpoint can also cause damage. If you save progress before the output is written, a crash skips a chunk forever. If you write the output first and the checkpoint after, a crash repeats a chunk, which is fine only if the write is idempotent; an append-only write doubles those rows. A checkpoint written in place can be left half-written by a crash, and then the job cannot start.

## The defence in code

```python
import json, os, tempfile

def save_checkpoint(path: str, state: dict) -> None:
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path))
    with os.fdopen(fd, "w") as f:
        json.dump(state, f)
    os.replace(tmp, path)                      # atomic: readers see the old or the new file, never half

def load_checkpoint(path: str) -> dict:
    try:
        with open(path) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"next": 0}

def run(rows, out: dict, ckpt: str, chunk: int = 2, fail_at=None) -> None:
    state = load_checkpoint(ckpt)
    for start in range(state["next"], len(rows), chunk):
        for i in range(start, min(start + chunk, len(rows))):
            if i == fail_at:
                raise RuntimeError("crash")
            out[rows[i]["id"]] = rows[i]["x"] * 2      # keyed write: a repeat overwrites
        save_checkpoint(ckpt, {"next": start + chunk})  # after the output, so a crash repeats a chunk

with tempfile.TemporaryDirectory() as d:
    ckpt, out = os.path.join(d, "ckpt.json"), {}
    rows = [{"id": i, "x": i} for i in range(5)]
    try:
        run(rows, out, ckpt, fail_at=3)
    except RuntimeError:
        print("crashed, checkpoint:", load_checkpoint(ckpt))
    run(rows, out, ckpt)                                # resumes at chunk starting at row 2
    print(out)
```

The first run crashes with the checkpoint at row 2. The rerun resumes there and nothing is duplicated.

## What to say in the interview

"I process in chunks, write the output idempotently by key, and then save a checkpoint atomically with a temporary file and a rename. A crash can repeat a chunk but never skip one, and because the write is idempotent the repeat is harmless. Bad rows go to a quarantine with a reason, and I alert if their share is unusual. I also take the run date as a parameter, never the current time, so a backfill gives the same result."
