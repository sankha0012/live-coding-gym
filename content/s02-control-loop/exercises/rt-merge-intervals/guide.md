**Why this matters.** Merging time ranges is what calendars and booking systems do: overlapping meetings become one busy block. Unsorted input would make you compare every pair, so the first move is to put it in order.
**How we get there.**
1. Sort the intervals by start with `sorted(intervals)`. This returns a new list, so the caller's list is untouched. After sorting, an interval can only overlap the one just before it in the result.
2. Keep a `merged` list and walk the sorted intervals as `start, end`.
3. If `start <= merged[-1][1]`, it overlaps or touches the last block, so we extend: `merged[-1][1] = max(merged[-1][1], end)`.
4. Otherwise it is separate, so `merged.append([start, end])`. We append a fresh list, not the original one, so we never share objects with the input.
**Check it.** `[1, 2]` and `[2, 3]` merge because we use `<=`. In `[1, 10], [2, 3]` the max keeps the end at 10. Sorting costs O(n log n) and the scan O(n).
**Watch out.** Using `<` misses touching intervals, taking `end` without `max` shrinks a block that contains another, and appending the input list itself lets later edits change the caller's data.
