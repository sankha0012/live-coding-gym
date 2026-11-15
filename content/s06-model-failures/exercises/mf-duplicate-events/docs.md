# dedupe_events reference

## Contract

`dedupe_events(events) -> tuple[list[dict], int]`

`events` is a list of dicts, each with a hashable `"id"`. For each id the first event is kept and later ones are dropped, even when their other fields differ. Kept events stay in original order. The result is `(unique, duplicates)` where `duplicates` is the number of events dropped.

Ids are compared by Python equality and hashing, so `1` and `"1"` are different ids. Falsy ids such as `0` and `""` are ordinary ids and are deduplicated like any other. An empty list returns `([], 0)`. The input list and its dicts are not modified.

```
dedupe_events([{"id": "a", "v": 1}, {"id": "b"}, {"id": "a", "v": 2}])
# ([{"id": "a", "v": 1}, {"id": "b"}], 1)
```

## Library notes

- `set.add(x)` and `x in s`: average O(1). Items must be hashable, otherwise `TypeError: unhashable type`.
- `dict.fromkeys(iterable) -> dict`: keeps the first insertion order. Gotcha: every key gets the same value, so it cannot carry the events themselves.
- `dict.setdefault(key, default) -> value`: inserts only when the key is absent and returns the stored value.
- Gotcha: `1 == 1.0 == True`, and they hash alike, so a set treats them as the same id.

## Gotchas

- Scanning the kept list for each event is O(n squared). Use a set of seen ids.
- Keeping the first event is a choice. For updates you may want the latest version, so confirm which one the stream expects.
- Deduplicating per batch misses duplicates that arrive in a later batch. Real systems keep ids across a time window.
