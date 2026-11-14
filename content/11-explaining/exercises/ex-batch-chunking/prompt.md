```python
from itertools import islice


def chunks(items, size):
    """Yield lists of at most `size` items from any iterable."""
    if size < 1:
        raise ValueError("size must be >= 1")
    it = iter(items)
    while True:
        batch = list(islice(it, size))
        if not batch:
            return
        yield batch


def score_all(rows, model, batch_size=64):
    """Score rows in batches. Returns scores in the same order as rows."""
    scores = []
    for batch in chunks(rows, batch_size):
        out = model(batch)
        if len(out) != len(batch):
            raise RuntimeError(
                f"model returned {len(out)} scores for {len(batch)} rows"
            )
        scores.extend(out)
    return scores


def fake_model(batch):
    return [len(r) * 0.1 for r in batch]


if __name__ == "__main__":
    rows = ["a", "bb", "ccc", "dddd", "eeeee"]
    print(list(chunks(rows, 2)))
    print(score_all(rows, fake_model, batch_size=2))
    print(list(chunks([], 3)))
    print(score_all(iter(rows), fake_model, batch_size=10))
    try:
        score_all(rows, lambda b: b[:-1], batch_size=2)
    except RuntimeError as e:
        print("error:", e)
```

Explain this code as you would to the interviewer after finishing it: what it does, how, complexity, one risk.
