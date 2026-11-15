**Why this matters.** A wrong average looks plausible, so nobody questions it. This function is wrong in three ways, and the first two give a believable number, not a crash.

**How we get there.**
1. Reproduce. Delivered 25 and 35 plus one cancelled should give 30, but the code gives 20.
2. Locate the first bug: nothing filters on status, so the cancelled order is counted. We keep only `o["status"] == "delivered"`.
3. Locate the second: `or 0` turns a missing time into a zero, and the order still counts in `len(orders)`. A missing value is not zero minutes, so we skip it with `is not None`.
4. Divide by the length of the cleaned list, not the original one, so the numerator and denominator describe the same rows: `sum(d) / len(d)`.
5. Locate the third: with no rows left, we would divide by zero. The spec says return `None`, so we check `if not d` first.

**Check it.** An empty list and a list of only cancelled orders both return `None`.

**Watch out.** Fixing only the filter leaves the denominator wrong. When a number looks off, ask which rows the top and the bottom of the fraction are counting.
