**Why this matters.** Sometimes we first need a list that another query produces, such as the customers who cancelled three or more times, and then we want the full details of those customers. IN with a subquery does exactly that.

**How we get there.**
1. Build the list first, on `orders` alone: `SELECT customer_id FROM orders WHERE status = 'cancelled' GROUP BY customer_id HAVING COUNT(*) >= 3`.
2. This returns one column of ids: the customers with at least three cancelled orders. HAVING filters the groups after counting.
3. In the outer query, read from `customers` and keep rows with `WHERE customer_id IN (...)` that list.
4. Select `customer_id, name` and sort by `customer_id`.

**Check it.** IN cannot duplicate a customer, because it only tests membership. The cost is one pass over orders plus a lookup per customer.

**Watch out.** The flip side, `NOT IN`, returns nothing if the list contains a NULL, so prefer NOT EXISTS there.
