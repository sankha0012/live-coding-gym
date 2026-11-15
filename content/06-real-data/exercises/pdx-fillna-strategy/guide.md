**Why this matters.** Missing values have to be filled before most models run, but one global number is a poor guess: a pizza place and a sushi bar have different typical orders. So we fill each gap with a value from the same restaurant, and keep a safety net for restaurants with no data at all.

**How we get there.**
1. Start from `orders.copy()` so the input is untouched.
2. `out.groupby("restaurant_id")["subtotal"].transform("median")` gives every row the median of its own restaurant. `transform` returns a series aligned to the original index, so rows keep their order and index. The median skips missing values by default.
3. `out["subtotal"].fillna(per_restaurant)` fills each gap with that value. Known subtotals are not touched.
4. A restaurant with no known subtotal has a median of NaN, so some gaps remain. A second `.fillna(out["subtotal"].median())` fills those from the whole column.

**Check it.** A frame with nothing missing, or no rows, comes back unchanged. It is one pass over the data.

**Watch out.** Using the mean lets one huge order drag every fill upward, and filling everything with the global median ignores the per-restaurant rule.
