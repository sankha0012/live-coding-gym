**Why this matters.** An orphan is a row that points at something that does not exist, like an order for a courier nobody has on file. We count them before anyone trusts a join.

**How we get there.**
1. Start with the rule that needs no join: delivered orders with `courier_id IS NULL`. One `COUNT(*)` with a `WHERE`.
2. For the other checks, use the anti-join pattern. `LEFT JOIN` the parent table, then keep the rows where the parent key is NULL: `WHERE c.customer_id IS NULL`.
3. Couriers need one extra condition, `o.courier_id IS NOT NULL`. A cancelled order has no courier by design, and without this we would count every one of them.
4. Each check is a SELECT of a name and `COUNT(*)`. An aggregate with no matching rows still returns one row, with 0, so all four rows always appear.
5. Stack them with `UNION ALL` and put a single `ORDER BY check_name` at the end.

**Check it.** A clean database gives four rows of zero rather than an empty result. Each check is one pass over `orders`.

**Watch out.** Forgetting the NOT NULL guard on the courier makes the check report every cancelled order as missing.
