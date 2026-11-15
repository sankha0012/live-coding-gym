## Contract

`final_state(events) -> dict`.

Each event is a dict `{"id": str, "entity": str, "ts": int, "state": str}`. Events may arrive out of order, and the same event may appear more than once. The result maps each entity to a state string. An empty list returns `{}`.

- Events with the same `id` are duplicates. Only the first one in list order is kept, even if the later copy has a different `ts`, `entity` or `state`.
- Among the remaining events of one entity, the highest `ts` wins. Timestamps may be zero or negative.
- If two remaining events of one entity share the highest `ts`, the one appearing later in the list wins. The id and the state text play no part in that choice.
- Entities are independent, and the same `ts` in different entities means nothing.
- The input list and its dicts are not modified.

Example: `[{"id":"2","entity":"a","ts":5,"state":"shipped"}, {"id":"1","entity":"a","ts":2,"state":"new"}]` gives `{"a": "shipped"}`.

## Library notes

- `set.add(x)` returns `None`; `x in s` is a constant-time membership test for hashable values.
- `dict.get(k, default)` returns the value or the default without raising `KeyError`.
- `enumerate(seq)` yields `(index, item)` pairs and is useful when list position matters.
- `max(items, key=f)` returns the first of several equal maxima, which matters for ties.

## Gotchas

- Real queues deliver at least once, so dedupe on a unique event id before applying anything.
- Arrival order is not event order; trust the event timestamp, and decide explicitly what a tie means.
- Mutating incoming events makes replays and debugging unreliable.
