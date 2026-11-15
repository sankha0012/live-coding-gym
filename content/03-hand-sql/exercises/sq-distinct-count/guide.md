**Why this matters.** "How many orders" and "how many customers" are different questions, because some customers order many times. Reports mix them up all the time.

**How we get there.**
1. Cuisine is on the restaurant, so join `orders o` to `restaurants r` on `restaurant_id`.
2. Filter with `WHERE o.status = 'delivered' AND r.cuisine = 'pizza'`.
3. `COUNT(*)` counts every remaining row. That is the number of orders.
4. `COUNT(DISTINCT o.customer_id)` counts each customer once, however often they ordered. That is the number of customers.
5. Both aggregates sit in one SELECT with no GROUP BY, so the result is a single row.

**Check it.** The distinct count can never exceed the order count; if it does, something is wrong. Counting distinct values needs extra work (a hash or a sort) on top of the scan.

**Watch out.** Using `COUNT(*)` for both columns, or forgetting `DISTINCT`, reports repeat buyers several times.
