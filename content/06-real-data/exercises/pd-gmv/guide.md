**Why this matters.** GMV is the first number a marketplace reports, so a small slip repeats everywhere. Two things hide here: which orders count, and what a missing value does to a sum.

**How we get there.**
1. Keep only `status == "delivered"` and take a copy. Cancelled orders never brought in money.
2. Build the order value. In pandas, a missing number plus a number is missing, so `subtotal + delivery_fee` would erase the whole order. We use `d["subtotal"].fillna(0) + d["delivery_fee"]`, as the spec says to treat a missing subtotal as 0.
3. Merge the city from `restaurants` with a left join on `restaurant_id`, so no order is dropped.
4. Group by `city` and sum the value column.
5. Sort descending with `sort_values(ascending=False)` to get the largest city first.

**Check it.** The result is a Series indexed by city. The sort dominates the cost, so O(n log n). The input frames are untouched because we worked on a copy.

**Watch out.** Adding without `fillna` makes orders with a missing subtotal vanish from the sum, and skipping the status filter inflates GMV with cancelled orders.
