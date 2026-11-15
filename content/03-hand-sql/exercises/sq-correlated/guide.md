**Why this matters.** "The biggest one within each group" is a classic: top order per restaurant, latest login per user. The twist here is ties: if two orders share the top subtotal, both must appear.

**How we get there.**
1. Start by listing delivered orders: `FROM orders o WHERE o.status = 'delivered'`.
2. For each row we need to know the best subtotal in its own restaurant. That is a smaller question: `SELECT MAX(x.subtotal) FROM orders x WHERE x.restaurant_id = o.restaurant_id AND x.status = 'delivered'`.
3. The inner query uses `o` from the outside, so it is correlated: it is re-evaluated in the context of each outer row.
4. Keep the row only if `o.subtotal` equals that maximum.
5. Sort by restaurant, then order.

**Check it.** Using equals keeps every tied order, which is what the problem wants. A restaurant with no delivered orders has no outer rows, so it never appears. Naively this is one inner search per row; an index on `restaurant_id` makes that cheap.

**Watch out.** The inner query must repeat the delivered filter, or a cancelled order could set the maximum.
