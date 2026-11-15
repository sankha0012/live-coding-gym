# Late and out-of-order events

## What it is

Events do not arrive in the order they happened. A phone sends a click when it gets network again, a queue retries a message, two services have different delays. Each event has an event time (when it happened) and an arrival time (when you received it). Delivery is usually at least once, so duplicates arrive too. See [event dedup and ordering](#/kb/prod-event-dedup-ordering).

## How it breaks in production

- **Order by arrival.** Computing "time since the previous event" in arrival order gives negative gaps.
- **Last write wins by accident.** An old update that arrives late overwrites a newer state.
- **Closed windows change.** Yesterday's totals were published, then late events arrive and the numbers move.
- **Retries create duplicates.** The same event id appears twice and is counted twice.

## The defence in code

```python
import pandas as pd

ev = pd.DataFrame({
    "event_id": ["a", "b", "c", "a", "d"],
    "ts": pd.to_datetime(["2026-05-01 10:00", "2026-05-01 10:05", "2026-05-01 10:01",
                          "2026-05-01 10:00", "2026-05-01 09:00"]),
    "arrived": pd.to_datetime(["2026-05-01 10:00", "2026-05-01 10:05", "2026-05-01 10:06",
                               "2026-05-01 10:07", "2026-05-02 08:00"]),
})

def accept(df, watermark_minutes=60):
    df = df.drop_duplicates("event_id", keep="first")
    late = (df["arrived"] - df["ts"]) > pd.Timedelta(minutes=watermark_minutes)
    return df[~late].sort_values("ts"), df[late]

ok, late = accept(ev)
print(ok["event_id"].tolist(), late["event_id"].tolist())   # ['a', 'c', 'b'] ['d']
print(ev["ts"].is_monotonic_increasing)                     # False
```

The function drops repeated event ids, then splits events into accepted ones and those that arrived more than the allowed delay (the watermark) after they happened. Event `d` happened at 09:00 and arrived the next morning, so it goes to a separate late bucket instead of silently changing old results. Accepted events are sorted by event time, so `c` (10:01) comes before `b` (10:05) even though it arrived after. The `False` shows that the raw table is not in event order, so any "previous event" logic must sort first. Late events can still be reprocessed in a batch correction, but that is a decision, not an accident.

## What to say in the interview

"I separate event time from arrival time, and I never assume the input is sorted. I deduplicate by event id, sort by event time before computing gaps or state, and apply a version rule so an older update cannot overwrite a newer one. For late data I choose a watermark and send anything later to a side table, so published numbers do not change silently."
