**Why this matters.** Plain binary search finds some match. With duplicates you need the first one, and that small change is where off-by-one bugs live. Interviewers ask this exactly because it exposes shaky loop boundaries.
**How we get there.**
1. Keep a window `lo` to `hi` where `hi` is exclusive, starting as `0` and `len(nums)`. The loop runs while `lo < hi`.
2. Look at `mid = (lo + hi) // 2`. If `nums[mid] < target`, the target cannot be at mid or left of it, so `lo = mid + 1`.
3. Otherwise mid might be the answer or something to its left, so `hi = mid`. We do not return on a match; equal values stay in the window and we keep squeezing left.
4. When the window closes, `lo` is the first position whose value is not smaller than the target. It might be past the end or hold a bigger number, so we check `lo < len(nums) and nums[lo] == target`, else return `-1`.
**Check it.** An empty list never enters the loop, and the final check returns `-1`. Each step halves the window, so it is O(log n) time and O(1) space.
**Watch out.** Returning as soon as `nums[mid] == target` gives a correct match but not the leftmost one.
