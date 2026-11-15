**Why this matters.** Some conditions are about rows and some are about groups. Mixing them up is one of the most common SQL errors, and it comes up whenever a question says "with at least N orders and an average above X".

**How we get there.**
1. Keep delivered orders with `WHERE status = 'delivered'`. This filters individual rows, before any grouping happens.
2. `GROUP BY restaurant_id`, one group per restaurant.
3. Compute `COUNT(*) AS n` and `AVG(actual_minutes) AS avg_min`.
4. Filter the groups with `HAVING COUNT(*) >= 40 AND AVG(actual_minutes) > 42`. These tests need the aggregates, so they cannot go in `WHERE`.
5. `ORDER BY avg_min DESC`, slowest first.

**Check it.** `WHERE` runs before the groups exist and `HAVING` runs after them. The `WHERE` filter also matters for `COUNT(*)`: without it cancelled orders would be counted in `n` and in the 40 threshold (`AVG` alone would already skip their NULL times). The cost is one scan and a group.

**Watch out.** Putting `COUNT(*) >= 40` in `WHERE`, which is an error because aggregates do not exist yet at that stage.
