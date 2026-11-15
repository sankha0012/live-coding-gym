**Why this matters.** Orders store only ids, not names. To make a readable list we follow the ids to the tables that hold the names, which is the everyday job of a join.

**How we get there.**
1. Start from the table that holds the facts: `FROM orders o`. Short aliases keep the query readable.
2. Add customers: `JOIN customers c ON c.customer_id = o.customer_id`. The ON clause says which rows belong together.
3. Add restaurants the same way: `JOIN restaurants r ON r.restaurant_id = o.restaurant_id`.
4. The filter is about the order, so `WHERE o.subtotal >= 150` goes in WHERE.
5. Select the columns, naming them `c.name AS customer_name` and `r.name AS restaurant_name`, since both tables have a `name` column. Sort by `o.order_id`.

**Check it.** An inner join keeps only orders that have both a customer and a restaurant. Matching on primary keys keeps the cost roughly linear.

**Watch out.** Both `name` columns would collide without the aliases, and an ON clause with the wrong columns multiplies rows.
