**Why this matters.** A model that predicts the future must be tested on the future. A random split lets later orders leak into training, so the score looks better than reality. We split by time instead: the past trains, the future tests.

**How we get there.**
1. `created_at` is text, and comparing text to a date is fragile, so first parse it: `ts = pd.to_datetime(orders["created_at"])`. We do not write it back, so `created_at` stays as it came.
2. Turn the cutoff into a timestamp with `pd.Timestamp(cutoff)`. A string like `"2026-10-01"` means midnight at the start of that day.
3. Build one mask: `before = ts < cutoff`. The strict sign means an order exactly at midnight is not before the cutoff.
4. Return `orders[before]` as train and `orders[~before]` as test, each with `.copy()`. Using the mask and its negation means every row lands in exactly one side, with no overlap and nothing lost.

**Check it.** Boolean selection keeps the original order and all columns. The cost is linear.

**Watch out.** Writing two separate conditions can go wrong at the cutoff: `<` with `>` drops the order sitting exactly on it, and `<=` with `>=` puts it on both sides.
