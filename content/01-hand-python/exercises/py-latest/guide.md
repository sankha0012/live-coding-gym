**Why this matters.** Event logs arrive unsorted, and what we want is the current state of each order. The tempting route is to sort everything first, but we do not need the whole order, only the winner per key.

**How we get there.**
1. Keep a dict `best` that maps each order id to the pair `(timestamp, status)` of the newest event seen so far.
2. For each event, unpack `oid, ts, status` right in the loop header.
3. If the order is new, or this timestamp is larger than the stored one, replace the entry: `if oid not in best or ts > best[oid][0]`.
4. At the end, drop the timestamps: `{oid: s for oid, (ts, s) in best.items()}`.

**Check it.** An empty list gives `{}`. Events can come in any order because we compare timestamps, not positions. It is one pass, O(n), with no sorting. If two events tie on timestamp, the first one seen is kept, since we use a strict `>`.

**Watch out.** Taking the last event in the list instead of the one with the largest timestamp breaks as soon as the input is unsorted.
