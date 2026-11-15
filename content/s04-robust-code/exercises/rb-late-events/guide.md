**Why this matters.** A queue gives no promise of order or uniqueness. An old "pending" can show up after "shipped", and the same event can be delivered twice. If we just take the last arrival, the entity ends up in the wrong state.

**How we get there.**
1. Keep a `seen` set of event ids. An id already in the set is a repeat, so we skip it; otherwise we add it. This makes the first copy the only one that counts.
2. Keep a dict `best` that maps each entity to its best event so far.
3. For a new event, look up the current best for its entity. Event time decides, not arrival: replace it when `e["ts"] >= cur["ts"]`.
4. The `>=` settles ties. With equal timestamps, the event that appears later in the list replaces the earlier one, as required.
5. At the end, build `{entity: e["state"]}` from the winners.

**Check it.** An empty list gives `{}`. One pass, with memory for the seen ids and the entities.

**Watch out.** Letting the last arrival win ignores timestamps, skipping the dedupe lets repeats influence ties, and `>` instead of `>=` breaks the tie rule.
