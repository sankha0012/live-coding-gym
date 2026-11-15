---
title: Checkpointing and resuming a batch
summary: Save how far a long job got, so a restart continues after the last finished item.
tags: [production, batch]
---
```python
import json, os

def run_batch(items, process, path):
    done = 0
    if os.path.exists(path):
        with open(path) as f:
            done = json.load(f)["done"]         # resume after the last finished item
    for i in range(done, len(items)):
        process(items[i])
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump({"done": i + 1}, f)
        os.replace(tmp, path)                   # atomic: never a half-written checkpoint
```

- Use it for long batch scoring, backfills and training loops that may crash or be stopped.
- Key rule: do the work, then save the position. Save it atomically.
- Say: "A crash between work and save repeats one item, so the work must be idempotent."

<!-- more -->

## Details

```python
import tempfile

path = os.path.join(tempfile.mkdtemp(), "ckpt.json")
seen, fail_once = [], {"c"}

def process(x):
    if x in fail_once:
        fail_once.discard(x)
        raise RuntimeError("crash")
    seen.append(x)

try:
    run_batch(["a", "b", "c", "d"], process, path)
except RuntimeError:
    pass
seen                                             # ['a', 'b']   crashed on "c"
# the second run reads the checkpoint and starts at "c"
run_batch(["a", "b", "c", "d"], process, path)
seen                                             # ['a', 'b', 'c', 'd']
```

**Order of the two steps.** Work then save gives *at-least-once*: after a crash the last item may run again. Save then work gives *at-most-once*: an item can be lost. At-least-once with idempotent work is the usual choice.

**How often.** Saving after every item is safe and slow. Saving every N items or every chunk is faster, and a restart repeats at most N items.

**Same input.** A position is only valid for the same input in the same order. Store a fingerprint of the input (file name, row count, a hash) in the checkpoint and refuse to resume if it differs.

**What to store.** Enough to continue: the position, partial totals, the model version. Keep it small and in JSON so a person can read it.

**When finished.** Delete or mark the checkpoint, or the next fresh run will skip everything.

## Common mistakes

- Saving the position before the work is done, then losing an item on a crash.
- Writing the checkpoint with a plain `open(path, "w")`: a crash during the write corrupts it.
- Off-by-one: saving `i` instead of `i + 1` repeats an item on every restart.
- Resuming over an input that changed or was re-sorted.
- Leaving an old checkpoint in place, so a new run silently does nothing.

## See also

- [Atomic file writes](#/kb/prod-atomic-write)
- [Idempotency and idempotency keys](#/kb/prod-idempotency)
- [Chunked batch processing and isolating bad records](#/kb/prod-chunked-batch-processing)
