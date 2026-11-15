**Why this matters.** "Second highest" sounds like index 1 of a sorted list, but duplicates break that. In `[5, 5, 3]` the second highest distinct value is 3, not 5.

**How we get there.**
1. Remove duplicates with `set(values)`. Now every value appears once.
2. Sort the distinct values from largest to smallest: `sorted(..., reverse=True)`. We store this as `distinct`.
3. If there are fewer than two distinct values there is no second one, so we return `None`. That covers an empty list and a list like `[7, 7]`.
4. Otherwise the answer is `distinct[1]`.

The whole thing is `distinct[1] if len(distinct) >= 2 else None`.

**Check it.** `[]` and all-equal lists both give `None`. The sort makes it O(n log n). You could track the top two values in one pass for O(n), but the set version is easier to read and to get right.

**Watch out.** Sorting without deduplicating returns the maximum again when it appears twice.
