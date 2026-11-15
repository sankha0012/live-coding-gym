**Why this matters.** You cannot tell whether a character is unique until you have seen the whole string. That is why "first" and "unique" pull in opposite directions, and why one pass is not enough.
**How we get there.**
1. First pass: count every character with `Counter(s)`. Now we know the total for each one.
2. Second pass: walk the string again with `enumerate(s)`. Walking the original string, not the counter, is what gives us "first" for free.
3. Return the index `i` of the first character whose count is exactly 1.
4. If the loop ends without a hit, nothing is unique, so return `-1`.
**Check it.** `"aabb"` returns `-1`, and so does an empty string because both loops do nothing. Case matters because `"a"` and `"A"` are different keys. Two passes over n characters give O(n) time, and the counter holds at most one entry per distinct character.
**Watch out.** Ending the function with a fallback of `0` or `len(s) - 1` looks plausible, but it reports an index when no character is unique, so `"aabb"` fails.
