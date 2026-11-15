**Why this matters.** "Have we seen this before?" shows up everywhere: new versus returning customers, duplicates, first events. The right tool is a set, because asking whether something is in it is a quick lookup.

**How we get there.**
1. Keep a `seen` set and an output list `out`.
2. For each customer, decide the label first: `"returning" if c in seen else "new"`. Membership in a set takes constant time on average.
3. Append that label to `out`.
4. Only after deciding, do `seen.add(c)`. If we added first, every customer would look returning on their very first order.

**Check it.** An empty list gives `[]`. The result has one label per order, in the same order as the input, so a customer who buys three times gets one `new` and two `returning`. One pass, O(n). Using a list for `seen` would turn each lookup into a scan and make it quadratic.

**Watch out.** Adding the customer to `seen` before checking marks every first purchase as returning.
