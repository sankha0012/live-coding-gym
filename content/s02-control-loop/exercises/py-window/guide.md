**Why this matters.** "Peak load in any 60-minute window" is a rate-limit and capacity question. Checking every possible window is slow; a sliding window does it in one sweep.

**How we get there.**
1. Sort the timestamps. Now a window is a contiguous slice of the list.
2. Use two pointers: `right` moves over every index, `left` marks where the current window starts.
3. For each `right`, move `left` forward while `ts[right] - ts[left] >= w`. A window `t` to `t+59` holds differences up to 59, so a difference of 60 no longer fits.
4. The window now holds `right - left + 1` orders. Keep the biggest in `best = max(best, ...)`.

**Check it.** An empty list gives 0, and one timestamp gives 1. In `[0, 10, 59, 60, 61, 200]` the best window is 10 to 69, with 4 orders. Each index enters and leaves once, so after the sort it is O(n).

**Watch out.** Using `> w` instead of `>= w` lets a window span 61 minutes, so `[0, 60]` counts 2 instead of 1.
