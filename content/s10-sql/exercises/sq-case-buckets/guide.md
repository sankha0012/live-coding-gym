**Why this matters.** Turning a number into labels such as small, medium and large is how we build reports from raw values. The trap is order: a CASE stops at the first branch that matches, and NULL behaves in a surprising way.

**How we get there.**
1. Write a `CASE` that returns a label for each row. Branches are tried from top to bottom.
2. Put `WHEN subtotal IS NULL THEN 'unknown'` first. A comparison like `subtotal < 42` is never true for NULL, so NULL would slip past every number test and land in `ELSE`, which is 'large'.
3. Then `WHEN subtotal < 42 THEN 'small'` and `WHEN subtotal < 83 THEN 'medium'`. Because small was already caught, the second test only sees 42 and above, so we do not need to write both ends.
4. `ELSE 'large'` covers 83 and up.
5. Name the CASE `bucket`, then `GROUP BY bucket` and `COUNT(*)`.

**Check it.** The edges are half open: 42 is medium and 83 is large. It is one pass, linear in the number of orders.

**Watch out.** Checking NULL last, or not at all, quietly counts unknown subtotals as large.
