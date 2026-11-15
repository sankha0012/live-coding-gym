**Why this matters.** When a sender retries, the same event arrives twice, and counting both inflates every metric downstream. We drop the repeats without disturbing anything else.

**How we get there.**
1. Keep a `seen` set of ids. Asking "have I met this id?" is a constant-time check, so we never compare each event with all earlier ones.
2. Walk the events in their original order. If the id is already in `seen`, skip the event.
3. Otherwise add the id to `seen` and append the event to `unique`. We only ever append, so the order is kept and the first event for each id wins, even if a later one has different fields.
4. The number dropped is `len(events) - len(unique)`, so it cannot drift out of sync with the list.

**Check it.** An empty list gives `([], 0)` with no special case, and the input is never touched. Time is linear, extra space is one entry per unique id.

**Watch out.** Rebuilding through a dict or set can lose the order or keep the last event instead of the first, and counting distinct ids is not the same as counting dropped events.
