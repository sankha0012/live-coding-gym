**Why this matters.** Joining a list of lists into one list is an everyday chore: pages of results, batches, grouped rows. The trap is how much to flatten: here only one level, so inner lists inside an inner list must survive.

**How we get there.**
1. Start with the plain loop idea: for each inner list, take each item and add it to the output.
2. Turn that into a comprehension. The outer `for` picks an inner list, and the second `for` picks an item from it.
3. The reading order is the same as the loops: `[x for inner in lists for x in inner]`. The first `for` is the outer loop.
4. Because we only ever step into one inner list, a list nested deeper is just an item and is copied across untouched.

**Check it.** An empty outer list gives an empty result, and empty inner lists add nothing, so no special cases appear. The cost is linear in the total number of items, and the input is only read, never changed.

**Watch out.** Writing a recursive flatten, or putting the two `for` clauses in the wrong order, gives a different problem or a `NameError`.
