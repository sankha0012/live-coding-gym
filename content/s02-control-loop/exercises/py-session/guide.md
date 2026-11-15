**Why this matters.** Analytics groups raw events into sessions: a long enough pause means the user left. The traps are unsorted timestamps and the exact boundary, since a gap of exactly 30 is still the same session.

**How we get there.**
1. Return `[]` for empty input, because we are about to read `ts[0]`.
2. Sort first: `ts = sorted(timestamps)`. Gaps only make sense between neighbours in time.
3. Start with the first timestamp as the first session: `sessions = [[ts[0]]]`.
4. For each later `t`, compare it with the last event of the current session, `sessions[-1][-1]`.
5. If `t - sessions[-1][-1] > gap`, open a new session with `sessions.append([t])`. Otherwise add `t` to the current one.

**Check it.** `[0, 30, 60]` stays one session, because 30 is not greater than 30. The sort dominates, so it is O(n log n), and the scan is linear.

**Watch out.** Using `>=` splits sessions at exactly 30 minutes, and skipping the sort mis-groups events that arrive out of order.
