**Why this matters.** Overlapping shifts, bookings and meetings all reduce to merging intervals. The insight is that sorting by start puts every overlap next to its neighbour, so we only ever compare with the last merged interval.

**How we get there.**
1. Sort the shifts with `sorted(shifts)`. Lists compare by start first, so the earliest start comes first.
2. Keep a `merged` list, empty at first.
3. For each `s, e`, if `merged` has something and `s <= merged[-1][1]`, the shift overlaps or touches the last one, so we extend it.
4. Extend with `max(merged[-1][1], e)`, not just `e`, because a shift can sit entirely inside a longer one.
5. Otherwise start a new interval with `merged.append([s, e])`.

**Check it.** An empty input returns `[]`. Shifts given in reverse order still work because of the sort. The sort dominates, so it is O(n log n). Our merged entries are fresh lists, so the input is not changed.

**Watch out.** Setting the end to `e` instead of the max shrinks the merged shift when `[2, 3]` sits inside `[1, 5]`.
