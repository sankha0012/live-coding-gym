```python
from datetime import datetime


def time_split(rows, cutoff, gap_days=0):
    """Split rows by event time. Train is at least `gap_days` before cutoff,
    test is at or after cutoff. Rows in the gap are dropped."""
    train, test = [], []
    for row in sorted(rows, key=lambda r: r["ts"]):
        age = (cutoff - row["ts"]).days
        if row["ts"] >= cutoff:
            test.append(row)
        elif age >= gap_days:
            train.append(row)
    return train, test


if __name__ == "__main__":
    rows = [
        {"ts": datetime(2026, 1, d), "y": d % 2, "label_ts": datetime(2026, 1, d + 3)}
        for d in range(1, 21)
    ]
    cutoff = datetime(2026, 1, 15)
    train, test = time_split(rows, cutoff)
    print(len(train), len(test), train[-1]["ts"].day, test[0]["ts"].day)
    train, test = time_split(rows, cutoff, gap_days=3)
    print(len(train), len(test), train[-1]["ts"].day)
    print(time_split([], cutoff))
    for g in (0, 3):
        train, _ = time_split(rows, cutoff, gap_days=g)
        leaked = [r for r in train if r["label_ts"] > cutoff]
        print("gap", g, "labels known only after cutoff:", len(leaked))
```

Explain this code as you would to the interviewer after finishing it: what it does, how, complexity, one risk.
