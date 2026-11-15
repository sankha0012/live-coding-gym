**Why this matters.** Comparing each item with its neighbour is how we find gaps, changes and trends. The usual trap is an index that runs off the end of the list.

**How we get there.**
1. We want each item together with the next one. Picture the list twice, the second copy shifted left by one place.
2. `items[1:]` is exactly that shifted copy: it starts at the second item.
3. `zip` walks two sequences side by side and stops when the shorter one ends. The shifted copy is one shorter, so the last item never looks for a neighbour.
4. `zip` gives lazy tuples, so wrap it in `list(...)`: `list(zip(items, items[1:]))`.

**Check it.** An empty list and a single item both give `[]`, since the slice is empty and `zip` yields nothing. Time is linear, with extra space for the slice copy. For huge input `itertools.pairwise` avoids that copy.

**Watch out.** A loop with `items[i + 1]` over `range(len(items))` fails with `IndexError` on the last item.
