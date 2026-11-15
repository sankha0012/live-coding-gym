**Why this matters.** Two-sum is the textbook example of trading memory for speed. Testing every pair is O(n squared); remembering what you have seen turns the question into a lookup.
**How we get there.**
1. For a number `x` at position `j`, a partner must equal `target - x`. So instead of searching all pairs, we ask one question per number.
2. Keep a dict `seen` from value to the index where we saw it. Dict lookups are fast.
3. Walk with `enumerate`. If `target - x in seen`, return `[seen[target - x], j]`. The stored index is always earlier than `j`, so the order `i < j` holds.
4. If not, store `seen[x] = j` and continue. Storing after checking means a position can never pair with itself.
5. If the loop ends, return `None`.
**Check it.** `[2, 2, 8]` with target 10 returns `[1, 2]`: the second 2 overwrites the first in the dict, so we get the largest `i`. The first `j` that finds a partner is the smallest `j`. It is one pass, O(n) time and O(n) space.
**Watch out.** Storing `x` before the check allows a number to pair with itself, and returning values instead of indices answers a different question.
