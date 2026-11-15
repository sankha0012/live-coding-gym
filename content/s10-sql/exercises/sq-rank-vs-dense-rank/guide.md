**Why this matters.** Rankings with ties are a classic source of off-by-one answers. "Second place" means different things depending on whether tied rows leave a gap in the numbering.

**How we get there.**
1. In a CTE, count delivered orders per restaurant: `WHERE status = 'delivered' GROUP BY restaurant_id`. Restaurants with none never appear.
2. Rank the counts with `RANK() OVER (ORDER BY orders DESC)`. Equal counts share a rank, and the next rank skips numbers: 1, 1, 3.
3. Add `DENSE_RANK() OVER (ORDER BY orders DESC)` next to it. It also shares ranks on ties but never skips: 1, 1, 2.
4. Both windows read the same ordering, so they sit in the same `SELECT`.
5. `ORDER BY rnk, restaurant_id`, so tied restaurants come out in a fixed order.

**Check it.** We count first and rank second, because a window runs after grouping. The cost is one aggregate plus one sort.

**Watch out.** Mixing up the two: `RANK` for "what position is this", `DENSE_RANK` for "the second highest value".
