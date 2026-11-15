**Why this matters.** Removing duplicates sounds easy, but the spec makes three promises at once: first occurrence wins, order is kept, and the caller's list is left alone. Each easy implementation breaks one of them.

**How we get there.**
1. Test that duplicates go away, `[1, 1, 1]` becomes `[1]`.
2. Test order with an unsorted input with scattered repeats, `[3, 1, 2, 3, 1]` giving `[3, 1, 2]`. `list(set(items))` does not promise any order, so it can fail here.
3. The same test catches a version that keeps the last occurrence, because it would produce `[2, 3, 1]`.
4. Test that the input is not mutated. Copy the data into a variable, call the function, then compare the variable. A version that pops items out of the input fails.
5. Test the result is a different list object, even when nothing was removed, and add the empty list.

**Check it.** The correct version keeps a `seen` set and an output list, so it is linear in time and uses extra space for both.

**Watch out.** Returning the input itself when there are no duplicates passes every value check. Only `is not` catches it.
