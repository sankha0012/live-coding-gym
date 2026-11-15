**Why this matters.** "Who has never done X" is one of the most common questions in real reporting, such as customers who never completed an order. The trap is that "no delivered order" includes two kinds of customer: those with no orders at all and those with only cancelled ones.

**How we get there.**
1. Start with the people we might return: `FROM customers c WHERE c.city = 'Rio de Janeiro'`.
2. Write the question we want to ask about each customer: does a delivered order of theirs exist? That is `SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'delivered'`.
3. The inner query refers to `c`, so it is correlated.
4. Wrap it in `NOT EXISTS (...)` so we keep a customer only when that search finds nothing.
5. Add `ORDER BY c.customer_id`.

**Check it.** Customers with zero orders pass, and so do those with only cancelled orders, because the status test removes those rows. An index on `orders(customer_id)` keeps each check cheap.

**Watch out.** Do not turn this into a join plus `status <> 'delivered'`: that keeps anyone who has even one cancelled order, even if they also have a delivered one.
