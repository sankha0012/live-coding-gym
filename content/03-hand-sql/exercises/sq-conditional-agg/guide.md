**Why this matters.** We often need several counts side by side, such as delivered and cancelled per cuisine. The beginner answer runs two queries and glues them; the better answer gets both numbers in one pass.

**How we get there.**
1. Cuisine is on the restaurant, so join `orders o` to `restaurants r` first.
2. Group by `r.cuisine`, so we get one row per cuisine.
3. For delivered orders, add up a flag: `SUM(CASE WHEN o.status = 'delivered' THEN 1 ELSE 0 END)`. Each delivered order adds 1, every other adds 0, so the sum is a count.
4. Repeat the same idea for `'cancelled'` in a second column.
5. Sort by cuisine.

**Check it.** The `ELSE 0` matters: without it a non-matching row gives NULL, and a cuisine with no match would show NULL instead of 0. Both columns come from one scan, which is linear in the number of orders.

**Watch out.** Putting `WHERE status = 'delivered'` filters the cancelled rows away before the second column can count them.
