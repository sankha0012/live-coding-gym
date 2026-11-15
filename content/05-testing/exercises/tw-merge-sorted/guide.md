**Why this matters.** Merging two sorted lists is the heart of merge sort. A good test file has to check the subtle promises: stability, leftovers, and not damaging the inputs.

**How we get there.**
1. Start with a plain interleave, keys 1 and 4 against 2 and 3, to see the basic merge work.
2. Test equal keys. Put the same key in both lists with labels that are not in alphabetical order, `(1, "z")` in `a` and `(1, "a")` in `b`. The answer must have `a` first. A version that takes `b` on ties, or sorts by label too, gives the opposite order.
3. Test leftovers in both directions: one case where `a` runs out first and one where `b` does. A version that only appends the rest of `a` loses data in the second case.
4. Test empty inputs on each side and both together.
5. Compare both input lists afterwards. A version that pops from its arguments destroys them.

**Check it.** The correct merge walks both lists once with two indexes, so it is linear in the total length.

**Watch out.** Picking labels that happen to be in sorted order makes the stability bug invisible.
