**Why this matters.** Streams usually deliver at least once, and not in order. The same event can arrive twice, and a late "picked_up" can show up after "delivered". Processing has to give the same state however the events are shuffled or replayed.

**How we get there.**
1. Keep a `seen` set of event ids. If an id is already there, count a duplicate and skip it; otherwise add it.
2. Give every event a sort key `(ts, event_id)`. Tuples compare element by element, so a larger timestamp wins, and on a tie the larger id wins (ids compare as strings, so `"e9"` beats `"e10"`).
3. For each order, keep only the best `(key, status)` seen so far in a dict.
4. When an event arrives, replace the stored entry only if there is none yet or the new key is larger.
5. Finally return `{order_id: status}` plus the duplicate count.

**Check it.** Reversing the input gives the same answer, which is exactly the property we want. One pass, with memory for the seen ids and the orders.

**Watch out.** Trusting arrival order ("last one wins") instead of the timestamp, or leaving ties undecided so the result depends on input order.
