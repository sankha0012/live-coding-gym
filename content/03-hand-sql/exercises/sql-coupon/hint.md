100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders), or SUM(COUNT(*)) OVER () as the denominator.
