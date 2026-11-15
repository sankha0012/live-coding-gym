**Why this matters.** Averages over data with missing values go wrong quietly. If you divide by the number of rows instead of the number of real values, every None drags the average down.

**How we get there.**
1. Keep two dicts, `total` and `count`, both with defaults (`defaultdict(float)` and `defaultdict(int)`), so we can add without checking if the key exists.
2. Keep a `seen` set of every customer, because a customer whose values are all None must still appear in the answer.
3. For each row, add the customer to `seen`. Only if `v is not None` do we add to `total` and bump `count`. We test `is not None` so a real value of 0 still counts.
4. Build the result from `seen`: `total[cid] / count[cid] if count[cid] else None`. The `if` avoids dividing by zero.

**Check it.** An empty input gives `{}`. We do a single pass, so the cost is linear in the number of rows.

**Watch out.** Dividing by the total number of rows, or building the result only from customers with values, loses the denominator rule and the None customers.
