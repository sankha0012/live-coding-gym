# Duplicate events inflating metrics

## What it is

Most message queues and event pipelines promise at-least-once delivery. That means a consumer may receive the same event twice: after a retry, a restart, or a replay. If the code counts every arrival, the metric is inflated. Deduplication means keeping one record per unique event id. See [event dedup and ordering](#/kb/prod-event-dedup-ordering) and [idempotency](#/kb/prod-idempotency).

## How it breaks in production

Revenue appears 3 percent higher after a pipeline restart. A click-through rate doubles for an hour. A feature such as "orders in the last 7 days" counts the same order twice, so the model sees inflated activity during exactly the incidents when retries are frequent. None of this throws an error, and the duplicated data may even be written into the training set. Two extra traps: choosing the key badly (an id that is not truly unique drops real events), and ignoring which copy to keep when the duplicates differ, for instance a later correction of an earlier event.

## The defence in code

Keep the first or the latest event per id, and decide explicitly which. Here we keep the one with the latest update time, and make the output order deterministic. See [sort and dedupe](#/kb/pd-sort-dedupe).

```python
import pandas as pd

events = pd.DataFrame({
    "event_id": ["a", "b", "a", "c", "b"],
    "amount": [10.0, 5.0, 10.0, 7.0, 6.0],
    "updated_at": pd.to_datetime(
        ["2026-11-15 10:00", "2026-11-15 10:01", "2026-11-15 10:02",
         "2026-11-15 10:03", "2026-11-15 10:04"]),
})

clean = (events.sort_values(["event_id", "updated_at"])
               .drop_duplicates("event_id", keep="last")
               .reset_index(drop=True))

assert events["amount"].sum() == 38.0      # inflated
assert clean["amount"].sum() == 23.0       # a=10, b=6, c=7
assert clean["event_id"].tolist() == ["a", "b", "c"]
print(clean)
```

Also count how many duplicates you dropped. A sudden rise in that count is a useful alarm: it points to a retry storm or a replay upstream.

## What to say in the interview

"If events can arrive more than once, I deduplicate by a unique event id before computing any metric or feature, and I decide explicitly whether to keep the first or the latest copy. I sort first so the result is deterministic, and I log how many duplicates I removed, because a spike there signals an upstream retry problem. I would also make the processing idempotent so a replay cannot double-count."
