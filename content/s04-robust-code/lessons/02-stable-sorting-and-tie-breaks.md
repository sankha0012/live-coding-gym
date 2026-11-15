# Stable sorting and tie-breaks

## What it is

A sort is stable when items with equal keys keep the order they had in the input. Python's `sorted` and `list.sort` are always stable. A tie-break is an extra part of the sort key that decides between items the main key cannot separate, so the final order depends on the data and not on how it arrived. See [Sorting](#/kb/py-sorting) and [Sort and dedupe in pandas](#/kb/pd-sort-dedupe).

## How it breaks in production

Stability only helps if the input order is itself fixed, and in production it often is not. Rows come back from a database without an ORDER BY, from a set, from a thread pool or from files read in directory order. Two rows tie on score, the one that comes first wins a top-k slot, and the ranking differs between two runs. The same thing happens with `max` and `min`, which return the first of several equal items, and with `heapq.nlargest`. In pandas, `sort_values` defaults to quicksort, which is not stable, so ties can swap between versions or machines unless you pass `kind="stable"` or sort by several columns. The visible symptom is a leaderboard, a top-k recommendation list or a deduplication that changes between two identical runs.

## The defence in code

```python
rows = [
    {"id": "b", "score": 0.9},
    {"id": "a", "score": 0.9},
    {"id": "c", "score": 0.5},
]


def top_k(rows, k):
    # highest score first, then smallest id: a total order, no ties left
    return sorted(rows, key=lambda r: (-r["score"], r["id"]))[:k]


first = top_k(rows, 2)
second = top_k(list(reversed(rows)), 2)   # same data, different arrival order
assert first == second
assert [r["id"] for r in first] == ["a", "b"]
print([r["id"] for r in first])
```

The key is a tuple. The score is negated so that larger comes first while the id still sorts ascending. Because the id is unique, no two rows are equal and the order is fully determined. The test shuffles the arrival order and checks the answer does not move, which is the property that matters. For pandas, the equivalent is `df.sort_values(["score", "id"], ascending=[False, True])`.

## What to say in the interview

"Python's sort is stable, but that only preserves the input order, and my input order may not be deterministic. So I add a unique tie-break to the key, here the id, and I negate the score for descending order. Then the output is a function of the data alone. I test it by feeding the same rows in two different orders and asserting the same result."
