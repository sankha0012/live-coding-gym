**Why this matters.** Marketing wants to split customers into tiers, such as top 25% spenders. The trap is that `NTILE` needs a stable ordering: if two customers have the same spend, which band they land in must not be left to chance.

**How we get there.**
1. In a CTE, join `customers` to `orders`, keep Curitiba and delivered orders, and `GROUP BY c.customer_id`. The inner join already drops customers with no delivered orders.
2. Compute `ROUND(SUM(o.subtotal), 2)` as `spend`.
3. Outside the CTE, deal the customers into four groups: `NTILE(4) OVER (ORDER BY spend DESC, customer_id)`. Highest spenders come first, so they get band 1.
4. The second sort key, `customer_id`, settles ties the same way every time.
5. Finish with `ORDER BY band, spend DESC, customer_id`.

**Check it.** If the count does not divide by 4, the first bands each get one extra customer. The cost is one group and one sort.

**Watch out.** Leaving the tie-break out of the window, so equal spenders can fall on either side of a band boundary.
