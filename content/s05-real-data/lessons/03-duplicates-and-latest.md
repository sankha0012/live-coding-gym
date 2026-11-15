# Duplicates and keeping the latest

## What it is

The same real-world thing appears in the table more than once. Sometimes it is an exact copy, from a retried request or a double load. Sometimes it is several versions of one record, such as a customer whose plan changed. Deduplicating means choosing what makes two rows "the same" and which copy wins. See [sorting and dedupe](#/kb/pd-sort-dedupe) and [event dedup and ordering](#/kb/prod-event-dedup-ordering).

## How it breaks in production

- **Double counting.** A retried payment event is stored twice and revenue is too high.
- **Wrong winner.** `drop_duplicates` keeps the first row in the current order. If the table is not sorted, you may keep the stale version of a customer.
- **Wrong key.** Deduplicating on whole rows misses two versions of one order, because the status differs. Deduplicating on a too-short key merges different things.
- **Ties.** Two versions with the same timestamp make the winner depend on row order, so two runs can differ.

## The defence in code

```python
import pandas as pd

ev = pd.DataFrame({
    "customer_id": [1, 1, 2, 2],
    "updated_at": pd.to_datetime(["2026-01-02", "2026-01-05", "2026-01-03", "2026-01-03"]),
    "plan": ["free", "pro", "free", "free"],
})

print(ev.drop_duplicates("customer_id")["plan"].tolist())   # keeps first row

def latest_per_key(df, key, ts):
    return (df.sort_values([key, ts], kind="stable")
              .drop_duplicates(key, keep="last"))

print(latest_per_key(ev, "customer_id", "updated_at"))
print(ev.duplicated().tolist())
print(ev.duplicated("customer_id", keep=False).tolist())
```

The naive call returns `['free', 'free']`, so customer 1 keeps the stale January 2 row because it happens to come first. Sorting by key and timestamp and keeping the last row is deterministic, and the stable sort keeps ties in their input order. `duplicated()` with no arguments flags the fourth row as an exact copy, and `keep=False` marks every row sharing a key so you can inspect them before deleting anything. If two versions can tie, add a second sort column such as a sequence number.

## What to say in the interview

"First I decide what identifies a record, and whether duplicates are exact copies or versions. For versions I sort by key and timestamp and keep the last one, with a tiebreaker column so the result is the same on every run. I look at the duplicates with `keep=False` before dropping them, and I log how many rows were removed."
