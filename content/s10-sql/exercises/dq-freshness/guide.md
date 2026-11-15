**Why this matters.** A feed that stopped sending data looks fine until someone checks the dates. The sneaky case is a restaurant that never sent anything: it has no orders, so a query on the orders table never mentions it.

**How we get there.**
1. Start from `restaurants`, not `orders`. The list of restaurants we expect is the source of truth.
2. `LEFT JOIN orders` on `restaurant_id`. A restaurant with no orders stays, with NULL order columns.
3. `GROUP BY r.restaurant_id` and take `MAX(o.created_at)` as the latest order. For a restaurant with no orders, the max is NULL.
4. Filter groups with `HAVING`, because the max only exists after grouping: `MAX(o.created_at) IS NULL OR MAX(o.created_at) < '2026-10-29 00:00:00'`. The cutoff is 72 hours before the fixed reference time.
5. Sort by `latest_created_at, r.restaurant_id`. SQLite puts NULLs first in ascending order, so the never-seen restaurants lead.

**Check it.** A comparison with NULL is never true, which is why we test `IS NULL` separately. Timestamps in `YYYY-MM-DD HH:MM:SS` compare correctly as text. It is one join and one grouping.

**Watch out.** Writing `FROM orders` with an inner join silently drops the restaurants that are most broken.
