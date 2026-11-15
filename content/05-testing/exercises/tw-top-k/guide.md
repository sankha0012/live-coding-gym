**Why this matters.** Top-k is everywhere in ranking and reports. The bugs hide in ties, in odd values of `k`, and in silently reordering the caller's data.

**How we get there.**
1. Test the main case: the two highest of three pairs come back best first.
2. Test ties with names that are not in alphabetical order, `[("z", 2), ("a", 2), ("m", 9), ("b", 2)]` with `k=3`. The answer must keep `z` before `a`. A version that also sorts by name puts `a` first.
3. Test `k` larger than the list, which returns everything. The first test already catches a slice of `k + 1`, since it would return one pair too many.
4. Test `k = 0` and `k = -1`. A guard for only `k == 0` lets `-1` through, and a negative slice then returns the wrong pairs.
5. Test the empty list, then check the input list is the same afterwards. Sorting it in place changes data somewhere else.

**Check it.** `sorted` is stable and costs `n log n`.

**Watch out.** Ties with names already in alphabetical order will not reveal an extra sort by name.
