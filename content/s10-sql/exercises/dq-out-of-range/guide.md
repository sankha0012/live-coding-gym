**Why this matters.** Some values are impossible, like a negative price, and some are only suspicious, like a delivery that took ten times the promise. A small report of rule violations is the cheapest early warning on a table.

**How we get there.**
1. Write each rule as its own count: `SELECT 'actual_over_4x' AS rule_name, COUNT(*) AS violations FROM orders WHERE actual_minutes > 4 * promised_minutes`.
2. Keep each rule in a separate SELECT, so each has its own `WHERE`. The rules involve different columns and combine with `OR` inside one rule, like `subtotal < 0 OR delivery_fee < 0`.
3. For the minutes rule, put both conditions in one `WHERE` with `OR`: `promised_minutes <= 0 OR actual_minutes < 0`.
4. Stack the four SELECTs with `UNION ALL`. `COUNT(*)` returns 0 when nothing matches, so all four rows appear.
5. Finish with one `ORDER BY rule_name` after the last SELECT.

**Check it.** A comparison with NULL is never true, so cancelled orders with no `actual_minutes` are not flagged, which is what we want. Linear scan per rule.

**Watch out.** Writing `>=` instead of `>` at a boundary, like exactly 150, counts orders that are fine.
